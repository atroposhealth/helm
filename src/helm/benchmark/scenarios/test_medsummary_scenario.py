"""Tests for MedSummaryScenario."""

import os
import tempfile
import csv
from medsummary_scenario import MedSummaryScenario
from helm.benchmark.scenarios.scenario import TEST_SPLIT, CORRECT_TAG


def test_medsummary_scenario():
    """Test the MedSummary scenario with sample data."""
    
    # Create a temporary CSV file with test data
    with tempfile.TemporaryDirectory() as temp_dir:
        test_csv_path = os.path.join(temp_dir, "test_medsummary.csv")
        
        # Sample test data based on the actual CSV structure
        test_data = [
            {
                'id': 'test-001',
                'question': '''Generate a scientific summary for a cohort study in about 100 words like the example summary delimited by ------ for the question below. Make sure baseline differences relevant to the question are mentioned in the summary, but don't claim they are significant.

Question: Does treatment A vs treatment B affect outcome X in patients with condition Y?

Study Design:
{
  "population": "Patients with condition Y",
  "intervention": "Treatment A",
  "control": "Treatment B",
  "timeframe": "2020-2024"
}

Results:
{
  "intervention_size": "100",
  "control_size": "100",
  "baseline_differences": {"age_mean": "control 50 vs intervention 52"},
  "outcomes": {"outcome_x!OR": "1.5 (1.1, 2.0)", "outcome_x!pvalue": "0.02"}
}''',
                'answer': 'This cohort study compared treatment A (n=100) to treatment B (n=100) in patients with condition Y from 2020-2024. The intervention group was slightly older (52 vs 50 years). Treatment A was associated with a significantly higher rate of outcome X (OR 1.5, p=0.02).',
                'eval.direction_of_effect.label': 'correct',
                'eval.direction_of_effect.explanation': 'Correctly reported higher rate',
                'eval.numbers_accurate.label': 'correct',
                'eval.numbers_accurate.explanation': 'All numbers match',
                'eval.all_sig_outcomes.label': 'correct',
                'eval.all_sig_outcomes.explanation': 'Significant outcome reported'
            },
            {
                'id': 'test-002',
                'question': '''Generate a scientific summary for a cohort study...

Question: Another medical question

Study Design:
{
  "population": "Adults with diabetes",
  "intervention": "Drug X",
  "control": "Placebo",
  "timeframe": "2019-2023"
}

Results:
{
  "intervention_size": "200",
  "control_size": "200",
  "baseline_differences": {"bmi_mean": "control 28 vs intervention 29"},
  "outcomes": {"outcome_y!OR": "0.8 (0.6, 1.1)", "outcome_y!pvalue": "0.15"}
}''',
                'answer': 'This cohort study examined drug X (n=200) versus placebo (n=200) in adults with diabetes from 2019-2023. The intervention group had a slightly higher mean BMI (29 vs 28). There was no significant difference in outcome Y between groups (OR 0.8, p=0.15).',
                'eval.direction_of_effect.label': 'correct',
                'eval.direction_of_effect.explanation': 'Non-significant correctly reported',
                'eval.numbers_accurate.label': 'correct', 
                'eval.numbers_accurate.explanation': 'Numbers accurate',
                'eval.all_sig_outcomes.label': 'correct',
                'eval.all_sig_outcomes.explanation': 'No significant outcomes to report'
            }
        ]
        
        # Write test data to CSV
        with open(test_csv_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['id', 'question', 'answer', 
                         'eval.direction_of_effect.label', 'eval.direction_of_effect.explanation',
                         'eval.numbers_accurate.label', 'eval.numbers_accurate.explanation',
                         'eval.all_sig_outcomes.label', 'eval.all_sig_outcomes.explanation']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(test_data)
        
        # Test the scenario
        scenario = MedSummaryScenario(data_path=test_csv_path)
        instances = scenario.get_instances(temp_dir)
        
        # Verify instances were loaded correctly
        assert len(instances) == 2, f"Expected 2 instances, got {len(instances)}"
        
        # Check first instance
        first_instance = instances[0]
        assert first_instance.id == 'test-001'
        assert 'Does treatment A vs treatment B' in first_instance.input.text
        assert len(first_instance.references) == 1
        assert first_instance.references[0].output.text.startswith('This cohort study compared treatment A')
        assert CORRECT_TAG in first_instance.references[0].tags
        assert first_instance.split == TEST_SPLIT
        
        # Check extra data
        assert first_instance.extra_data['eval_direction_of_effect'] == 'correct'
        assert first_instance.extra_data['eval_numbers_accurate'] == 'correct'
        assert first_instance.extra_data['eval_all_sig_outcomes'] == 'correct'
        
        # Check second instance
        second_instance = instances[1]
        assert second_instance.id == 'test-002'
        assert 'Adults with diabetes' in second_instance.input.text
        assert 'no significant difference' in second_instance.references[0].output.text
        
        print("All tests passed!")


if __name__ == "__main__":
    test_medsummary_scenario()