"""
API FastAPI Simples para Classificação de Qualidade de Vinhos

Siga o notebook Atividade_API_ML.ipynb para completar!
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
import joblib
from datetime import datetime
from pathlib import Path
import numpy as np

# ========== CRIAR APP ==========

app = FastAPI(
    title="Wine Quality API",
    description="API simples para classificar qualidade de vinhos",
    version="1.0.0"
)

# ========== MODELOS DE DADOS ==========

class WineInput(BaseModel):
    """Dados do vinho para fazer predição"""
    fixed_acidity: float = Field(..., description="Acidez fixa")
    volatile_acidity: float = Field(..., description="Acidez volátil")
    citric_acid: float = Field(..., description="Ácido cítrico")
    residual_sugar: float = Field(..., description="Açúcar residual")
    chlorides: float = Field(..., description="Cloretos")
    free_sulfur_dioxide: float = Field(..., description="Dióxido de enxofre livre")
    total_sulfur_dioxide: float = Field(..., description="Dióxido de enxofre total")
    density: float = Field(..., description="Densidade")
    pH: float = Field(..., description="pH")
    sulphates: float = Field(..., description="Sulfatos")
    alcohol: float = Field(..., description="Teor alcoólico")
    
    class Config:
        schema_extra = {
            "example": {
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
            }
        }

class PredictionOutput(BaseModel):
    """Resultado da predição"""
    quality: str
    confidence: float
    probabilities: Dict[str, float]
    timestamp: str

# ========== VARIÁVEIS GLOBAIS ==========

model = None
model_loaded = False
total_predictions = 0

# ========== CARREGAR MODELO ==========

@app.on_event("startup")
async def load_model():
    """Carregar modelo na inicialização"""
    global model, model_loaded
    
    try:
        model_path = Path("models/wine_model.pkl")
        
        if model_path.exists():
            model = joblib.load(model_path)
            model_loaded = True
            print("✓ Modelo carregado com sucesso!")
        else:
            print("⚠ Modelo não encontrado. Execute: python scripts/train_model.py")
            
    except Exception as e:
        print(f"✗ Erro ao carregar modelo: {e}")

# ========== ENDPOINTS ==========

# TODO: PASSO 1 - Criar endpoint raiz GET /
# @app.get("/")
# def home():
#     """Página inicial da API"""
#     return {
#         # Retornar: message, version, endpoints
#     }


# TODO: PASSO 2 - Criar endpoint de health check GET /health
# @app.get("/health")
# def health_check():
#     """Verificar status da API"""
#     return {
#         # Retornar: status, model_loaded, total_predictions, timestamp
#     }


# TODO: PASSO 3 - Criar endpoint de predição POST /predict
# @app.post("/predict", response_model=PredictionOutput)
# def predict_quality(wine: WineInput):
#     """
#     Fazer predição da qualidade do vinho
#     
#     Retorna: Ruim, Médio ou Bom
#     """
#     global total_predictions
#     
#     # 1. Verificar se modelo está carregado
#     
#     # 2. Preparar dados (array numpy com 11 features)
#     
#     # 3. Fazer predição (predict e predict_proba)
#     
#     # 4. Converter ID para nome (0: Ruim, 1: Médio, 2: Bom)
#     
#     # 5. Calcular confiança (max das probabilidades)
#     
#     # 6. Criar dicionário de probabilidades
#     
#     # 7. Incrementar contador
#     
#     # 8. Retornar PredictionOutput


# TODO: PASSO 4 - Criar endpoint de estatísticas GET /stats
# @app.get("/stats")
# def get_stats():
#     """Ver estatísticas da API"""
#     return {
#         # Retornar: total_predictions, model_loaded, status
#     }


# ============================================================
# INSTRUÇÕES:
# ============================================================
# 
# ATENÇÃO: Complete APENAS os 4 endpoints acima!
# Todo o resto do código já está pronto.
# 
# 1. Siga o notebook Atividade_API_ML.ipynb
# 2. Complete cada TODO (PASSO 1 a 4)
# 3. Teste cada endpoint conforme avança
# 4. Use main_completo.py como referência se travar
# 
# Para testar:
# uvicorn api.main_template:app --reload
# 
# Acesse: http://localhost:8000/docs
# ============================================================
