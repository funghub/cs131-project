#!/bin/bash
#-e will stop at failure
set -e

BUCKET="gs://cs131-project/cs131_proj"
SCRIPT_PATH="$BUCKET/scaling.py"          # local path to .py file or gs bucket works ----
TG_INPUT_PATH="$BUCKET/biomarkers-30870-both_sexes-irnt.tsv.gz"
DB_INPUT_PATH="$BUCKET/icd10-E11-both_sexes.tsv.gz"
OUTPUT_BASE="$BUCKET/output/"
REGION="us-east1"

#create file for Runtime results ----
echo "workers,runtime_seconds" > results.csv

for n in 1 2 4; do
  CLUSTER="cs131-cluster-${n}w"

  echo "=== [${n} workers] Creating cluster ==="
  if [ "$n" -eq 1 ]; then
    gcloud dataproc clusters create $CLUSTER \
      --region=$REGION \
      --single-node \
      --master-machine-type=n1-standard-4 \
      --master-boot-disk-size=100GB
  else
    gcloud dataproc clusters create $CLUSTER \
      --region=$REGION \
      --num-workers=$n \
      --worker-machine-type=n1-standard-4 \
      --master-machine-type=n1-standard-4 \
      --master-boot-disk-size=100GB \
      --worker-boot-disk-size=100GB
  fi

  echo "=== [${n} workers] Submitting job ==="
  START=$(date +%s)

  gcloud dataproc jobs submit pyspark \
    --cluster=$CLUSTER \
    --region=$REGION \
    $SCRIPT_PATH \
    -- "$TG_INPUT_PATH" "$DB_INPUT_PATH" "${OUTPUT_BASE}run_${n}w/" \
    2>&1 | tee "job_output_${n}w.log"

  END=$(date +%s)

# Calculate runtime and write it into a csv file for timing ----
  RUNTIME=$((END-START))
  echo "${n},${RUNTIME}" >> results.csv
  echo "=== [${n} workers] Runtime: ${RUNTIME}s ==="

  echo "=== [${n} workers] Deleting cluster ==="
  gcloud dataproc clusters delete $CLUSTER --region=$REGION -q
done

echo ""
echo "=== FINAL RESULTS ==="
cat results.csv