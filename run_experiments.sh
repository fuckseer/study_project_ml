#!/bin/bash
set -e

CONFIG_FILE="config/experiments.yml"

EXPERIMENT_NAME=$(yq e '.experiment_name' "$CONFIG_FILE")

echo "🚀 Running experiment grid: $EXPERIMENT_NAME"

yq e '.param_grid[] | [.c_param, .penalty, .solver] | @tsv' "$CONFIG_FILE" | \
while IFS=$'\t' read -r C_PARAM PENALTY SOLVER; do

    echo "---"
    echo "Running with: C=$C_PARAM, penalty=$PENALTY, solver=$SOLVER"

    docker compose run --rm -T training \
        python -m study_project_ml.pad_project_ml.modeling.train \
        --experiment-name "$EXPERIMENT_NAME" \
        --c-param "$C_PARAM" \
        --penalty "$PENALTY" \
        --solver "$SOLVER"
done

echo "✅ All experiments completed!"