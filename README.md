# PySec Minimal (FastAPI)

## Rodar local
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
bash scripts/run.sh  # (Windows: uvicorn app.main:app --port 8080 --reload)
```

## Testes
```bash
pytest -q
```

## CI (GitHub Actions)
- Roda testes
- **Bandit** (SAST) – falha em Médio/Alto
- **Safety** (SCA) – falha em vulneráveis

Abra um PR e veja o job **test-and-scan**.
