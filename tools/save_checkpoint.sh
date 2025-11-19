#!/bin/bash

# Script de sauvegarde du projet uubereats-poc
# Crée une archive .tar.gz propre sans .venv, __pycache__, .git, etc.

DATE=$(date +"%Y-%m-%d_%H-%M-%S")
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CHECKPOINT_DIR="${PROJECT_DIR}/../checkpoints"

mkdir -p "$CHECKPOINT_DIR"

tar --exclude=".venv" \
    --exclude="__pycache__" \
    --exclude=".git" \
    -czf "$CHECKPOINT_DIR/uubereats-poc-$DATE.tar.gz" \
    -C "$(dirname "$PROJECT_DIR")" "$(basename "$PROJECT_DIR")"

echo "✅ Checkpoint créé : $CHECKPOINT_DIR/uubereats-poc-$DATE.tar.gz"

