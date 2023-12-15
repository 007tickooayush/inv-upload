# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /backview

# Copy the requirements file into the container
COPY requirements.txt /backview/

# Install mysql-connector-java for pyspark
RUN apt-get update && apt-get install -y default-jre
RUN apt-get update && apt-get install -y curl
RUN curl -L -o /tmp/mysql-connector-java-8.0.23.jar https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.23/mysql-connector-java-8.0.23.jar

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
# COPY . .

# Set the command to run the application
# CMD ["uvicorn", "app:app", "--reload"]
# CMD ["python", "app.py"]
EXPOSE 8000

# Run the FastAPI application using uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000","--reload"]