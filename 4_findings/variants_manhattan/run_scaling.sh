#!/bin/bash
# run_scaling.sh — run the same Spark job at 2, 3, and 4 executors
#based on spark demo 2

set -euo pipefail

# change this to your bucket where you store the data
BUCKET=gs://cs131_proj

TG_INPUT=$BUCKET/biomarkers-30870-both_sexes-irnt.tsv.gz
DB_INPUT=$BUCKET/icd10-E11-both_sexes.tsv.gz

# SCRIPT=$BUCKET/scripts/scaling.py

# change this to the script on your local
#SCRIPT=./scaling.py
#SCRIPT=./extract_data_pval.py
SCRIPT=./extract_data_neglog.py

#OUTPUT_LOG_CLOUD=./$BUCKET/output/log.txt
OUTPUT_LOG_LOCAL=./output/log.txt

TIMING_LOG=./output/timing.txt 

#for N in 2 3 4; do
for N in 2; do
  echo "=== Submitting batch with $N executor(s) ===" | tee -a "$TIMING_LOG"

  START=$(date +%s)
  gcloud dataproc batches submit pyspark "$SCRIPT" \
    --region=us-central1 \
    --deps-bucket="$BUCKET" \
    --properties=spark.dynamicAllocation.enabled=false,spark.executor.instances="$N" \
    -- "$TG_INPUT" "$DB_INPUT" "$BUCKET/output/exec$N/" &> "$OUTPUT_LOG_LOCAL"
  END=$(date +%s)

  ELAPSED=$((END - START))
  echo "exec$N: ${ELAPSED}s" | tee -a "$TIMING_LOG"

  if [ "$N" -ne 4 ]; then
    echo "=== Waiting 120s for machines to release ===" | tee -a "$TIMING_LOG"
    sleep 120
  fi
done

echo "all runs done"
