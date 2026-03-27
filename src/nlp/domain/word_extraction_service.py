import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re
from typing import List

# Descargar recursos necesarios (ejecutar una sola vez)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class WordExtractionService:
    """Servicio para extraer y procesar palabras clave de textos"""
    
    def __init__(self):
        self.spanish_stopwords = set(stopwords.words('spanish'))
        self.english_stopwords = set(stopwords.words('english'))
    
    def extract_keywords(
        self, 
        text: str, 
        min_length: int = 3,
        language: str = 'spanish'
    ) -> List[str]:
        """
        Extrae palabras clave de un texto
        
        Args:
            text: Texto del cual extraer palabras
            min_length: Longitud mínima de palabras a considerar
            language: Idioma ('spanish' o 'english')
        
        Returns:
            Lista de palabras clave únicas y procesadas
        """
        if not text or len(text.strip()) == 0:
            return []
        
        # Convertir a minúsculas
        text_lower = text.lower()
        
        # Tokenizar
        tokens = word_tokenize(text_lower)
        
        # Seleccionar stopwords según idioma
        stopwords_set = self.spanish_stopwords if language == 'spanish' else self.english_stopwords
        
        # Filtrar: solo palabras alfanuméricas, sin stopwords y con longitud mínima
        keywords = []
        seen = set()
        
        for token in tokens:
            # Eliminar puntuación y caracteres especiales
            clean_token = re.sub(r'[^\w]', '', token)
            
            # Validar que cumpla criterios
            if (clean_token 
                and len(clean_token) >= min_length 
                and clean_token not in stopwords_set
                and clean_token.isalpha()
                and clean_token not in seen):
                keywords.append(clean_token)
                seen.add(clean_token)
        
        return keywords
    
    def extract_and_rank_keywords(
        self,
        text: str,
        min_length: int = 3,
        language: str = 'spanish',
        top_n: int = 10
    ) -> dict:
        """
        Extrae palabras clave y las ranking por frecuencia
        
        Args:
            text: Texto del cual extraer palabras
            min_length: Longitud mínima de palabras
            language: Idioma
            top_n: Número top de palabras a retornar
        
        Returns:
            Dict con 'keywords' (list) y 'frequency' (dict)
        """
        keywords = self.extract_keywords(text, min_length, language)
        
        # Contar frecuencias
        frequency = {}
        for keyword in keywords:
            frequency[keyword] = frequency.get(keyword, 0) + 1
        
        # Ordenar por frecuencia
        ranked = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        top_keywords = [word for word, _ in ranked[:top_n]]
        
        return {
            'keywords': top_keywords,
            'frequency': dict(ranked[:top_n]),
            'total_keywords': len(keywords),
            'unique_keywords': len(set(keywords))
        }
    
    def extract_phrases(
        self,
        text: str,
        phrase_length: int = 2,
        language: str = 'spanish'
    ) -> List[str]:
        """
        Extrae frases (n-gramas) del texto
        
        Args:
            text: Texto del cual extraer frases
            phrase_length: Longitud de las frases (número de palabras)
            language: Idioma
        
        Returns:
            Lista de frases únicas
        """
        keywords = self.extract_keywords(text, min_length=2, language=language)
        
        # Crear n-gramas
        phrases = []
        for i in range(len(keywords) - phrase_length + 1):
            phrase = ' '.join(keywords[i:i + phrase_length])
            phrases.append(phrase)
        
        # Retornar frases únicas
        return list(set(phrases))
