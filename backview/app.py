from fastapi import FastAPI
# import uvicorn
import findspark
from pyspark.sql import SparkSession

from dotenv import load_dotenv
import os

os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-17-openjdk-amd64"

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

spark = SparkSession.builder.appName("PySpark Mysql Connection").config("spark.jars", "/tmp/mysql-connector-java-8.0.23.jar").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

url = "jdbc:mysql://mysql:3306/file_handle"

mysql_properties = {
    "user": "root",
    "password": "root",
    "driver": "com.mysql.cj.jdbc.Driver"
}

table_name = "data"

df = spark.read.jdbc(url,table_name,properties=mysql_properties)

@app.get("/")
def read_root():
    print("Hello World")
    return {"Hello": "Ayush Tickoo"}

@app.get("/demo1")
def get_demo():
    return {"Hello": "DEMO"}


# if __name__ == "__main__":
#     print("Starting server...")
#     port = os.getenv("PORT")  # Get the port from the environment file
#     # print(f"Running on port {port}")
    # uvicorn.run(app, host="127.0.0.1", port=int(port))  # Run the server
    # uvicorn.run(app)

print('-------------------------------------- app.py ')

print("============================================ Started server ============================================")