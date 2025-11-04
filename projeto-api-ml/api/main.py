"""
API FastAPI Simples para Classificação de Qualidade de Vinhos
Nível: Fácil-Intermediário
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

@app.get("/")
def home():
    """Página inicial da API"""
    return {
        "message": "Wine Quality Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "predict": "/predict (POST)"
        }
    }

@app.get("/health")
def health_check():
    """Verificar status da API"""
    return {
        "status": "online",
        "model_loaded": model_loaded,
        "total_predictions": total_predictions,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict", response_model=PredictionOutput)
def predict_quality(wine: WineInput):
    """
    Fazer predição da qualidade do vinho
    
    Retorna: Ruim, Médio ou Bom
    """
    global total_predictions
    
    # Verificar se modelo está carregado
    if not model_loaded:
        raise HTTPException(
            status_code=503, 
            detail="Modelo não está carregado. Treine o modelo primeiro."
        )
    
    try:
        # Preparar dados para predição
        features = np.array([[
            wine.fixed_acidity,
            wine.volatile_acidity,
            wine.citric_acid,
            wine.residual_sugar,
            wine.chlorides,
            wine.free_sulfur_dioxide,
            wine.total_sulfur_dioxide,
            wine.density,
            wine.pH,
            wine.sulphates,
            wine.alcohol
        ]])
        
        # Fazer predição
        prediction_id = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        # Converter ID para nome
        quality_names = {0: "Ruim", 1: "Médio", 2: "Bom"}
        quality = quality_names[prediction_id]
        
        # Calcular confiança
        confidence = float(max(probabilities))
        
        # Criar dicionário de probabilidades
        prob_dict = {
            "Ruim": float(probabilities[0]),
            "Médio": float(probabilities[1]),
            "Bom": float(probabilities[2])
        }
        
        # Incrementar contador
        total_predictions += 1
        
        # Retornar resultado
        return PredictionOutput(
            quality=quality,
            confidence=confidence,
            probabilities=prob_dict,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao fazer predição: {str(e)}"
        )

@app.get("/stats")
def get_stats():
    """Ver estatísticas da API"""
    return {
        "total_predictions": total_predictions,
        "model_loaded": model_loaded,
        "status": "active"
    }

# Para rodar localmente: uvicorn main:app --reload
