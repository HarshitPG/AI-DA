import numpy as np
import matplotlib.pyplot as plt

class CareerPathNetwork:
    def __init__(self):
        # Conditional Probability Distributions
        self.P_AptitudeSkills = 0.6
        self.P_CodingSkills_given_AptitudeSkills = {
            True: 0.7,
            False: 0.3
        }
        self.P_GoJob_given_Skills = {
            (True, True): 0.9,
            (True, False): 0.4,
            (False, True): 0.5,
            (False, False): 0.1
        }
        self.P_StartupSuccess_given_GoJob = {
            (True, True): 0.3,
            (True, False): 0.1,
            (False, True): 0.2,
            (False, False): 0.05
        }

    def monte_carlo_simulation(self, num_samples=10000, target_evidence=None):
        count_target_event = 0
        count_evidence_event = 0

        for _ in range(num_samples):
            # Sample the nodes based on the given conditional probabilities
            aptitude_skills = target_evidence.get('aptitude_skills', np.random.rand() < self.P_AptitudeSkills)
            coding_skills = target_evidence.get('coding_skills', np.random.rand() < self.P_CodingSkills_given_AptitudeSkills[aptitude_skills])
            go_job = target_evidence.get('go_job', np.random.rand() < self.P_GoJob_given_Skills[(aptitude_skills, coding_skills)])
            startup_success = np.random.rand() < self.P_StartupSuccess_given_GoJob[(go_job, coding_skills)]

            # Check if the sampled values match the target evidence
            evidence_match = all(
                value == target_evidence.get(key, None)
                for key, value in locals().items()
                if key in target_evidence
            )

            if evidence_match:
                count_evidence_event += 1
                if startup_success:
                    count_target_event += 1

        # Calculate the conditional probability
        return count_target_event / count_evidence_event if count_evidence_event > 0 else 0

    def run_simulations(self):
        scenarios = [
            {'name': 'P(Startup Success | High Aptitude, Coding Skills)',
             'evidence': {'aptitude_skills': True, 'coding_skills': True}},
            {'name': 'P(Startup Success | Low Aptitude, Low Coding Skills)',
             'evidence': {'aptitude_skills': False, 'coding_skills': False}}
        ]

        sample_sizes = [100, 1000, 10000, 100000]
        plt.figure(figsize=(10, 6))

        for scenario in scenarios:
            scenario_probs = []
            for samples in sample_sizes:
                prob = self.monte_carlo_simulation(
                    num_samples=samples,
                    target_evidence=scenario['evidence']
                )
                scenario_probs.append(prob)
            
            plt.plot(sample_sizes, scenario_probs, marker='o', label=scenario['name'])

        plt.xscale('log')
        plt.xlabel('Number of Samples')
        plt.ylabel('Estimated Probability')
        plt.title('Career Path Simulation: Startup Success Probability')
        plt.legend()
        plt.grid(True)
        plt.show()

        return {scenario['name']: self.monte_carlo_simulation(num_samples=100000, target_evidence=scenario['evidence'])
                for scenario in scenarios}

career_network = CareerPathNetwork()
results = career_network.run_simulations()
print("Startup Success Probabilities:")
for scenario, probability in results.items():
    print(f"{scenario}: {probability:.2%}")