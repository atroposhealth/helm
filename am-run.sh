# Pick any suite name of your choice
export SUITE_NAME=am43

# Replace this with your model or models
export MODELS_TO_RUN="openai/gpt-4.1-2025-04-14 openai/o4-mini-2025-04-16 openai/o3-2025-04-16 anthropic/claude-3-7-sonnet-20250219 anthropic/claude-opus-4-20250514 anthropic/claude-sonnet-4-20250514 google/gemini-2.5-pro google/gemini-2.5-flash google/gemini-2.0-flash-001"
# export MODELS_TO_RUN="anthropic/claude-opus-4-20250514 anthropic/claude-sonnet-4-20250514"
# export MODELS_TO_RUN="openai/gpt-4.1-2025-04-14 google/gemini-2.0-flash-001"

export RUN_ENTRIES_CONF_PATH=run_entries_medsummaryeval.conf
export SCHEMA_PATH=schema_medsummary.yaml
export NUM_TRAIN_TRIALS=0
export MAX_EVAL_INSTANCES=100
export PRIORITY=2

helm-run --conf-paths $RUN_ENTRIES_CONF_PATH --num-train-trials $NUM_TRAIN_TRIALS --max-eval-instances $MAX_EVAL_INSTANCES --priority $PRIORITY --suite $SUITE_NAME --models-to-run $MODELS_TO_RUN

helm-summarize --schema $SCHEMA_PATH --suite $SUITE_NAME

helm-server --suite $SUITE_NAME
