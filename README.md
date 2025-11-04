# Início Rápido - Aula 12: API ML

---

## IMPORTANTE: Ordem Correta!

**SEMPRE treine o modelo ANTES de buildar o Docker!**

---

## Passo 1: Navegar para o projeto

```bash
cd "Aula 12/projeto-api-ml"
```

---

## Passo 2: Treinar o modelo (5 min) - OBRIGATÓRIO PRIMEIRO!

```bash
# Instalar dependências
pip install scikit-learn pandas joblib numpy

# Treinar modelo
python scripts/train_model.py
```

**✅ Verifique que foi criado:**
```bash
ls -la models/
ls -la data/
```

Você deve ver:
- `models/wine_model.pkl`
- `data/wine_data.csv`
- `data/example_request.json`

** NÃO prossiga sem esses arquivos!**

---

## Passo 3: Build Docker (3 min)

```bash
docker build -t wine-api .
```

**Tempo:** 3-5 minutos (primeira vez)

---

## Passo 4: Subir API (1 min)

```bash
docker compose up -d
```

**Aguarde ~10 segundos** para a API inicializar.

---

## Passo 5: Verificar (1 min)

```bash
# Health check
curl http://localhost:8000/health
```

**Resposta esperada:**
```json
{
  "status": "online",
  "model_loaded": true,
  "total_predictions": 0,
  "timestamp": "2024-..."
}
```

**Se `model_loaded: false`** = modelo não foi treinado! Volte ao Passo 2!

---

## Passo 6: Testar no Navegador (5 min)

Abra: **http://localhost:8000/docs**

1. Clique em `POST /predict`
2. Clique em "Try it out"
3. Clique em "Execute"
4. Veja o resultado!

---

## Passo 7: Fazer Predição (2 min)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "fixed_acidity": 7.0,
    "volatile_acidity": 0.3,
    "citric_acid": 0.5,
    "residual_sugar": 2.0,
    "chlorides": 0.05,
    "free_sulfur_dioxide": 30.0,
    "total_sulfur_dioxide": 100.0,
    "density": 0.995,
    "pH": 3.2,
    "sulphates": 0.6,
    "alcohol": 13.0
  }'
```

---

## Passo 8: Executar Testes (3 min)

```bash
pip install requests
python tests/test_api.py
```

---

## 📋 Checklist Rápido

- [ ] Treinei o modelo (`train_model.py`)
- [ ] Verifiquei que `models/wine_model.pkl` existe
- [ ] Fiz build do Docker
- [ ] Subi a API
- [ ] Testei `/health` e `model_loaded: true`
- [ ] Acessei o Swagger UI
- [ ] Fiz pelo menos 1 predição

---

## 🚨 Problemas Comuns

### 1. "model_loaded": false

**Causa:** Modelo não foi treinado ou não está na pasta correta

**Solução:**
```bash
# Treinar modelo
python scripts/train_model.py

# Verificar
ls -la models/wine_model.pkl

# Reiniciar API
docker compose restart
```

### 2. Erro no Docker Build

**Causa:** Tentou buildar antes de treinar

**Solução:**
```bash
# 1. Treinar PRIMEIRO
python scripts/train_model.py

# 2. Depois buildar
docker build -t wine-api .
```

### 3. "COPY models/ failed"

**Causa:** Pasta models/ não existe ou está vazia

**Solução:**
```bash
# Criar pasta
mkdir -p models data

# Treinar
python scripts/train_model.py

# Rebuild
docker build -t wine-api --no-cache .
```

### 4. API não responde

```bash
# Ver logs
docker compose logs -f

# Verificar containers
docker compose ps

# Reiniciar
docker compose restart
```

---

## 🎯 Resumo da Ordem Correta

```bash
# 1️⃣ SEMPRE PRIMEIRO - Treinar
python scripts/train_model.py

# 2️⃣ Verificar arquivos
ls -la models/ data/

# 3️⃣ Build Docker
docker build -t wine-api .

# 4️⃣ Subir API
docker compose up -d

# 5️⃣ Testar
curl http://localhost:8000/health
open http://localhost:8000/docs
```

---

## 📊 URLs Importantes

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **Health:** http://localhost:8000/health
- **Stats:** http://localhost:8000/stats

---

## 🔧 Comandos Úteis

```bash
# Ver logs
docker compose logs -f

# Parar
docker compose down

# Rebuild completo
docker compose down
docker build -t wine-api --no-cache .
docker compose up -d

# Retreinar modelo
python scripts/train_model.py
docker compose restart
```

---

## ✅ Tudo Funcionando?

Se você conseguiu:
- ✅ Treinar o modelo
- ✅ Subir a API
- ✅ Ver `model_loaded: true`
- ✅ Fazer uma predição

