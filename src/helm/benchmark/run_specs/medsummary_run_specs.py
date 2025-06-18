"""Run specifications for MedSummary scenario in HELM."""

from typing import List

from helm.benchmark.adaptation.adapter_spec import AdapterSpec
from helm.benchmark.adaptation.common_adapter_specs import (
    get_generation_adapter_spec,
)
from helm.benchmark.annotation.annotator import AnnotatorSpec
from helm.benchmark.metrics.common_metric_specs import get_generic_metric_specs
from helm.benchmark.metrics.metric import MetricSpec

from helm.benchmark.run_spec import RunSpec, run_spec_function
from helm.benchmark.scenarios.medsummary_scenario import MedSummaryScenario
from helm.benchmark.scenarios.scenario import ScenarioSpec


@run_spec_function("medsummary")
def get_medsummary_run_spec(
    stop_sequences: List[str] = None,
    max_train_instances: int = 0,
    temperature: float = 0.0,
) -> RunSpec:
    scenario_spec = ScenarioSpec(class_name="helm.benchmark.scenarios.medsummary_scenario.MedSummaryScenario")
    adapter_spec = get_generation_adapter_spec(
        instructions="",  # Instructions are already in the prompt
        input_noun=None,  # No need for input/output nouns
        output_noun=None,
        max_train_instances=max_train_instances,
        max_tokens=600, # Allow enough tokens for detailed summaries
        temperature=temperature,
        stop_sequences=stop_sequences if stop_sequences else [],
    )
    # annotator_specs = [AnnotatorSpec(class_name="helm.benchmark.annotation.medsummary_annotator.MedSummaryDirectionAnnotator")]
    # annotator_specs = [AnnotatorSpec(class_name="helm.benchmark.annotation.medsummary_annotator.MedSummaryNumbersAnnotator")]
    annotator_specs = [AnnotatorSpec(class_name="helm.benchmark.annotation.medsummary_annotator.MedSummaryCompletenessAnnotator")]


    metric_specs = [
        # MetricSpec(class_name="helm.benchmark.metrics.medsummary_metrics.MedSummaryDirectionMetric", args={}),
        # MetricSpec(class_name="helm.benchmark.metrics.medsummary_metrics.MedSummaryNumbersMetric", args={}),
        MetricSpec(class_name="helm.benchmark.metrics.medsummary_metrics.MedSummaryCompletenessMetric", args={}),
        MetricSpec(class_name="helm.benchmark.metrics.basic_metrics.BasicGenerationMetric", args={"names": []})
    ]
    return RunSpec(
        name="medsummary",
        scenario_spec=scenario_spec,
        adapter_spec=adapter_spec,
        metric_specs=metric_specs,
        annotators=annotator_specs,
        groups=["medsummary"],
    )
