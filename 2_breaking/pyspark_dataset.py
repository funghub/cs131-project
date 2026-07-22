from pyspark.sql import SparkSession
import sys

# Create a SparkSession
spark = SparkSession.builder.appName("SparkTriglcerideDataset").getOrCreate()

# arguments passed in from the command line
input_path  = sys.argv[1]

# Read data from TSV.gz file
df = (spark.read
      .format("csv")
      .option("compression","gzip")
      .option("sep", "\t")
      .option("inferSchema", "true") # Infer schema (data types)
      .option("header", "true") # special row to put header to tell what data
      .csv(input_path))

# Check if columns look right
# print("\nCheck columns structure:")
# df.printSchema()

# Show first 5 rows
# print("\nCheck column names:")
# df.show(5)

# Select the Columns we want to look
df_selected =  df.select('beta_CSA','beta_EUR','se_CSA','se_EUR')

# Display 1st 5 lines
#print("\nCheck first 5 rows:")
#df_selected.show(5)

print("Counting NAbeta_CSA")
NAbeta_CSA = df_selected.where(df_selected.beta_CSA=="NA").count()
print("Counting NAbeta_EUR")
NAbeta_EUR = df_selected.where(df_selected.beta_EUR=="NA").count()
print("Counting NAse_CSA")
NAse_CSA = df_selected.where(df_selected.se_CSA=="NA").count()
print("Counting NAse_EUR")
NAse_EUR = df_selected.where(df_selected.se_EUR=="NA").count()

print(f'''
      beta_CSA = {NAbeta_CSA}
      beta_EUR = {NAbeta_EUR}
      se_CSA = {NAse_CSA}
      se_EUR = {NAse_EUR}
      ''')
