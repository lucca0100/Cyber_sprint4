# PySec Minimal — DevSecOps + LGPD (Python/FastAPI)
## 👥 Integrantes

- **Lucca Alexandre** — RM **99700**  
- **Victor Wittner** — RM **98667**  
- **Matheus Haruo** — RM **97663**  
- **João Saborido** — RM **98184**

---


Projeto mínimo em **Python + FastAPI** com pipeline **CI** no GitHub Actions para demonstrar **SSDLC**, **SAST**, **SCA**, **(opcional) DAST com ZAP**, proteção de branch e práticas **LGPD** (minimização de dados, hash de senhas, token com expiração e rotas do titular).

## 🔹 Objetivos
- **SSDLC Automatizado** (Testes + SAST + SCA no CI)
- **Gestão Contínua de Vulnerabilidades** (Bandit, Safety e opcional ZAP)
- **LGPD** (minimização de dados, autenticação segura, rotas do titular)

---

## Stack
- **FastAPI** (API)
- **PyJWT** (JWT com expiração)
- **bcrypt** (hash de senhas)
- **Pydantic** (validação de entrada)
- **Pytest** (testes)
- **Bandit** (SAST)
- **Safety** (SCA)
- **ZAP Baseline** (DAST – **não-bloqueante**, opcional)
- **GitHub Actions** (CI)
- **Dependabot** (atualizações automáticas de deps)

---

## Endpoints principais
- `GET /health` — healthcheck
- `POST /auth/register` — cadastro (e-mail único, senha com hash **bcrypt**)
- `POST /auth/login` — login (gera **JWT** com expiração de 15 min)
- `GET /me/export` — **LGPD**: exportação simplificada (demo)
- `DELETE /me` — **LGPD**: exclusão simplificada (demo)

> Observação: as rotas **/me** são **demonstração** (sem BD). Em produção, identifique o usuário pelo `sub` do JWT e registre auditoria/consentimento.

---

## ▶Como rodar localmente

### Windows (PowerShell)
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# testes
python -m pytest -q

# API
python -m uvicorn app.main:app --port 8080 --reload
```

### Linux/Mac
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m pytest -q
python -m uvicorn app.main:app --port 8080 --reload
```

Docs: **http://127.0.0.1:8080/docs**

---

##  CI (GitHub Actions)

Arquivo: `.github/workflows/ci.yml`

Steps (não-bloqueantes, para facilitar a entrega):
- **Install deps**
- **Start API** (para ZAP, opcional)
- **Run tests** (pytest)
- **SAST (Bandit)**
- **SCA (Safety)**
- **DAST (ZAP Baseline)** *(opcional, não-bloqueante)*

> Depois da entrega, é possível “**endurecer**” o pipeline removendo `continue-on-error: true` e `|| true`, e usando `--exit-code 1` no Safety.

---

## Práticas de segurança aplicadas
- **Validação forte** (Pydantic: `EmailStr`, senha com tamanho mínimo)
- **Autenticação segura** (hash **bcrypt** + **JWT** com expiração curta)
- **Tratamento de erros seguro** (401/409 sem vazar detalhes)
- **Normalização de finais de linha** (evita quebra em CI)
- **Proteção de branch** (merge sob status checks)

---

## LGPD (implementado no projeto)
- **Minimização**: DTOs aceitam apenas `email` e `password`.
- **Senha segura**: armazenada com hash **bcrypt**.
- **Sessão curta**: **JWT** com expiração de 15 minutos.
- **Direitos do titular (demo)**:  
  - `GET /me/export` — exporta dados mínimos (exemplo)  
  - `DELETE /me` — exclusão (exemplo)
- **Observações de produção**:
  - **HTTPS** obrigatório (TLS)
  - `SECRET` do JWT por **variável de ambiente**
  - Auditoria e consentimento (quando houver BD real)

---

## Gestão contínua de vulnerabilidades
- **SAST**: **Bandit** no CI
- **SCA**: **Safety** no CI
- **DAST (opcional)**: **ZAP Baseline** no CI contra `http://127.0.0.1:8080`
- **Dependabot**: `.github/dependabot.yml` configurado (pip, semanal)

---

##  Passo a passo (o que foi feito)
1. Criação do repositório no GitHub.
2. Inclusão do projeto mínimo (FastAPI + testes + segurança básica).
3. Setup do CI (`.github/workflows/ci.yml`) com pytest, Bandit, Safety e (opcional) ZAP.
4. Abertura de PR para rodar o CI.
5. Proteção da `main` (Settings → Branches → “Require status checks to pass”).
6. Dependabot habilitado:
   - Settings → **Code security and analysis** (Dependency graph / Alerts / Security updates **ON**)
   - `.github/dependabot.yml` na **branch `main`**
7. Evidências coletadas (Actions, PR verde, Swagger, Branch protection).
8. Merge do PR.

---

## Como testar (via Swagger)

- **/auth/register**
  ```json
  {"email": "teste@example.com", "password": "segura123"}
  ```
  Esperado: 201 `{}` (ou 409 se já existir)

- **/auth/login**
  ```json
  {"email": "teste@example.com", "password": "segura123"}
  ```
  Esperado: 200 `{"token": "<jwt>"}`

- **/me/export** → 200 `{"email":"...", "exported_at":"..."}`  
- **/me** (DELETE) → 200 `{"status":"deleted"}`  
- **Erro controlado (opcional)**: `/auth/login` com senha errada → 401

---

## Evidências (onde colocar os prints)
Pasta `docs/img/` (exemplos):
- PR com checks (verde)
- Actions (run do job com steps — e ZAP, se aplicável)
- Branch Protection (Settings → Branches)
- Swagger:
  - 201/409 do register  
  - 200 do login (token)  
  - 200 do `/me/export`  
  - 200 do `/me` (delete)  
  - (opcional) 401 do login errado
- dependabot.yml (arquivo) + Settings → Code security and analysis

Sugestão:
- `docs/RELATORIO_SSDLC.md`: PR/Actions/Branch + Swagger de auth (+ 401)
- `docs/PLANO_GERENCIAMENTO_VULNS.md`: Bandit/Safety/(ZAP), Security & Analysis, dependabot.yml
- `docs/PLANO_LGPD.md`: Swagger `/me` e `/me/export`, print do código (bcrypt + JWT + Pydantic), nota de HTTPS/SECRET



## Depois da entrega (opcional — modo rigor)
- Remover `continue-on-error` e `|| true` do CI.
- No **Safety**, usar `--exit-code 1`.
- Exigir **Pull Request** e **1 review** na proteção de branch.
- Usar **SECRET** do JWT via variável de ambiente.
- Adicionar **DB real** + auditoria e consentimento (LGPD).
