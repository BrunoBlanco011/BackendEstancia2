from fastapi import HTTPException
from src.nlp.domain.word_extraction_service import WordExtractionService
from typing import List


class NLPController:
    """Controlador para operaciones de procesamiento de lenguaje natural"""
    
    def __init__(self, word_extraction_service: WordExtractionService):
        self.word_extraction_service = word_extraction_service
    
    async def extract_keywords(
        self,
        text: str,
        min_length: int = 3,
        language: str = 'spanish'
    ) -> dict:
        """
        Extrae palabras clave de un texto
        
        Raises:
            HTTPException: Si el texto está vacío o es inválido
        """
        try:
            if not text or len(text.strip()) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="El texto no puede estar vacío"
                )
            
            if min_length < 1:
                raise HTTPException(
                    status_code=400,
                    detail="La longitud mínima debe ser mayor a 0"
                )
            
            if language not in ['spanish', 'english']:
                raise HTTPException(
                    status_code=400,
                    detail="Idioma no soportado. Use 'spanish' o 'english'"
                )
            
            keywords = self.word_extraction_service.extract_keywords(
                text=text,
                min_length=min_length,
                language=language
            )
            
            return {
                "success": True,
                "keywords": keywords,
                "count": len(keywords)
            }
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al extraer palabras clave: {str(e)}"
            )
    
    async def extract_and_rank_keywords(
        self,
        text: str,
        min_length: int = 3,
        language: str = 'spanish',
        top_n: int = 10
    ) -> dict:
        """
        Extrae y ranking de palabras clave por frecuencia
        
        Raises:
            HTTPException: Si hay errores en los parámetros o procesamiento
        """
        try:
            if not text or len(text.strip()) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="El texto no puede estar vacío"
                )
            
            if top_n < 1 or top_n > 100:
                raise HTTPException(
                    status_code=400,
                    detail="top_n debe estar entre 1 y 100"
                )
            
            result = self.word_extraction_service.extract_and_rank_keywords(
                text=text,
                min_length=min_length,
                language=language,
                top_n=top_n
            )
            
            return {
                "success": True,
                **result
            }
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al procesar texto: {str(e)}"
            )
    
    async def extract_phrases(
        self,
        text: str,
        phrase_length: int = 2,
        language: str = 'spanish'
    ) -> dict:
        """
        Extrae frases (n-gramas) del texto
        
        Raises:
            HTTPException: Si hay errores en parámetros
        """
        try:
            if not text or len(text.strip()) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="El texto no puede estar vacío"
                )
            
            if phrase_length < 1 or phrase_length > 5:
                raise HTTPException(
                    status_code=400,
                    detail="La longitud de frase debe estar entre 1 y 5"
                )
            
            phrases = self.word_extraction_service.extract_phrases(
                text=text,
                phrase_length=phrase_length,
                language=language
            )
            
            return {
                "success": True,
                "phrases": phrases,
                "count": len(phrases)
            }
        
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error al extraer frases: {str(e)}"
            )
