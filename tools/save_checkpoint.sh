#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: ./save_checkpoint <nom>"
  exit 1
fi

NAME=$1
DATE=$(date +"%Y-%m-%d %H:%M")

echo "## Checkpoint - $DATE" >> docs/progression.md
echo "- $NAME" >> docs/progression.md
echo "" >> docs/progression.md

git add .
git commit -m "Checkpoint: $NAME"
git tag "cp-$NAME"

echo "Checkpoint '$NAME' créé avec succès."
