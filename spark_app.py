from pyspark.sql import SparkSession
from pyspark.sql.functions import get_json_object, explode, split, col
from pyspark.sql.column import Column

HOST = "127.0.0.1"
PORT = 9090

spark = SparkSession.builder.appName("Coinbase Stream Reader").getOrCreate()

stream = spark.readStream.format("socket") \
    .option("host", HOST) \
    .option("port", PORT) \
    .option("delimiter", "/n") \
    .load()

# Extract values from the JSON objects in the stream
df = stream.select(
    get_json_object(stream.value, "$.type").alias("type"), 
    get_json_object(stream.value, "$.product_id").alias("product_id"),
    get_json_object(stream.value, "$.changes").alias("changes"),
    get_json_object(stream.value, "$.time").alias("time")
)

# # Split the "changes" column into three separate columns
# df = df.withColumn("change_type", col("changes")[0])
# df = df.withColumn("change_price", col("changes")[1])
# df = df.withColumn("change_percentage", col("changes")[2])

# # Drop the original "changes" column
# df = df.drop("changes")

query = df.writeStream.outputMode("append") \
    .option("truncate", False) \
    .format("console")\
    .start()\
    .awaitTermination()