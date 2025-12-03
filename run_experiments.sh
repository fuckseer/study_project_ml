#!/bin/bash
set -e

CONFIG_FILE="config/experiments.yml"

if ! command -v yq &> /dev/null
then
    echo "yq could not be found. Please install it (e.g., 'brew install yq' or 'pip install yq')."
    exit 1
fi

EXPERIMENT_NAME=$(yq e '.experiment_name' $CONFIG_FILE)

echo "🚀 Running experiment grid: $EXPERIMENT_NAME"

yq e '.param_grid[] | to_json' $CONFIG_FILE | while read -r params_json; do
    C_PARAM=$(echo "$params_json" | yq e '.c_param' -)
    PENALTY=$(echo "$params_json" | yq e '.penalty' -)
    SOLVER=$(echo "$params_json" | yq e '.solver' -)

    echo "---"
    echo "Running with: C=$C_PARAM, penalty=$PENALTY, solver=$SOLVER"

    docker-compose run --rm training \
        --experiment-name "$EXPERIMENT_NAME" \
        --c-param "$C_PARAM" \
        --penalty "$PENALTY" \
        --solver "$SOLVER"
done

echo "✅ All experiments completed successfully."