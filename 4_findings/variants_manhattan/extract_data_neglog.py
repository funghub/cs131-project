from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import sys

# Set up Spark ----
spark = SparkSession.builder.appName("ExtractData_Manhattan").getOrCreate()

TG_INPUT_PATH = sys.argv[1]
DB_INPUT_PATH = sys.argv[2]
OUTPUT_PATH = sys.argv[3]

tg_df = (spark.read
         .format("csv")
         .option("compression", "gzip")
         .option("sep", "\t")
         .option("inferSchema", "true")
         .option("header", "true")
         .csv(TG_INPUT_PATH))

tg_df.printSchema()

db_df = (spark.read
         .format("csv")
         .option("compression", "gzip")
         .option("sep", "\t")
         .option("inferSchema", "true")
         .option("header", "true")
         .csv(DB_INPUT_PATH))

db_df.printSchema()

# Drop variants flagged low-confidence(==false) for either population ----
tg_clean = tg_df.filter(
    (F.col("low_confidence_CSA") == "false") & (F.col("low_confidence_EUR") == "false")
)
db_clean = db_df.filter(
    (F.col("low_confidence_CSA") == "false") & (F.col("low_confidence_EUR") == "false")
)

# Add single variant key to dataframe as the SNP ID
tg_newcols = tg_clean.withColumn("variant_id", F.concat_ws(":", "chr", "pos", "ref", "alt"))
db_newcols = db_clean.withColumn("variant_id", F.concat_ws(":", "chr", "pos", "ref", "alt"))


# convert neglog10_pval_{pop} to a p-value (-log_{10}(p)=x)
#10^(neglog10_pval_EUR*(-1))
#tg_newcols = tg_newcols.withColumn("pval_EUR", (F.pow(10,-F.col("neglog10_pval_EUR"))))
#tg_newcols = tg_newcols.withColumn("pval_CSA", (F.pow(10,-F.col("neglog10_pval_CSA"))))
#db_newcols = db_newcols.withColumn("pval_EUR", (F.pow(10,-F.col("neglog10_pval_EUR"))))
#db_newcols = db_newcols.withColumn("pval_CSA", (F.pow(10,-F.col("neglog10_pval_CSA"))))


# Select the columns we want to look at ----
tg_selected = tg_newcols.select("chr", "pos", "variant_id", "neglog10_pval_EUR", "neglog10_pval_CSA")
db_selected = db_newcols.select("chr", "pos", "variant_id", "neglog10_pval_EUR", "neglog10_pval_CSA")

# ---- Write results to GCS ----
tg_selected.write.mode("overwrite").option("header", "true").csv(OUTPUT_PATH + "tg_for_manhattan_neglog")
db_selected.write.mode("overwrite").option("header", "true").csv(OUTPUT_PATH + "db_for_manhattan_neglog")


# Obtain the Top 10 pval (smallest) in each dataset for each population for each chromosome
#top10_tg_EUR = tg_selected.orderBy("pval_EUR").limit(10)
#print("Show Triglyceride Dataset EUR:")
#top10_tg_EUR.show()
#top10_tg_CSA = tg_selected.orderBy("pval_CSA").limit(10)
#print("Show Triglyceride Dataset CSA:")
#top10_tg_CSA.show()

#top10_db_EUR = db_selected.orderBy("pval_EUR").limit(10)
#print("\nShow Diabetes Dataset EUR:")
#top10_db_EUR.show()
#top10_db_CSA = db_selected.orderBy("pval_CSA").limit(10)
#print("Show Diabetes Dataset CSA:")
#top10_db_CSA.show()


# Obtain the Top 10 neglog_pval (biggest) in each dataset for each population for each chromosome
top10_tg_EUR = tg_selected.order("neglog10_pval_EUR", decreasing = TRUE).limit(5)
print("Show Triglyceride Dataset EUR:")
top10_tg_EUR.show()
top10_tg_CSA = tg_selected.order("neglog10_pval_CSA", decreasing = TRUE).limit(5)
print("Show Triglyceride Dataset CSA:")
top10_tg_CSA.show()

top10_db_EUR = db_selected.order("neglog10_pval_EUR", decreasing = TRUE).limit(5)
print("\nShow Diabetes Dataset EUR:")
top10_db_EUR.show()
top10_db_CSA = db_selected.order("neglog10_pval_CSA", decreasing = TRUE).limit(5)
print("Show Diabetes Dataset CSA:")
top10_db_CSA.show()


spark.stop()
