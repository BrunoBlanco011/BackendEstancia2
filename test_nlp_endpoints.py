"""
Script para probar los endpoints NLP del backend
Ejecutar: python test_nlp_endpoints.py
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_extract_keywords():
    """Test: Extracción de palabras clave simples"""
    print("\n" + "="*60)
    print("TEST 1: Extract Keywords (Simples)")
    print("="*60)
    
    url = f"{BASE_URL}/nlp/extract-keywords"
    payload = {
        "text": "Tengo mucha preocupación y ansiedad. Mi concentración está muy baja y sufro de insomnio.",
        "min_length": 3,
        "language": "spanish"
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def test_extract_ranked_keywords():
    """Test: Extracción de palabras clave con ranking"""
    print("\n" + "="*60)
    print("TEST 2: Extract Ranked Keywords (Con Frecuencia)")
    print("="*60)
    
    url = f"{BASE_URL}/nlp/extract-ranked-keywords"
    payload = {
        "text": "La ansiedad es un problema serio. Tengo ansiedad desde hace años. "
                "Mi ansiedad afecta mi vida diaria. También sufro fatiga y nerviosismo. "
                "El nerviosismo aumenta mi tensión.",
        "min_length": 3,
        "language": "spanish",
        "top_n": 5
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def test_extract_phrases():
    """Test: Extracción de frases/n-gramas"""
    print("\n" + "="*60)
    print("TEST 3: Extract Phrases (N-gramas)")
    print("="*60)
    
    url = f"{BASE_URL}/nlp/extract-phrases"
    payload = {
        "text": "Tengo problemas de concentración y dificultad para dormir. "
                "Mi estado emocional es muy bajo.",
        "phrase_length": 2,
        "language": "spanish"
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def test_nlp_health():
    """Test: Health check del módulo"""
    print("\n" + "="*60)
    print("TEST 4: NLP Health Check")
    print("="*60)
    
    url = f"{BASE_URL}/nlp/health"
    
    print(f"URL: {url}")
    
    try:
        response = requests.get(url)
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def test_english_extraction():
    """Test: Extracción en inglés"""
    print("\n" + "="*60)
    print("TEST 5: English Text Processing")
    print("="*60)
    
    url = f"{BASE_URL}/nlp/extract-ranked-keywords"
    payload = {
        "text": "I have anxiety and depression. My sleep is really bad. "
                "I feel anxious most of the time.",
        "min_length": 3,
        "language": "english",
        "top_n": 5
    }
    
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload)
        print(f"\nStatus: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def test_long_text():
    """Test: Texto largo"""
    print("\n" + "="*60)
    print("TEST 6: Long Text Processing")
    print("="*60)
    
    url = f"{BASE_URL}/nlp/extract-ranked-keywords"
    long_text = """
    La ansiedad es un trastorno mental que afecta a muchas personas en el mundo.
    Los síntomas de la ansiedad incluyen preocupación constante, nerviosismo, 
    insomnio y fatiga. La ansiedad puede ser provocada por estrés, depresión 
    u otros factores. Es importante buscar ayuda profesional si sufres de ansiedad.
    El tratamiento para la ansiedad puede incluir terapia, medicamentos o ambos.
    La ansiedad y la depresión frecuentemente van juntas. La tensión muscular 
    es común en las personas con ansiedad.
    """
    
    payload = {
        "text": long_text,
        "min_length": 3,
        "language": "spanish",
        "top_n": 10
    }
    
    print(f"URL: {url}")
    print(f"Texto: {len(long_text)} caracteres")
    
    try:
        response = requests.post(url, json=payload)
        print(f"\nStatus: {response.status_code}")
        result = response.json()
        print(f"Total de palabras únicas: {result.get('unique_keywords', 0)}")
        print(f"Palabras clave top 10: {result.get('keywords', [])}")
        print(f"Response completo: {json.dumps(result, indent=2)}")
    except Exception as e:
        print(f"Error: {e}")


def run_all_tests():
    """Ejecuta todos los tests"""
    print("\n" + "#"*60)
    print("# EJECUTANDO TESTS DEL MÓDULO NLP")
    print("#"*60)
    
    try:
        # Primero verif que el servidor esté disponible
        print("\nVerificando conexión con la API...")
        response = requests.get(f"{BASE_URL}/nlp/health", timeout=3)
        if response.status_code == 200:
            print("✅ API disponible en", BASE_URL)
        else:
            print("⚠️  API respondió con status:", response.status_code)
    except requests.ConnectionError:
        print("❌ ERROR: No se puede conectar a la API en", BASE_URL)
        print("   Asegúrate que el servidor está corriendo: python main.py")
        return
    except Exception as e:
        print("❌ ERROR:", e)
        return
    
    # Ejecutar tests
    test_extract_keywords()
    test_extract_ranked_keywords()
    test_extract_phrases()
    test_nlp_health()
    test_english_extraction()
    test_long_text()
    
    print("\n" + "#"*60)
    print("# TESTS COMPLETADOS")
    print("#"*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
