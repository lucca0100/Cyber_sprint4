from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime, timedelta
import bcrypt, jwt

app = FastAPI(title="PySec Minimal")

SECRET = "change-me-please"  # use variável de ambiente em produção

class RegisterReq(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)

_db = {}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/auth/register", status_code=201)
def register(req: RegisterReq):
    if req.email in _db:
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    _db[req.email] = bcrypt.hashpw(req.password.encode(), bcrypt.gensalt()).decode()
    return {}

@app.post("/auth/login")
def login(req: RegisterReq):
    hash_ = _db.get(req.email)
    if not hash_ or not bcrypt.checkpw(req.password.encode(), hash_.encode()):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    exp = datetime.utcnow() + timedelta(minutes=15)
    token = jwt.encode({"sub": req.email, "exp": exp}, SECRET, algorithm="HS256")
    return {"token": token}
