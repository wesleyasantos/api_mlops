"""
Script Simples para Treinar Modelo de Classificação de Vinhos
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import json
import os

print("=" * 60)
print("TREINAMENTO DO MODELO DE VINHOS")
print("=" * 60)

# Criar pastas
os.makedirs('models', exist_ok=True)
os.makedirs('data', exist_ok=True)

# Passo 1: Criar dataset
print("\n[1/4] Criando dataset de vinhos...")
np.random.seed(42)

# 500 vinhos com 11 características
data = {
    'fixed_acidity': np.random.uniform(4, 15, 500),
    'volatile_acidity': np.random.uniform(0.1, 1.5, 500),
    'citric_acid': np.random.uniform(0, 1, 500),
    'residual_sugar': np.random.uniform(1, 15, 500),
    'chlorides': np.random.uniform(0.01, 0.5, 500),
    'free_sulfur_dioxide': np.random.uniform(1, 70, 500),
    'total_sulfur_dioxide': np.random.uniform(6, 250, 500),
    'density': np.random.uniform(0.99, 1.01, 500),
    'pH': np.random.uniform(2.7, 4.0, 500),
    'sulphates': np.random.uniform(0.3, 2.0, 500),
    'alcohol': np.random.uniform(8, 14, 500),
}

df = pd.DataFrame(data)

# Criar qualidade (0=Ruim, 1=Médio, 2=Bom)
df['quality'] = 0
df.loc[(df['alcohol'] > 10) & (df['volatile_acidity'] < 0.6), 'quality'] = 1
df.loc[(df['alcohol'] > 12) & (df['volatile_acidity'] < 0.4), 'quality'] = 2

# Salvar dataset
df.to_csv('data/wine_data.csv', index=False)
print(f"   ✓ Dataset criado: {len(df)} vinhos")
print(f"   ✓ Distribuição:")
print(f"      Ruim: {(df['quality']==0).sum()}")
print(f"      Médio: {(df['quality']==1).sum()}")
print(f"      Bom: {(df['quality']==2).sum()}")

# Passo 2: Separar dados
print("\n[2/4] Separando dados...")
X = df.drop('quality', axis=1)
y = df['quality']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"   ✓ Treino: {len(X_train)} vinhos")
print(f"   ✓ Teste: {len(X_test)} vinhos")

# Passo 3: Treinar modelo
print("\n[3/4] Treinando modelo...")
model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_train, y_train)

# Avaliar
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"   ✓ Modelo treinado!")
print(f"   ✓ Acurácia: {accuracy:.2%}")

# Passo 4: Salvar modelo
print("\n[4/4] Salvando modelo...")
joblib.dump(model, 'models/wine_model.pkl')
print("   ✓ Modelo salvo em: models/wine_model.pkl")

# Salvar exemplo
example = {
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

with open('data/example_request.json', 'w') as f:
    json.dump(example, f, indent=2)

print("   ✓ Exemplo salvo em: data/example_request.json")

print("\n" + "=" * 60)
print("TREINAMENTO CONCLUÍDO!")
print("=" * 60)
print("\nPróximos passos:")
print("1. Subir a API: docker compose up")
print("2. Testar: curl http://localhost:8000/health")
print("3. Acessar docs: http://localhost:8000/docs")
