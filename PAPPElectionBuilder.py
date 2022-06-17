import numpy as np
import itertools


class PAPPElectionBuilder:

    def __init__(self, committee_size: int, number_of_parties: int, number_of_voters: int, profile_all: bool):
        self.m = number_of_parties
        self.k = committee_size
        self.n = number_of_voters
        self.parties = list(np.arange(0, self.m))
        self.voters = list(np.arange(0, self.n))
        self.profile_all = profile_all

    def _compute_approval_scores(self, profile: list[set[int]]) -> list[int]:
        """Given a profile, this function returns the approval scores of all parties."""
        approval_scores = np.zeros(self.m, dtype=int)
        for party in range(0, self.m):
            for ballot in profile:
                if party in ballot:
                    approval_scores[party] += 1
        return list(approval_scores)

    def compute_approval_ballots(self) -> list[set[int]]:
        """This function computes the set of all ballots used for the logical formula."""
        ballots = []
        for i in range(1, 2 ** self.m):
            ballots.append({party for party in self.parties if (i // (2 ** party)) % 2 == 1})
        if not self.profile_all:
            ballots = ballots[0:len(ballots) - 1]
        return ballots

    def compute_all_committees(self) -> list[list[int]]:
        """This function computes a list of all committees"""
        committees = [list(committee) for committee in itertools.combinations_with_replacement(self.parties, self.k)]
        return committees

    def compute_approval_profiles(self, ballots: list[set[int]]) -> list[list[set[int]]]:
        """Given a set of ballots, this function computes the preference profiles used for the logical formula."""
        profiles = [list(profile) for profile in itertools.combinations_with_replacement(ballots, self.n)]
        if self.profile_all:
            return profiles
        profs = []
        for profile in profiles:
            approval_scores = self._compute_approval_scores(profile)
            if max(approval_scores) <= 4 and sum(approval_scores) <= 11:
                profs.append(profile)
        return profs
