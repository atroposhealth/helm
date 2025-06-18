from typing import Dict, Optional, Set

from helm.benchmark.annotation.model_as_judge import AnnotatorModelInfo, LLMAsJuryAnnotator
from helm.clients.auto_client import AutoClient


DIRECTION_PROMPT_TEMPLATE = """# Instructions
You are an expert in medical research. 
I will give you 2 inputs. 
The first is a prompt to summarize a retrospective observational research study. 
The second is a summary generated from the prompt. 
Your job is to judge whether the direction of all effects reported in the summary matches the prompt.

## Specific rules
- Treat all continuous outcomes (cont) with a positive value as an increase over baseline.
- All mean differences (MD) are Intervention minus Control.
- Only evaluate if the direction of the effect (positive/negative, increase/decrease) reported in the summary matches the prompt
  - However, if an effect is not significant, it is acceptable to report as "no difference" even if the prompt numerically shows an increase or decrease.

# Response
Your response should be either 0 or 1. 1 indicates the direction of all effects is reported correctly. Otherwise, respond with 0. Only mention one of these two responses.

# Inputs
[BEGIN DATA]
The summarization prompt is: {{QUESTION}}. 
The summary is: {{RESPONSE}}.
[END DATA]

# Output Format
Generate a valid JSON object with your evaluation:
{
    "direction_of_effect": {
        "score": 0,
        "explanation": "Explain why this score was given."
    },
}

Ensure the output is valid JSON:
- Use **double quotes** (") for all keys and string values.
- When quoting text or sections inside the explanations, use escaped double quotes (\") to
  maintain valid JSON formatting.
- Do not include any additional information in the output.
"""

DIRECTION_ANNOTATION_CRITERIA: Dict[str, Set[str]] = {
    "direction_of_effect": {"score", "explanation"},
}


NUMBERS_PROMPT_TEMPLATE = """# Instructions
You are an expert in medical research. 
I will give you 2 inputs. 
The first is a prompt to summarize a retrospective observational research study. 
The second is a summary generated from the prompt. 
Your job is to judge whether all numbers in the summary are accurately sourced from the prompt with reasonable rounding.

## Specific rules
- Only evaluate if the numbers in the summary match the relevant source in the prompt.
- Rounding of decimals is allowed, so long as it is numerically accurate.

# Response
Your response should be either 0 or 1. 1 indicates the numbers are all reported correctly. Otherwise, respond with 0. Only mention one of these two responses.

# Inputs
[BEGIN DATA]
The summarization prompt is: {{QUESTION}}. 
The summary is: {{RESPONSE}}.
[END DATA]

# Output Format
Generate a valid JSON object with your evaluation:
{
    "numbers_accurate": {
        "score": 0,
        "explanation": "Explain why this score was given."
    },
}

Ensure the output is valid JSON:
- Use **double quotes** (") for all keys and string values.
- When quoting text or sections inside the explanations, use escaped double quotes (\") to
  maintain valid JSON formatting.
- Do not include any additional information in the output.
"""

NUMBERS_ANNOTATION_CRITERIA: Dict[str, Set[str]] = {
    "numbers_accurate": {"score", "explanation"},
}


COMPLETENESS_PROMPT_TEMPLATE = """# Instructions
You are an expert in medical research. 
I will give you 2 inputs. 
The first is a prompt to summarize a retrospective observational research study. 
The second is a summary generated from the prompt. 
Your job is to judge whether all significant outcomes in the prompt are mentioned in the summary.

## Specific rules
- Check if the prompt contains an outcome ending in '!pvalue' in the "outcomes" dictionary.
  - If so, and this p-value is <= 0.05, ensure the summary explicitly mentions that there is a difference or higher/lower risk with that outcome.
  - Note that not all studies have outcomes with p-values. In such cases, return "CORRECT".
- Non-significant outcomes do not need to be mentioned in the summary. 

# Response
Your response should be either 0 or 1. 1 indicates all significant outcomes from the prompt are mentioned in the summary. Otherwise, respond with 0. Only mention one of these two responses.

# Inputs
[BEGIN DATA]
The summarization prompt is: {{QUESTION}}. 
The summary is: {{RESPONSE}}.
[END DATA]

# Output Format
Generate a valid JSON object with your evaluation:
{
    "completeness": {
        "score": 0,
        "explanation": "Explain why this score was given."
    },
}

Ensure the output is valid JSON:
- Use **double quotes** (") for all keys and string values.
- When quoting text or sections inside the explanations, use escaped double quotes (\") to
  maintain valid JSON formatting.
- Do not include any additional information in the output.
"""

COMPLETENESS_ANNOTATION_CRITERIA: Dict[str, Set[str]] = {
    "completeness": {"score", "explanation"},
}

ANNOTATOR_MODELS: Dict[str, AnnotatorModelInfo] = {
    "oai": AnnotatorModelInfo(
        model_name="openai/o4-mini-2025-04-16",
        model_deployment="openai/o4-mini-2025-04-16",
    ),
    "claude": AnnotatorModelInfo(
        model_name="anthropic/claude-sonnet-4-20250514",
        model_deployment="anthropic/claude-sonnet-4-20250514",
    ),
    "gemini": AnnotatorModelInfo(
        model_name="google/gemini-2.5-pro",
        model_deployment="google/gemini-2.5-pro",
    ),

}


class MedSummaryDirectionAnnotator(LLMAsJuryAnnotator):
    """The MedSummary direction of effect autograder."""

    name = "medsummary"

    def __init__(self, auto_client: AutoClient, template_name: Optional[str] = None):
        super().__init__(
            auto_client=auto_client,
            prompt_template=DIRECTION_PROMPT_TEMPLATE,
            annotation_criteria=DIRECTION_ANNOTATION_CRITERIA,
            annotator_models=ANNOTATOR_MODELS,
        )

class MedSummaryNumbersAnnotator(LLMAsJuryAnnotator):
    """The MedSummary numbers autograder."""

    name = "medsummary"

    def __init__(self, auto_client: AutoClient, template_name: Optional[str] = None):
        super().__init__(
            auto_client=auto_client,
            prompt_template=NUMBERS_PROMPT_TEMPLATE,
            annotation_criteria=NUMBERS_ANNOTATION_CRITERIA,
            annotator_models=ANNOTATOR_MODELS,
        )

class MedSummaryCompletenessAnnotator(LLMAsJuryAnnotator):
    """The MedSummary completeness autograder."""

    name = "medsummary"

    def __init__(self, auto_client: AutoClient, template_name: Optional[str] = None):
        super().__init__(
            auto_client=auto_client,
            prompt_template=COMPLETENESS_PROMPT_TEMPLATE,
            annotation_criteria=COMPLETENESS_ANNOTATION_CRITERIA,
            annotator_models=ANNOTATOR_MODELS,
        )
