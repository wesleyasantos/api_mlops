# Instruções para a Atividade: Construindo Endpoints de API ML

## Objetivo

Nesta atividade, você vai construir **apenas os 4 endpoints** de uma API FastAPI para classificação de vinhos.

**Toda a estrutura já está pronta!** Você só precisa completar a seção de endpoints.

---

## Estrutura do Projeto

```
projeto-api-ml/
├── api/
│   ├── main_template.py     ← VOCÊ VAI TRABALHAR AQUI
│   └── requirements.txt
│
├── Atividade_API_ML.ipynb   ← GUIA PASSO A PASSO (SIGA ESTE!)
└── INSTRUCOES_ATIVIDADE.md  ← Este arquivo
```

---

## O Que Já Está Pronto

Abra `api/main_template.py` e observe que JÁ estão prontos:

- ✅ **Importações** - Todas as bibliotecas necessárias
- ✅ **FastAPI App** - Aplicação criada e configurada
- ✅ **Modelos Pydantic** - `WineInput` e `PredictionOutput`
- ✅ **Variáveis Globais** - `model`, `model_loaded`, `total_predictions`
- ✅ **Função load_model()** - Carrega o modelo na inicialização

---

## O Que Você Vai Fazer

Você vai completar **apenas a seção `# ========== ENDPOINTS ==========`**:

### 4 Endpoints para construir:

1. **GET /** - Página inicial (10 min)
2. **GET /health** - Verificação de saúde (10 min)
3. **POST /predict** - Fazer predição ⭐ **PRINCIPAL** (40 min)
4. **GET /stats** - Estatísticas (5 min)


---

## Como Fazer

### Passo a Passo:

1. **Leia o notebook** `Atividade_API_ML.ipynb`
   - Ele tem instruções detalhadas para cada endpoint
   - Explicações de cada linha de código
   - Exemplos e testes

2. **Abra** `api/main_template.py`
   - Encontre a seção `# ========== ENDPOINTS ==========`
   - Você verá 4 TODOs comentados

3. **Complete cada TODO**
   - Descomente o código
   - Preencha as partes faltantes
   - Siga as instruções do notebook

4. **Teste cada passo**
   ```bash
   uvicorn api.main_template:app --reload
   ```
   - Abra: http://localhost:8000/docs
   - Teste cada endpoint no Swagger UI

5. **Se travar**, consulte `api/main.py`
   - Ele tem a solução completa
   - Compare com seu código

---

## Preparação Inicial

### 1. Instalar dependências:

```bash
cd projeto-api-ml
pip install -r api/requirements.txt
```

### 2. Treinar o modelo:

```bash
python scripts/train_model.py
```

**IMPORTANTE:** O modelo precisa estar treinado antes de começar!

Verifique:
```bash
ls -la models/wine_model.pkl
```

Deve aparecer o arquivo `wine_model.pkl`.

---

## Testando Sua API

### Durante o desenvolvimento:

```bash
uvicorn api.main_template:app --reload
```

### Testes no navegador:

- **Swagger UI:** http://localhost:8000/docs
- **GET /:** http://localhost:8000/
- **GET /health:** http://localhost:8000/health

### Teste via curl:

```bash
# Health check
curl http://localhost:8000/health

# Predição
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

## Checklist de Conclusão

Antes de considerar a atividade completa, verifique:

### Código:
- [ ] Endpoint `GET /` criado
- [ ] Endpoint `GET /health` criado
- [ ] Endpoint `POST /predict` criado (completo!)
- [ ] Endpoint `GET /stats` criado

### Testes:
- [ ] API inicia sem erros
- [ ] Console mostra "Modelo carregado com sucesso!"
- [ ] Swagger UI acessível em `/docs`
- [ ] Todos os 4 endpoints funcionam
- [ ] Predição retorna formato correto
- [ ] Contador de predições incrementa

### Entendimento:
- [ ] Entendo a diferença entre GET e POST
- [ ] Entendo como FastAPI usa decorators
- [ ] Entendo o fluxo de predição
- [ ] Entendo como validar dados com Pydantic
- [ ] Entendo como retornar erros HTTP

---

## Usando Sua API no Projeto

Após completar e testar, você pode usar sua versão:

```bash
# Backup do original
mv api/main.py api/main_backup.py

# Usar sua versão
cp api/main_template.py api/main.py

# Rodar
uvicorn api.main:app --reload

# Ou rodar no Docker
docker compose up -d
```

---

## Recursos de Ajuda

1. **Notebook:** `Atividade_API_ML.ipynb` - Guia passo a passo detalhado
2. **Solução:** `api/main_completo.py` - Código completo para consulta
3. **Documentação:** http://localhost:8000/docs - Swagger UI
4. **FastAPI Docs:** https://fastapi.tiangolo.com/

---

## Dicas

- **Não copie e cole tudo de uma vez!** Faça um endpoint por vez
- **Teste frequentemente** - Rode a API após cada endpoint
- **Leia as explicações** - O notebook explica cada linha
- **Use o Swagger UI** - É mais fácil testar por lá
- **Consulte a solução** - Não há problema em olhar quando travar

---

## Desafios Extras (Opcional)

Se terminar rápido, tente:

### Fácil:
1. Adicionar campo `"author"` no endpoint `/`
2. Adicionar validação: `alcohol > 0`
3. Mudar mensagens de erro

### Médio:
4. Adicionar endpoint `GET /version`
5. Salvar log de predições em arquivo
6. Adicionar timestamp de inicialização

### Difícil:
7. Implementar cache de predições
8. Adicionar rate limiting
9. Endpoint `POST /batch-predict` para múltiplas predições

---

## Entrega

Ao final, você deve ter:

1. ✅ Arquivo `main_template.py` completado
2. ✅ API funcionando 100%
3. ✅ Todos os 4 endpoints testados
4. ✅ Screenshots ou vídeo mostrando funcionamento

---

**Boa sorte! Você vai construir uma API ML funcional!** 🚀
