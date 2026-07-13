from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from src.nlp.infrastructure.controllers.NLPController import NLPController
from src.core.security.jwt_middleware import get_current_user, UserPrincipal


class ExtractKeywordsRequest(BaseModel):
    text: str
    min_length: Optional[int] = 3
    language: Optional[str] = 'spanish'


class ExtractAndRankKeywordsRequest(BaseModel):
    text: str
    min_length: Optional[int] = 3
    language: Optional[str] = 'spanish'
    top_n: Optional[int] = 10


class ExtractPhrasesRequest(BaseModel):
    text: str
    phrase_length: Optional[int] = 2
    language: Optional[str] = 'spanish'


def configure_nlp_routes(
    api_router: APIRouter,
    extract_keywords_controller,
    extract_and_rank_keywords_controller,
    extract_phrases_controller
):
    """Configura las rutas del módulo NLP"""
    
    @api_router.post("/nlp/extract-keywords")
    async def extract_keywords(
        request: ExtractKeywordsRequest,
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        """
        Extrae palabras clave simples de un texto

        - **text**: Texto a procesar
        - **min_length**: Longitud mínima de palabras (default: 3)
        - **language**: Idioma ('spanish' o 'english', default: 'spanish')
        """
        return await extract_keywords_controller(
            text=request.text,
            min_length=request.min_length,
            language=request.language
        )

    @api_router.post("/nlp/extract-ranked-keywords")
    async def extract_ranked_keywords(
        request: ExtractAndRankKeywordsRequest,
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        """
        Extrae palabras clave con ranking por frecuencia

        - **text**: Texto a procesar
        - **min_length**: Longitud mínima de palabras (default: 3)
        - **language**: Idioma ('spanish' o 'english', default: 'spanish')
        - **top_n**: Número top de palabras a retornar (default: 10, max: 100)
        """
        return await extract_and_rank_keywords_controller(
            text=request.text,
            min_length=request.min_length,
            language=request.language,
            top_n=request.top_n
        )

    @api_router.post("/nlp/extract-phrases")
    async def extract_phrases(
        request: ExtractPhrasesRequest,
        current_user: UserPrincipal = Depends(get_current_user)
    ):
        """
        Extrae frases (n-gramas) de un texto

        - **text**: Texto a procesar
        - **phrase_length**: Longitud de las frases en palabras (1-5, default: 2)
        - **language**: Idioma ('spanish' o 'english', default: 'spanish')
        """
        return await extract_phrases_controller(
            text=request.text,
            phrase_length=request.phrase_length,
            language=request.language
        )
    
    @api_router.get("/nlp/health")
    async def nlp_health():
        """Verifica el estado del módulo NLP"""
        return {
            "status": "healthy",
            "module": "NLP Processing",
            "supported_languages": ["spanish", "english"],
            "available_endpoints": [
                "/nlp/extract-keywords",
                "/nlp/extract-ranked-keywords",
                "/nlp/extract-phrases"
            ]
        }
