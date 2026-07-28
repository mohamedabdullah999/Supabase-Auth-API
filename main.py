from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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


@app.post("/auth/signup")
async def signup(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return JSONResponse(status_code=400, content={"error": "Email and password are required"})

    try:
        result = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        return JSONResponse(status_code=201, content={
            "id": result.user.id,
            "email": result.user.email,
            "created_at": str(result.user.created_at)
        })
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
