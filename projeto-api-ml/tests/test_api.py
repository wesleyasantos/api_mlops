"""
Testes Simples da API
"""

import requests
import json

API_URL = "http://localhost:8000"

def print_test(name):
    """Printar nome do teste"""
    print(f"\n{'='*60}")
    print(f"TESTE: {name}")
    print('='*60)

def test_1_home():
    """Teste 1: Página inicial"""
    print_test("Página Inicial")
    
    response = requests.get(f"{API_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    assert response.status_code == 200
    print("✓ Passou!")

def test_2_health():
    """Teste 2: Health check"""
    print_test("Health Check")
    
    response = requests.get(f"{API_URL}/health")
    data = response.json()
    
    print(f"Status: {data['status']}")
    print(f"Modelo carregado: {data['model_loaded']}")
    print(f"Predições feitas: {data['total_predictions']}")
    
    assert response.status_code == 200
    assert data['model_loaded'] == True, "Modelo não está carregado!"
    print("✓ Passou!")

def test_3_prediction_good():
    """Teste 3: Predição de vinho BOM"""
    print_test("Predição - Vinho Bom")
    
    wine = {
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
    
    response = requests.post(f"{API_URL}/predict", json=wine)
    data = response.json()
    
    print(f"Qualidade: {data['quality']}")
    print(f"Confiança: {data['confidence']:.2%}")
    print(f"Probabilidades:")
    for q, prob in data['probabilities'].items():
        print(f"  {q}: {prob:.2%}")
    
    assert response.status_code == 200
    print("✓ Passou!")

def test_4_prediction_bad():
    """Teste 4: Predição de vinho RUIM"""
    print_test("Predição - Vinho Ruim")
    
    wine = {
        "fixed_acidity": 10.0,
        "volatile_acidity": 1.2,
        "citric_acid": 0.1,
        "residual_sugar": 1.0,
        "chlorides": 0.3,
        "free_sulfur_dioxide": 5.0,
        "total_sulfur_dioxide": 20.0,
        "density": 1.0,
        "pH": 3.8,
        "sulphates": 0.3,
        "alcohol": 8.5
    }
    
    response = requests.post(f"{API_URL}/predict", json=wine)
    data = response.json()
    
    print(f"Qualidade: {data['quality']}")
    print(f"Confiança: {data['confidence']:.2%}")
    
    assert response.status_code == 200
    print("✓ Passou!")

def test_5_stats():
    """Teste 5: Estatísticas"""
    print_test("Estatísticas")
    
    response = requests.get(f"{API_URL}/stats")
    data = response.json()
    
    print(f"Total de predições: {data['total_predictions']}")
    print(f"Status: {data['status']}")
    
    assert response.status_code == 200
    print("✓ Passou!")

def test_6_multiple():
    """Teste 6: Múltiplas predições"""
    print_test("Múltiplas Predições")
    
    wines = [
        {"fixed_acidity": 7.0, "volatile_acidity": 0.3, "citric_acid": 0.5, 
         "residual_sugar": 2.0, "chlorides": 0.05, "free_sulfur_dioxide": 30.0,
         "total_sulfur_dioxide": 100.0, "density": 0.995, "pH": 3.2, 
         "sulphates": 0.6, "alcohol": 13.0},
        
        {"fixed_acidity": 9.0, "volatile_acidity": 0.8, "citric_acid": 0.2,
         "residual_sugar": 1.5, "chlorides": 0.2, "free_sulfur_dioxide": 10.0,
         "total_sulfur_dioxide": 40.0, "density": 1.0, "pH": 3.6,
         "sulphates": 0.4, "alcohol": 9.0},
        
        {"fixed_acidity": 7.5, "volatile_acidity": 0.5, "citric_acid": 0.3,
         "residual_sugar": 2.5, "chlorides": 0.07, "free_sulfur_dioxide": 22.0,
         "total_sulfur_dioxide": 85.0, "density": 0.997, "pH": 3.4,
         "sulphates": 0.52, "alcohol": 10.5}
    ]
    
    print(f"\nTestando {len(wines)} vinhos...")
    
    for i, wine in enumerate(wines, 1):
        response = requests.post(f"{API_URL}/predict", json=wine)
        if response.status_code == 200:
            data = response.json()
            print(f"  Vinho {i}: {data['quality']} (confiança: {data['confidence']:.2%})")
    
    print("✓ Passou!")

def run_all_tests():
    """Executar todos os testes"""
    print("\n" + "="*60)
    print("  INICIANDO TESTES DA API")
    print("="*60)
    
    tests = [
        test_1_home,
        test_2_health,
        test_3_prediction_good,
        test_4_prediction_bad,
        test_5_stats,
        test_6_multiple
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            failed += 1
            print(f"\n✗ FALHOU: {e}")
    
    # Resumo
    print("\n" + "="*60)
    print("  RESUMO")
    print("="*60)
    print(f"Total: {len(tests)}")
    print(f"✓ Passou: {passed}")
    print(f"✗ Falhou: {failed}")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 TODOS OS TESTES PASSARAM! 🎉\n")
    else:
        print(f"\n⚠ {failed} teste(s) falharam\n")

if __name__ == "__main__":
    try:
        print("\nVerificando se a API está online...")
        response = requests.get(f"{API_URL}/health", timeout=5)
        print("✓ API está online!\n")
        
        run_all_tests()
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: API não está rodando!")
        print("Inicie a API com: docker compose up\n")
    except Exception as e:
        print(f"\n❌ ERRO: {e}\n")
