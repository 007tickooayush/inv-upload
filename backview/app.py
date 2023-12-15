from fastapi import FastAPI
from fastapi.responses import FileResponse

# import uvicorn
import findspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, BinaryType, TimestampType

from dotenv import load_dotenv
import os

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

spark = SparkSession.builder.appName("PySpark Mysql Connection").config("spark.jars",
                                                                        "/tmp/mysql-connector-java-8.0.23.jar").getOrCreate()

from pyspark.sql.functions import *

spark.sparkContext.setLogLevel("ERROR")

url = "jdbc:mysql://mysql:3306/file_handle"

mysql_properties = {
    "user": "root",
    "password": "root",
    "driver": "com.mysql.cj.jdbc.Driver"
}

table_name = "data"

table_schema = StructType([
    StructField("id", IntegerType()),
    StructField("vid_id", StringType()),
    StructField("filename", StringType()),
    StructField("size", IntegerType()),
    StructField("type", StringType()),
    StructField("file", BinaryType()),
    StructField("createdAt", TimestampType()),
    StructField("updatedAt", TimestampType())
])


@app.get("/")
def read_root():
    # print(df.head(2))
    return {"Hello": "Ayush Tickoo"}


@app.get("/demo1")
def get_demo():
    return {"Hello": "DEMO"}


@app.get("/download-spark/{uuid}")
async def get_files(uuid:str):
    filtered_df = spark.read.jdbc(url, table_name, properties=mysql_properties).where(col("vid_id") == uuid)
    json_list = filtered_df.toJSON().collect()[0] # select(col("file"),col("type")).toJSON()
    return json_list

# @app.get("/download-spark/{uuid}")
# async def get_files(uuid: str):
#     filtered_df = spark.read.jdbc(url, table_name, properties=mysql_properties).where(col("vid_id") == uuid)
#     selected_df = filtered_df.select(col("file"), col("type"),col("filename"))
#     file_bytes = selected_df.collect()[0]["file"]
#     file_type = selected_df.collect()[0]["type"]
#     file_path = selected_df.collect()[0]["filename"]
#     with open(file_path) as f:
#         f.write(file_bytes)
#
#     return FileResponse(file_path, media_type=file_type)


print('-------------------------------------- app.py ')

print("============================================ Started server ============================================")
