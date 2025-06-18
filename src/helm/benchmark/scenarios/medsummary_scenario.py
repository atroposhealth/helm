"""MedSummary scenario for HELM - Medical study summarization task."""

import csv
import os
from typing import List, Dict, Any

from helm.common.hierarchical_logger import hlog
from helm.benchmark.scenarios.scenario import (
    Scenario,
    Instance,
    Reference,
    TEST_SPLIT,
    CORRECT_TAG,
    Input,
    Output,
)


class MedSummaryScenario(Scenario):
    """
    MedSummary scenario for summarizing real-world evidence studies.
    
    This scenario evaluates language models on their ability to generate accurate
    scientific summaries of cohort studies based on structured study design and
    results data. The task requires:
    
    1. Understanding complex medical study designs
    2. Accurately reporting baseline differences between groups
    3. Correctly identifying and reporting statistically significant outcomes
    4. Maintaining scientific accuracy in reporting numbers and percentages
    5. Following specific formatting guidelines for medical summaries
    
    Each instance consists of:
    - A detailed prompt with study design and results in JSON format
    - A target summary that correctly summarizes the study
    - Evaluation labels for direction of effects, numerical accuracy, and 
      completeness of significant outcomes
    """
    
    name = "medsummary"
    description = (
        "A dataset for evaluating the ability to generate accurate scientific "
        "summaries of real-world evidence studies from structured data."
    )
    tags = ["summarization", "biomedical", "reasoning"]
    
    def __init__(self, data_path: str = None):
        super().__init__()
        self.data_path = data_path
    
    def get_instances(self, output_path: str) -> List[Instance]:
        """Load instances from the CSV file."""
        # If no data path specified, use the default location
        if self.data_path is None:
            self.data_path = os.path.join(output_path, "medsummary_data.csv")
        
        instances: List[Instance] = []
        
        # Read the CSV file
        hlog(f"Loading MedSummary data from {self.data_path}")
        
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for idx, row in enumerate(reader):
                    # Extract fields from the CSV
                    instance_id = row.get('id', f'instance_{idx}')
                    question = row['question']
                    answer = row['answer']
                    
                    # Extract evaluation labels
                    direction_label = row.get('eval.direction_of_effect.label', '')
                    direction_explanation = row.get('eval.direction_of_effect.explanation', '')
                    numbers_label = row.get('eval.numbers_accurate.label', '')
                    numbers_explanation = row.get('eval.numbers_accurate.explanation', '')
                    sig_outcomes_label = row.get('eval.all_sig_outcomes.label', '')
                    sig_outcomes_explanation = row.get('eval.all_sig_outcomes.explanation', '')
                    
                    # Create the instance
                    instance = Instance(
                        input=Input(text=question),
                        references=[
                            Reference(
                                Output(text=answer),
                                tags=[CORRECT_TAG]
                            )
                        ],
                        split=TEST_SPLIT,  # All instances go to test split
                        id=instance_id,
                        extra_data={
                            'eval_direction_of_effect': direction_label,
                            'eval_direction_explanation': direction_explanation,
                            'eval_numbers_accurate': numbers_label,
                            'eval_numbers_explanation': numbers_explanation,
                            'eval_all_sig_outcomes': sig_outcomes_label,
                            'eval_sig_outcomes_explanation': sig_outcomes_explanation,
                        }
                    )
                    
                    instances.append(instance)
            
            hlog(f"Loaded {len(instances)} instances from MedSummary dataset")
            
        except FileNotFoundError:
            hlog(f"Warning: Could not find data file at {self.data_path}")
            hlog("Please ensure the medsummary_data.csv file is available")
            
        return instances
    
    def get_evaluation_metrics(self) -> Dict[str, Any]:
        """
        Define evaluation metrics specific to medical summarization.
        
        This could be extended to include custom metrics that check:
        - Accuracy of reported p-values
        - Correct identification of significant vs non-significant outcomes
        - Numerical accuracy in reporting percentages and statistics
        - Proper direction of effects
        """
        # For now, we'll use standard summarization metrics
        # But this could be extended with custom medical accuracy metrics
        return {
            'include_basic_metrics': True,
            'include_summarization_metrics': True,
            'include_classification_metrics': False,
        }