from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from supabase import create_client, Client
import os

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

security = HTTPBearer(auto_error=False)


@app.on_event("startup")
async def startup_event():
    print("Server running and connected to Supabase")


async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Access token required")

    token = credentials.credentials

    try:
        user_response = supabase.auth.get_user(token)
        return user_response.user, token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


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


@app.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return JSONResponse(status_code=400, content={"error": "Email and password are required"})

    try:
        result = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return JSONResponse(status_code=200, content={
            "access_token": result.session.access_token,
            "refresh_token": result.session.refresh_token
        })
    except Exception as e:
        return JSONResponse(status_code=401, content={"error": "Invalid login credentials"})


@app.get("/public/info")
async def public_info():
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
async def protected_profile(user_and_token: tuple = Depends(verify_token)):
    user, token = user_and_token
    return {
        "id": user.id,
        "email": user.email,
        "created_at": str(user.created_at)
    }


@app.get("/protected/dashboard")
async def protected_dashboard(user_and_token: tuple = Depends(verify_token)):
    user, token = user_and_token
    return {
        "message": f"Welcome to your dashboard, {user.email}"
    }


@app.post("/auth/logout")
async def logout(user_and_token: tuple = Depends(verify_token)):
    user, token = user_and_token

    try:
        supabase.auth.sign_out()
        return JSONResponse(status_code=204, content=None)
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})