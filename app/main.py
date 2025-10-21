from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime, timedelta
import bcrypt, jwt

app = FastAPI(title="PySec Minimal")

# Em produção use variável de ambiente (ex.: os.environ["JWT_SECRET"])
SECRET = "change-me-please"

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

# --------------------------
# LGPD / RBAC DEMONSTRATION
# --------------------------

# RBAC simples por header (apenas para evidência didática)
def get_role(x_role: str | None = None):
    # Ex.: enviar X-Role: admin nos testes/demonstração
    return x_role or "user"

@app.delete("/me")
def delete_me(role: str = Depends(get_role)):
    # Em um sistema real, identificaria o usuário pelo JWT (sub)
    if role not in ("user", "admin"):
        raise HTTPException(status_code=403, detail="forbidden")
    # Aqui você apagaria os dados do usuário no banco (ex.: _db.pop(...))
    return {"status": "deleted"}

@app.get("/me/export")
def export_me(role: str = Depends(get_role)):
    if role not in ("user", "admin"):
        raise HTTPException(status_code=403, detail="forbidden")
    # Em um sistema real, retornaria os dados do usuário
    return {"email": "demo@example.com", "exported_at": datetime.utcnow().isoformat()}

# Observações para o relatório:
# - Minimização de dados: somente email e senha nos DTOs.
# - Senhas com hash (bcrypt) e JWT com expiração curta (15 min).
# - Em produção: HTTPS obrigatório e SECRET via variável de ambiente.
