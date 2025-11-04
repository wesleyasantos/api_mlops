"""
API FastAPI Simples para Classificação de Qualidade de Vinhos
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
