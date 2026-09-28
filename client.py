"""Multi-Armed Bandit Decision Engine (UCB1 & Thompson Sampling)
100% Python Standard Library (math, random).
"""

import math
import random

class MultiArmedBanditEngine:
    """Bandit optimization engine supporting UCB1 and Thompson sampling."""
    def __init__(self, k_arms=5):
        self.k_arms = k_arms
        self.counts = [0] * k_arms
        self.values = [0.0] * k_arms
        self.alpha = [1.0] * k_arms
        self.beta = [1.0] * k_arms
        self.total_pulls = 0

    def select_ucb1(self):
        for i in range(self.k_arms):
            if self.counts[i] == 0:
                return i
        best_arm = 0
        best_bound = -1.0
        for i in range(self.k_arms):
            bonus = math.sqrt(2.0 * math.log(self.total_pulls) / self.counts[i])
            ucb = self.values[i] + bonus
            if ucb > best_bound:
                best_bound = ucb
                best_arm = i
        return best_arm

    def update(self, arm, reward):
        self.total_pulls += 1
        self.counts[arm] += 1
        self.values[arm] += (reward - self.values[arm]) / self.counts[arm]
        if reward > 0.5:
            self.alpha[arm] += 1.0
        else:
            self.beta[arm] += 1.0

    def get_stats(self):
        return {
            "total_pulls": self.total_pulls,
            "arm_counts": self.counts,
            "arm_values": [round(v, 4) for v in self.values],
            "best_arm": max(range(self.k_arms), key=lambda i: self.values[i])
        }
