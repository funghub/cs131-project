#!/bin/bash
# run_scaling.sh — run the same Spark job at 2, 3, and 4 executors
#based on spark demo 2

set -euo pipefail

BUCKET=gs://cs131-501617-project
TG_INPUT=$BUCKET/biomarkers-30870-both_sexes-irnt.tsv.gz
DB_INPUT=$BUCKET/icd10-E11-both_sexes.tsv.gz
SCRIPT=$BUCKET/scripts/scaling.py

TIMING_LOG=/mnt/c/Users/Jane/Documents/cs131-project/3_scaling/scaling.txt 

for N in 2 3 4; do
  echo "=== Submitting batch with $N executor(s) ===" | tee -a "$TIMING_LOG"

  START=$(date +%s)
  gcloud dataproc batches submit pyspark "$SCRIPT" \
    --region=us-central1 \
    --deps-bucket="$BUCKET" \
    --properties=spark.dynamicAllocation.enabled=false,spark.executor.instances="$N" \
    -- "$TG_INPUT" "$DB_INPUT" "$BUCKET/output/exec$N/"
  END=$(date +%s)

  ELAPSED=$((END - START))
  echo "exec$N: ${ELAPSED}s" | tee -a "$TIMING_LOG"

  if [ "$N" -ne 4 ]; then
    echo "=== Waiting 120s for machines to release ===" | tee -a "$TIMING_LOG"
    sleep 120
  fi
done

echo "all runs done"
