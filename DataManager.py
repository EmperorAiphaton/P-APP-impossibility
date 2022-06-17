import numpy as np


class DataManager:

    def __init__(self, ballots: list[set[int]], committees: list[list[int]], profiles: list[list[set[int]]],
                 feasible_committees_for_all_profiles: list[list[list[int]]]):
        self.multiplier = len(committees)
        self.ballots=ballots
        self.ballots_to_list_index = self._list_to_list_position_dict(ballots)
        self.committees_to_list_index = self._list_to_list_position_dict(committees)
        self.profiles_to_list_index_dict = self._build_profiles_to_list_index_dict(profiles)
        self.feasible_committees_for_all_profiles=feasible_committees_for_all_profiles
        self.manipulation_table = self._compute_manipulation_table(committees, ballots)

    def _compute_manipulation_table(self, committees: list[list[int]], ballots: list[set[int]]) \
            -> list[list[list[bool]]]:
        """This function takes a set of committees and ballots, and outputs a list stating for all triples
        of the form (ballot, committee1, committee2) whether a voter with ballot as preference prefers
        committee1 to committee2."""
        manipulation_table = []
        for ballot in ballots:
            preference_table=[]
            for committee1 in committees:
                item=[]
                for committee2 in committees:
                    item.append(len([party for party in committee1 if party in ballot]) >
                                len([party for party in committee2 if party in ballot]))
                preference_table.append(item)
            manipulation_table.append(preference_table)
        return manipulation_table

    def _build_profiles_to_list_index_dict(self, profiles) -> dict:
        """This function takes a list of profiles as input and
        computes a map from the profiles to their position in the list."""
        profiles_by_ballot_indices = [np.sort([self.ballots_to_list_index[tuple(ballot)] for ballot in profile])
                                      for profile in profiles]
        return self._list_to_list_position_dict(profiles_by_ballot_indices)

    def _profile_to_list_index(self, profile: list[set[int]]) -> int:
        """This function takes a profile as input and returns a set containing the list indices of the
        ballots in the profile"""
        profile_by_ballot_indices = [self.ballots_to_list_index[tuple(ballot)] for ballot in profile]
        return self.profiles_to_list_index_dict[tuple(profile_by_ballot_indices)]

    def _list_to_list_position_dict(self, input_list):
        """This function takes an list (where each element is hashable) and returns a map from the list
        elements to their position in the list."""
        output_dict = {}
        for i in range(0, len(input_list)):
            output_dict[tuple(input_list[i])] = i
        return output_dict

    def get_committee_index(self, committee: list[list[int]]) -> int:
        """This function takes a committee and returns the position of the committee in the committee list"""
        return self.committees_to_list_index[tuple(committee)]

    def get_variable(self, profile: list[set[int]], committee: list[int]) -> int:
        """This function takes a profile and a committee as input and returns the integer corresponding
        to the variable of the input data in the logical formula."""
        return self.multiplier*(1+self._profile_to_list_index(profile)) \
               + self.committees_to_list_index[tuple(committee)]

    def get_feasible_committees_for_profile(self, profile: list[set[int]]) -> list[list[int]]:
        """This function takes a profile as input and returns the set of committees satisfying the
        specified axioms (weak representation, Pareto-optimality) for this profile. """
        return self.feasible_committees_for_all_profiles[self._profile_to_list_index(profile)]

    def is_profile_known(self, profile: list[set[int]]) -> bool:
        """This function checks whether the input profile is contained in the map from profiles to
        integers."""
        profile_by_ballot_indices = [self.ballots_to_list_index[tuple(ballot)] for ballot in profile]
        profile_by_ballot_indices.sort()
        return tuple(profile_by_ballot_indices) in self.profiles_to_list_index_dict.keys()

    def get_anonymous_profile(self, profile: list[set[int]]) -> list[set[int]]:
        """Given an input profile, this function returns the canonical representative of this profile."""
        profile_by_ballot_indices = [self.ballots_to_list_index[tuple(ballot)] for ballot in profile]
        profile_by_ballot_indices.sort()
        return [self.ballots[index] for index in profile_by_ballot_indices]

    def voter_prefers_committee1_to_committee2(self, ballot: set[int], committee1: list[int], committee2: list[int])\
            -> bool:
        """Given a ballot and two committees c1 and c2, this function decides whether a voter with the ballot as
        preference relation prefers c1 to c2."""
        return self.manipulation_table[self.ballots_to_list_index[tuple(ballot)
        ]][self.committees_to_list_index[tuple(committee1)]][self.committees_to_list_index[tuple(committee2)]]
