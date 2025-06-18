from helm.benchmark.annotation.medsummary_annotator import ANNOTATOR_MODELS
from helm.benchmark.metrics.llm_jury_metrics import LLMJuryMetric


class MedSummaryDirectionMetric(LLMJuryMetric):
    """Score metrics for MedSummary Direction of Effect."""

    def __init__(self):
        super().__init__(
            metric_name="medsummary_direction_of_effect",
            scenario_name="medsummary",
            annotator_models=ANNOTATOR_MODELS,
            default_score=0.0,
        )

class MedSummaryNumbersMetric(LLMJuryMetric):
    """Score metrics for MedSummary Numbers Accurate."""

    def __init__(self):
        super().__init__(
            metric_name="medsummary_numbers",
            scenario_name="medsummary",
            annotator_models=ANNOTATOR_MODELS,
            default_score=0.0,
        )

class MedSummaryCompletenessMetric(LLMJuryMetric):
    """Score metrics for MedSummary Completeness."""

    def __init__(self):
        super().__init__(
            metric_name="medsummary_completeness",
            scenario_name="medsummary",
            annotator_models=ANNOTATOR_MODELS,
            default_score=0.0,
        )
