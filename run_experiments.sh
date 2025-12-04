#!/bin/bash
set -euo pipefail

CONFIG_FILE="config/experiments.yml"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

echo "📘 Using config: $CONFIG_FILE"

EXPERIMENT_NAME=$(yq e '.experiment_name' "$CONFIG_FILE")
echo "🚀 Running experiment grid: $EXPERIMENT_NAME"
echo

GRID_LEN=$(yq e '.param_grid | length' "$CONFIG_FILE")

for (( i=0; i<GRID_LEN; i++ )); do
    C_PARAM=$(yq e ".param_grid[$i].c_param" "$CONFIG_FILE")
    PENALTY=$(yq e ".param_grid[$i].penalty" "$CONFIG_FILE")
    SOLVER=$(yq e ".param_grid[$i].solver" "$CONFIG_FILE")

    echo "----------------------------------------"
    echo "⚙️  Experiment $((i+1)) / $GRID_LEN"
    echo "    C = $C_PARAM"
    echo "    penalty = $PENALTY"
    echo "    solver = $SOLVER"
    echo "----------------------------------------"

    docker compose run --rm -T training \
        python -m study_project_ml.pad_project_ml.modeling.train \
        --experiment-name "$EXPERIMENT_NAME" \
        --c-param "$C_PARAM" \
        --penalty "$PENALTY" \
        --solver "$SOLVER"

    echo "✅ Experiment $((i+1)) done"
    echo
done

echo "🎉 All experiments completed!"