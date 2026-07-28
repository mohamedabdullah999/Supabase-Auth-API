from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client, Client
import os


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    print("Server running and connected to Supabase")
