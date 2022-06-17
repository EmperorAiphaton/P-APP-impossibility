import pycosat

from PAPPElectionBuilder import PAPPElectionBuilder
from AxiomHelper import AxiomHelper
from DataManager import DataManager
import itertools


class FormulaConstructor:

    def __init__(self, committee_size: int, number_of_parties: int, number_of_voters: int, pareto_optimality: bool,
                 weak_representation_naive: bool,
                 all_profiles: bool):
        self.election_builder = PAPPElectionBuilder(committee_size, number_of_parties, number_of_voters, all_profiles)
        self.ballots = self.election_builder.compute_approval_ballots()
        self.committees = self.election_builder.compute_all_committees()
        self.profiles = self.election_builder.compute_approval_profiles(self.ballots)
        self.axiom_helper = AxiomHelper(committee_size, number_of_parties,
                                        number_of_voters, pareto_optimality, weak_representation_naive)
        self.feasible_committees_for_all_profiles = \
            self.axiom_helper.compute_feasible_committees_for_all_profiles(self.profiles, self.committees, self.ballots)
        self.data_manager = \
            DataManager(self.ballots, self.committees, self.profiles, self.feasible_committees_for_all_profiles)

    def write_papp_function_constraints(self) -> list[list[int]]:
        """This function writes the constraints specifying that the variables indeed encode a logical formula.
        Since we already filtered out all committees that violate weak representation (and, depending on the
        input parameters, some other axioms) for all profiles, this function also encodes that the function
        satisfies weak representation (and all other input axioms)."""
        formula = list()
        for profile in self.profiles:
            feasible_committees = self.data_manager.get_feasible_committees_for_profile(profile)
            formula.append([self.data_manager.get_variable(profile, committee) for committee in feasible_committees])
            if len(feasible_committees) > 1:
                for [committee1, committee2] in list(itertools.combinations(feasible_committees, 2)):
                    formula.append([-self.data_manager.get_variable(profile, committee1),
                                    -self.data_manager.get_variable(profile, committee2)])
        return formula

    def write_strategyproofness_constraint(self) -> list[list[int]]:
        """This function writes the strategy-proofness constraints as described in [1]"""
        formula = []
        already_written = set()
        'In this set, we keep track of constraints we have already written to avoid duplication'
        for true_profile in self.profiles:
            true_feasible_committees = self.data_manager.get_feasible_committees_for_profile(true_profile)
            for manipulator in range(0, len(true_profile)):
                for ballot in self.ballots:
                    if ballot != true_profile[manipulator]:
                        manipulated_profile = true_profile.copy()
                        manipulated_profile[manipulator] = ballot
                        'after the manipulation, we may have to reorder the voters to find the canonical representative'
                        manipulated_profile = self.data_manager.get_anonymous_profile(manipulated_profile)
                        if self.data_manager.is_profile_known(manipulated_profile):
                            manipulated_feasible_committees = \
                                self.data_manager.get_feasible_committees_for_profile(manipulated_profile)
                            for committee1 in true_feasible_committees:
                                for committee2 in manipulated_feasible_committees:
                                    if self.data_manager.voter_prefers_committee1_to_committee2(ballot, committee1,
                                                                                                committee2):
                                        constraint = [-self.data_manager.get_variable(true_profile, committee1),
                                                      -self.data_manager.get_variable(manipulated_profile, committee2)]
                                        if tuple(constraint) not in already_written:
                                            formula.append(constraint)
                                            already_written.add(tuple(constraint))
        return formula

    def write_symmetry_breaking_clause(self) -> list[list[int]]:
        """Specifies the symmetry-breaking clause as discussed by Lemma 2 in [1]."""
        tie_breaking_profile = [{0}, {0, 1}, {1}, {2}, {2, 3}, {3}]
        tie_breaking_profile = self.data_manager.get_anonymous_profile(tie_breaking_profile)
        allowed_committees = [[0, 0, 2], [0, 1, 2]]
        return [[self.data_manager.get_variable(tie_breaking_profile, committee) for committee in allowed_committees]]

    def write_formula(self, output_file: str, sat_solve: bool, symmetry_breaking: bool) -> None:
        """This function writes the logical formula in the output file. If sat_solve is true, it
        also calls a SAT solver to check whether the logical formula is unsatisfiable."""
        formula = []
        if symmetry_breaking:
            formula = self.write_symmetry_breaking_clause()
        formula.extend(self.write_papp_function_constraints())
        formula.extend(self.write_strategyproofness_constraint())
        if sat_solve:
            if pycosat.solve(formula) == "UNSAT":
                print("unsatisfiable")
            else:
                print("satisfiable")
        max_var = max([max([abs(int(variable)) for variable in constraint]) for constraint in formula])
        f = open(output_file, "w")
        s = "p cnf " + str(max_var) + " " + str(len(formula)) + "\n"
        f.write(s)
        for item in formula:
            for entry in item:
                f.write(str(entry) + " ")
            f.write("0\n")
        f.close()
