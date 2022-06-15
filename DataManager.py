import numpy as np

class DataManager:

    ballots_to_list_index: dict
    committees_to_list_index: dict
    profiles_to_list_index: dict
    multiplier: int
    feasible_committees_for_all_profiles: list[list[list[int]]]
    manipulation_table = list[list[list[bool]]]
    ballots = list[list[int]]

    def __init__(self, ballots: list[set[int]], committees: list[list[int]], profiles: list[list[set[int]]],
                 feasible_committees_for_all_profiles: list[list[list[int]]]):
        self.multiplier = len(committees)
        self.ballots=ballots
        self.ballots_to_list_index = self._list_to_list_position_dict(ballots)
        self.committees_to_list_index = self._list_to_list_position_dict(committees)
        self.profiles_to_list_index_dict = self._build_profiles_to_list_index_dict(profiles)
        self.feasible_committees_for_all_profiles=feasible_committees_for_all_profiles
        self.manipulation_table = self._compute_manipulation_table(committees, ballots)


    def _compute_manipulation_table(self, committees: list[list[int]], ballots: list[set[int]]) -> list[list[list[bool]]]:
        manipulation_table = []
        for ballot in ballots:
            preference_table=[]
            for committee1 in committees:
                item=[]
                for committee2 in committees:
                    item.append(len([party for party in committee1 if party in ballot])>len([party for party in committee2 if party in ballot]))
                preference_table.append(item)
            manipulation_table.append(preference_table)
        return manipulation_table


    def _build_profiles_to_list_index_dict(self, profiles) -> dict:
        profiles_by_ballot_indices = [np.sort([self.ballots_to_list_index[tuple(ballot)] for ballot in profile]) for profile in profiles]
        return self._list_to_list_position_dict(profiles_by_ballot_indices)


    def _profile_to_list_index(self, profile: list[set[int]]) -> int:
        profile_by_ballot_indices = [self.ballots_to_list_index[tuple(ballot)] for ballot in profile]
        return self.profiles_to_list_index_dict[tuple(profile_by_ballot_indices)]


    def _list_to_list_position_dict(self, input_list):
        output_dict = {}
        for i in range(0, len(input_list)):
            output_dict[tuple(input_list[i])] = i
        return output_dict


    def get_committee_index(self, committee: list[list[int]]) -> int:
        return self.committees_to_list_index[tuple(committee)]




    def get_variable(self, profile: list[set[int]], committee: list[int]) -> int :
        return self.multiplier*(1+self._profile_to_list_index(profile)) + self.committees_to_list_index[tuple(committee)]


    def get_feasible_committees_for_profile(self, profile: list[set[int]]) -> list[list[int]]:
        return self.feasible_committees_for_all_profiles[self._profile_to_list_index(profile)]


    def is_profile_known(self, profile: list[set[int]]) -> bool:
        profile_by_ballot_indices = [self.ballots_to_list_index[tuple(ballot)] for ballot in profile]
        profile_by_ballot_indices.sort()
        return tuple(profile_by_ballot_indices) in self.profiles_to_list_index_dict.keys()

    def sort_profile(self, profile: list[set[int]]) -> list[set[int]]:
        profile_by_ballot_indices = [self.ballots_to_list_index[tuple(ballot)] for ballot in profile]
        profile_by_ballot_indices.sort()
        return [self.ballots[index] for index in profile_by_ballot_indices]


    def voter_prefers_C1_to_C2(self, ballot: set[int], committe1: list[int], committe2: list[int]):
        return self.manipulation_table[self.ballots_to_list_index[tuple(ballot)]][self.committees_to_list_index[tuple(
            committe1)]][self.committees_to_list_index[tuple(committe2)]]
