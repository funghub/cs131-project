from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
import sys

# Set up Spark ----
spark = SparkSession.builder.appName("GWAS_Join").getOrCreate()

TG_INPUT_PATH = sys.argv[1]
DB_INPUT_PATH = sys.argv[2]
OUTPUT_PATH = sys.argv[3]

# ---- Define schema explicitly (instead of inferSchema) ----
# We only need to list the columns we actually plan to use.
# Everything else in the raw file gets dropped at read time.
tg_schema = StructType([
    StructField("chr", StringType(), True),
    StructField("pos", IntegerType(), True),
    StructField("ref", StringType(), True),
    StructField("alt", StringType(), True),
    StructField("af_meta_hq", DoubleType(), True),
    StructField("beta_meta_hq", DoubleType(), True),
    StructField("se_meta_hq", DoubleType(), True),
    StructField("neglog10_pval_meta_hq", DoubleType(), True),
    StructField("neglog10_pval_heterogeneity_hq", DoubleType(), True),
    StructField("af_meta", DoubleType(), True),
    StructField("beta_meta", DoubleType(), True),
    StructField("se_meta", DoubleType(), True),
    StructField("neglog10_pval_meta", DoubleType(), True),
    StructField("neglog10_pval_heterogeneity", DoubleType(), True),
    StructField("af_AFR", DoubleType(), True),
    StructField("af_AMR", DoubleType(), True),
    StructField("af_CSA", DoubleType(), True),
    StructField("af_EAS", DoubleType(), True),
    StructField("af_EUR", DoubleType(), True),
    StructField("af_MID", DoubleType(), True),
    StructField("beta_AFR", DoubleType(), True),
    StructField("beta_AMR", DoubleType(), True),
    StructField("beta_CSA", DoubleType(), True),
    StructField("beta_EAS", DoubleType(), True),
    StructField("beta_EUR", DoubleType(), True),
    StructField("beta_MID", DoubleType(), True),
    StructField("se_AFR", DoubleType(), True),
    StructField("se_AMR", DoubleType(), True),
    StructField("se_CSA", DoubleType(), True),
    StructField("se_EAS", DoubleType(), True),
    StructField("se_EUR", DoubleType(), True),
    StructField("se_MID", DoubleType(), True),
    StructField("neglog10_pval_AFR", DoubleType(), True),
    StructField("neglog10_pval_AMR", DoubleType(), True),
    StructField("neglog10_pval_CSA", DoubleType(), True),
    StructField("neglog10_pval_EAS", DoubleType(), True),
    StructField("neglog10_pval_EUR", DoubleType(), True),
    StructField("neglog10_pval_MID", DoubleType(), True),
    StructField("low_confidence_AFR", StringType(), True),
    StructField("low_confidence_AMR", StringType(), True),
    StructField("low_confidence_CSA", StringType(), True),
    StructField("low_confidence_EAS", StringType(), True),
    StructField("low_confidence_EUR", StringType(), True),
    StructField("low_confidence_MID", StringType(), True),
])

db_schema = StructType([
    StructField("chr", StringType(), True),
    StructField("pos", IntegerType(), True),
    StructField("ref", StringType(), True),
    StructField("alt", StringType(), True),
    StructField("af_cases_meta_hq", DoubleType(), True),
    StructField("af_controls_meta_hq", DoubleType(), True),
    StructField("beta_meta_hq", DoubleType(), True),
    StructField("se_meta_hq", DoubleType(), True),
    StructField("neglog10_pval_meta_hq", DoubleType(), True),
    StructField("neglog10_pval_heterogeneity_hq", DoubleType(), True),
    StructField("af_cases_meta", DoubleType(), True),
    StructField("af_controls_meta", DoubleType(), True),
    StructField("beta_meta", DoubleType(), True),
    StructField("se_meta", DoubleType(), True),
    StructField("neglog10_pval_meta", DoubleType(), True),
    StructField("neglog10_pval_heterogeneity", DoubleType(), True),
    StructField("af_cases_AFR", DoubleType(), True),
    StructField("af_cases_CSA", DoubleType(), True),
    StructField("af_cases_EAS", DoubleType(), True),
    StructField("af_cases_EUR", DoubleType(), True),
    StructField("af_cases_MID", DoubleType(), True),
    StructField("af_controls_AFR", DoubleType(), True),
    StructField("af_controls_CSA", DoubleType(), True),
    StructField("af_controls_EAS", DoubleType(), True),
    StructField("af_controls_EUR", DoubleType(), True),
    StructField("af_controls_MID", DoubleType(), True),
    StructField("beta_AFR", DoubleType(), True),
    StructField("beta_CSA", DoubleType(), True),
    StructField("beta_EAS", DoubleType(), True),
    StructField("beta_EUR", DoubleType(), True),
    StructField("beta_MID", DoubleType(), True),
    StructField("se_AFR", DoubleType(), True),
    StructField("se_CSA", DoubleType(), True),
    StructField("se_EAS", DoubleType(), True),
    StructField("se_EUR", DoubleType(), True),
    StructField("se_MID", DoubleType(), True),
    StructField("neglog10_pval_AFR", DoubleType(), True),
    StructField("neglog10_pval_CSA", DoubleType(), True),
    StructField("neglog10_pval_EAS", DoubleType(), True),
    StructField("neglog10_pval_EUR", DoubleType(), True),
    StructField("neglog10_pval_MID", DoubleType(), True),
    StructField("low_confidence_AFR", StringType(), True),
    StructField("low_confidence_CSA", StringType(), True),
    StructField("low_confidence_EAS", StringType(), True),
    StructField("low_confidence_EUR", StringType(), True),
    StructField("low_confidence_MID", StringType(), True),
])

# Read data from TSV.gz file (schema replaces inferSchema) ----
tg_df = (spark.read
         .format("csv")
         .option("compression", "gzip")
         .option("sep", "\t")
         .option("enforceSchema", "false")
         .schema(tg_schema)
         .option("header", "true")
         .csv(TG_INPUT_PATH))

db_df = (spark.read
         .format("csv")
         .option("compression", "gzip")
         .option("sep", "\t")
         .option("enforceSchema", "false")
         .schema(db_schema)
         .option("header", "true")
         .csv(DB_INPUT_PATH))

# Check if columns look right
# print("\nCheck columns structure:")
tg_df.printSchema()

# Select the columns we want to look at ----
tg_selected = tg_df.select("chr", "pos", "ref", "alt", "beta_CSA", "se_CSA", "beta_EUR", "se_EUR",
               "neglog10_pval_EUR", "neglog10_pval_heterogeneity_hq",
               "low_confidence_CSA", "low_confidence_EUR")
db_selected = db_df.select("chr", "pos", "ref", "alt", "beta_CSA", "se_CSA", "beta_EUR", "se_EUR",
               "neglog10_pval_EUR", "neglog10_pval_heterogeneity_hq",
               "low_confidence_CSA", "low_confidence_EUR")


# Drop rows missing what we need for the z-test ----
tg_clean = tg_selected.dropna(subset=["beta_CSA", "se_CSA", "beta_EUR", "se_EUR"])
db_clean = db_selected.dropna(subset=["beta_CSA", "se_CSA", "beta_EUR", "se_EUR"])

# Build a single variant key on both dataframes ----
tg_clean = tg_clean.withColumn("variant_id", F.concat_ws(":", "chr", "pos", "ref", "alt"))
db_clean = db_clean.withColumn("variant_id", F.concat_ws(":", "chr", "pos", "ref", "alt"))

# Drop variants flagged low-confidence(==false) for either population ----
tg_clean = tg_clean.filter(
    (F.col("low_confidence_CSA") == "false") & (F.col("low_confidence_EUR") == "false")
)
db_clean = db_clean.filter(
    (F.col("low_confidence_CSA") == "false") & (F.col("low_confidence_EUR") == "false")
)

# Filter to genome-wide significant triglyceride variants ----

NEGLOG10_GWAS_SIG = 7.301  # -log10(5e-8), genome-wide significance threshold from lit

tg_sig = tg_clean.filter(F.col("neglog10_pval_EUR") > NEGLOG10_GWAS_SIG)
print(f"Significant triglyceride variants: {tg_sig.count()}")
 
tg_sig.cache()

# Join triglyceride and diabetes on shared variant ----
df_joined = tg_sig.alias("t").join(
    db_clean.alias("d"), on="variant_id", how="inner"
).select(
    F.col("t.chr").alias("chr"),
    "variant_id",
    F.col("t.beta_CSA").alias("tg_beta_CSA"),
    F.col("t.se_CSA").alias("tg_se_CSA"),
    F.col("t.beta_EUR").alias("tg_beta_EUR"),
    F.col("t.se_EUR").alias("tg_se_EUR"),
    F.col("t.neglog10_pval_heterogeneity_hq").alias("tg_neglog10_pval_heterogeneity_hq"),
    F.col("d.beta_CSA").alias("db_beta_CSA"),
    F.col("d.se_CSA").alias("db_se_CSA"),
    F.col("d.beta_EUR").alias("db_beta_EUR"),
    F.col("d.se_EUR").alias("db_se_EUR"),
    F.col("d.neglog10_pval_heterogeneity_hq").alias("db_neglog10_pval_heterogeneity_hq"),
)

print(f"Joined row count: {df_joined.count()}")

# Compute the pairwise z-score for CSA vs EUR, for each trait ----
# z = (beta_CSA - beta_EUR) / sqrt(se_CSA^2 + se_EUR^2)
df_joined = df_joined.withColumn(
    "z_triglyceride",
    (F.col("tg_beta_CSA") - F.col("tg_beta_EUR")) /
    F.sqrt(F.col("tg_se_CSA")**2 + F.col("tg_se_EUR")**2)
).withColumn(
    "z_diabetes",
    (F.col("db_beta_CSA") - F.col("db_beta_EUR")) /
    F.sqrt(F.col("db_se_CSA")**2 + F.col("db_se_EUR")**2)
).withColumn(
    "significant_triglyceride",  # |z| > 1.96 -> significant at alpha = 0.05
    F.abs(F.col("z_triglyceride")) > 1.96
).withColumn(
    "significant_diabetes",
    F.abs(F.col("z_diabetes")) > 1.96
)
 
df_joined.cache()

print("\nCheck first 5 rows of z-scores:")
df_joined.select("variant_id", "z_triglyceride", "z_diabetes").show(5)
 
# Aggregate by chromosome for the heatmap ----
# Includes our own CSA-vs-EUR z-scores AND Pan-UKBB's own heterogeneity_hq
# test, as a cross-check: for diabetes specifically, if pops_pass_qc is
# only CSA+EUR, their heterogeneity_hq is essentially the same as our calculation (it is a double check)
by_chr = df_joined.groupBy("chr").agg(
    F.avg(F.abs(F.col("z_triglyceride"))).alias("mean_abs_z_triglyceride"),
    F.avg(F.abs(F.col("z_diabetes"))).alias("mean_abs_z_diabetes"),
    F.avg(F.col("tg_neglog10_pval_heterogeneity_hq")).alias("mean_tg_heterogeneity_hq"),
    F.avg(F.col("db_neglog10_pval_heterogeneity_hq")).alias("mean_db_heterogeneity_hq"),
    F.count("variant_id").alias("num_variants"),
)
 
print("\nCheck chromosome-level aggregation:")
by_chr.show(25)
 
# ---- Write results to GCS ----
df_joined.write.mode("overwrite").option("header", "true").csv(OUTPUT_PATH + "variant_level_zscores")
by_chr.write.mode("overwrite").option("header", "true").csv(OUTPUT_PATH + "chromosome_heatmap_data")
 
spark.stop()
