from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

def main():
    # 1. Initialize SparkSession with HDFS Connectivity
    spark = SparkSession.builder \
        .appName("NASA Log Analytics Dashboard Processor") \
        .getOrCreate()
       
    spark.sparkContext.setLogLevel("ERROR")
    print("\n" + "="*50)
    print("🚀 APACHE SPARK IN-MEMORY ANALYTICS ENGINE ONLINE")
    print("="*50 + "\n")

    # Define standard Schema for our clean key-value text pairs
    schema = StructType([
        StructField("Metric_Key", StringType(), True),
        StructField("Total_Count", IntegerType(), True)
    ])

    # ---------------------------------------------------------
    # LAYER 1: HTTP Status Code Processing
    # ---------------------------------------------------------
    print("📊 [Spark Processing]: Reading Status Code Metrics...")
    status_df = spark.read.csv("/wc_output/part-r-00000", sep="\t", schema=schema)
    print("📈 HTTP Status Code Distribution Matrix:")
    status_df.orderBy(status_df["Total_Count"].desc()).show()

    # ---------------------------------------------------------
    # LAYER 2: Top Active Client IP Processing
    # ---------------------------------------------------------
    print("\n🔍 [Spark Processing]: Reading Client IP Metrics...")
    ip_df = spark.read.csv("/new_ip_output/part-r-00000", sep="\t", schema=schema)
    print("👑 Top 5 Most Active Network Client IP Addresses:")
    ip_df.orderBy(ip_df["Total_Count"].desc()).show(5)

    # ----------------------------------------------------/-----
    # LAYER 3: Most Accessed Resources Processing
    # ---------------------------------------------------------
    print("\n🌐 [Spark Processing]: Reading Page Asset Metrics...")
    page_df = spark.read.csv("/page_output/part-r-00000", sep="\t", schema=schema)
    print("📦 Top 5 Most Demanded Web URL Resources:")
    page_df.orderBy(page_df["Total_Count"].desc()).show(5)

    # ---------------------------------------------------------
    # LAYER 4: Chronological Traffic Pattern Processing
    # ---------------------------------------------------------
    print("\n⏰ [Spark Processing]: Reading Hourly Traffic Frequencies...")
    freq_df = spark.read.csv("/freq_output/part-r-00000", sep="\t", schema=schema)
    print("⏳ Sorted Chronological Hourly Workload Profile:")
    freq_df.orderBy("Metric_Key").show(24, truncate=False)

    # Stop the Session cleanly
    spark.stop()

if __name__ == "__main__":
    main()
