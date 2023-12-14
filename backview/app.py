from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

@app.get("/")
def read_root():
    print("Hello World")
    return {"Hello": "Ayush Tickoo"}

@app.get("/demo")
def get_demo():
    return {"Hello": "DEMO"}


# if __name__ == "__main__":
#     print("Starting server...")
#     port = os.getenv("PORT")  # Get the port from the environment file
#     # print(f"Running on port {port}")
    # uvicorn.run(app, host="127.0.0.1", port=int(port))  # Run the server
    # uvicorn.run(app)

print('-------------------------------------- DEMO --------------------------------------')

print("============================================ Starting server...")