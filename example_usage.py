from client import MultiArmedBanditEngine

def main():
    bandit = MultiArmedBanditEngine(k_arms=4)
    # True rewards: arm 2 is best
    for _ in range(50):
        arm = bandit.select_ucb1()
        reward = 1.0 if arm == 2 else 0.1
        bandit.update(arm, reward)
    stats = bandit.get_stats()
    print("Multi-Armed Bandit UCB1 Verification:")
    print(f"Total Pulls: {stats['total_pulls']}, Best Arm: {stats['best_arm']}")
    print(f"Arm Pulls: {stats['arm_counts']}")

if __name__ == "__main__":
    main()
