import itertools

import numpy as np
import math

class AxiomHelper:

    k: int
    m: int
    n: int
    pareto_optimality: bool
    weak_representation_naive: bool
    parties: list[int]

    def __init__(self, committee_size: int, number_of_parties: int, number_of_voters: int, pareto_optimality: bool, weak_representation_naive: bool):
        self.m= number_of_parties
        self.k=committee_size
        self.n=number_of_voters
        self.parties = list(np.arange(0, self.m))
        self.pareto_optimality=pareto_optimality
        self.weak_representation_naive=weak_representation_naive


    # computes how often each party is uniquely approved in a profile
    def _compute_unique_approval_scores(self, profile: list[set[int]]) -> list[int]:
        unique_approval_scores = np.zeros(self.m, dtype=int)
        for party in range(0, self.m):
            for ballot in profile:
                if ballot == {party}:
                    unique_approval_scores[party] += 1
        return list(unique_approval_scores)


    def _pareto_dominance(self, party1: int, party2: int, profile: list[set[int]]) -> bool:
        strict_preference = False
        for ballot in profile:
            if party2 in ballot and party1 not in ballot:
                return False
            if party1 in ballot and party2 not in ballot:
                strict_preference = True
        return strict_preference


    def _filter_committees_failing_weak_representation(self, profile: list[set[int]], committees: list[list[int]]) -> list[list[int]]:
        unique_approval_scores = self._compute_unique_approval_scores(profile)
        parties_deserving_representation = {party for party in self.parties if unique_approval_scores[party] >= self.n / self.k}
        possible_committees = [committee for committee in committees if parties_deserving_representation.issubset(set(committee))]
        return possible_committees


    def _filter_committees_failing_pareto_optimality(self, profile: list[set[int]], committees: list[list[int]]) -> list[list[int]]:
        pareto_dominated_parties = set()
        for party1 in self.parties:
            for party2 in self.parties:
                if self._pareto_dominance(party1, party2, profile):
                    pareto_dominated_parties.add(party2)
        possible_committees = [committee for committee in committees if set(committee).isdisjoint(pareto_dominated_parties)]
        return possible_committees


    def _profile_contains_subset_list(self, profile: list[set[int]], input_set: set[int], start: int, length: int) -> bool:
        if length == 0:
            return True
        else:
            for index in range(start, len(profile)):
                if profile[index].issubset(set(input_set)):
                    if self._profile_contains_subset_list(profile, profile[index], index + 1, length - 1):
                        return True
        return False


    def _filter_committees_failing_weak_representation_clever(self, profile: list[set[int]], committees: list[list[int]],
                                                             value_of_committee_for_ballot: dict) -> list[list[int]]:
        unique_approval_scores = self._compute_unique_approval_scores(profile)
        parties_deserving_representation = {party for party in self.parties if
                                            unique_approval_scores[party] >= self.n / self.k}

        required_number_of_approved_members = {}
        for ballot in profile:
            ballot_as_tuple = tuple(ballot)
            if ballot_as_tuple not in required_number_of_approved_members.keys():
                if len(ballot)==1 and ballot_as_tuple[0] in parties_deserving_representation:
                    required_number_of_approved_members[ballot_as_tuple]=1
                else:
                    required_number_of_approved_members[ballot_as_tuple] = 0

        reduced_profile = [ballot for ballot in profile if not ballot.issubset(parties_deserving_representation)]
        reduced_profile.reverse()
        for index in range(0, len(reduced_profile)):
            if self._profile_contains_subset_list(reduced_profile, reduced_profile[index], index + 1, math.ceil(self.n / self.k)-1):
                required_number_of_approved_members[tuple(reduced_profile[index])] = \
                    len(parties_deserving_representation.intersection(reduced_profile[index])) + 1
        return [committee for committee in committees
                if all([value_of_committee_for_ballot[tuple([entry for item in [committee, ballot] for entry in item])]
                        >= required_number_of_approved_members[tuple(ballot)] for ballot in profile])]


    def compute_numbers_of_approvals(self, committees: list[list[int]], ballots: list[set[int]]) -> dict:
        number_of_approvals={}
        for committee in committees:
            for ballot in ballots:
                key = [entry for item in [committee, ballot ] for entry in item]
                number_of_approvals[tuple(key)]=len([party for party in committee if party in ballot])
        return number_of_approvals


    def compute_feasible_committees_for_all_profiles(self, profiles: list[list[set[int]]], committees: list[list[int]], ballots: list[set[int]]) -> list[list[list[int]]]:
        feasible_committees: list[list[list[int]]] = []
        for profile in profiles:
            feasible_committees_for_profile = committees
            if self.weak_representation_naive:
                feasible_committees_for_profile = self._filter_committees_failing_weak_representation(profile, feasible_committees_for_profile)
            else:
                value_of_committee_for_ballot = self.compute_numbers_of_approvals(committees, ballots)
                feasible_committees_for_profile = self._filter_committees_failing_weak_representation_clever(profile,feasible_committees_for_profile,                                                                                           value_of_committee_for_ballot)
            if self.pareto_optimality:
                feasible_committees_for_profile = self._filter_committees_failing_pareto_optimality(profile, feasible_committees_for_profile)
            feasible_committees.append(feasible_committees_for_profile)
        return feasible_committees