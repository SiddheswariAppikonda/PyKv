from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext

from auth_service.database import (
    create_users_table,
    add_user,
    get_user,
    get_all_users
)

# --------------------
# Password hashing
# --------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

# --------------------
# Pydantic model
# --------------------
class AuthRequest(BaseModel):
    username: str
    password: str

# --------------------
# FastAPI app
# --------------------
app = FastAPI(title="PyKV Auth Service")

# --------------------
# CORS
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# DB init
# --------------------
create_users_table()

# --------------------
# Routes
# --------------------
@app.post("/signup", status_code=201)
async def signup(req: AuthRequest):
    if get_user(req.username):
        raise HTTPException(status_code=409, detail="Username already exists")

    hashed_pwd = hash_password(req.password)
    add_user(req.username, hashed_pwd)

    return {"message": "Account created successfully"}

@app.post("/login")
async def login(req: AuthRequest):
    user = get_user(req.username)

    if not user or not verify_password(req.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}

@app.get("/all-users")
def all_users():
    return get_all_users()

@app.get("/health")
async def health():
    return {"status": "ok"}
