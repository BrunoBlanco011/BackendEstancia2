from src.nlp.domain.word_extraction_service import WordExtractionService
from src.nlp.infrastructure.controllers.NLPController import NLPController


class NLPDependencies:
    """Contenedor de dependencias para el módulo NLP"""
    
    def __init__(self):
        self.word_extraction_service = WordExtractionService()
        self.nlp_controller = NLPController(self.word_extraction_service)
    
    # Métodos para cada acción
    async def extract_keywords(self, text: str, min_length: int = 3, language: str = 'spanish'):
        return await self.nlp_controller.extract_keywords(text, min_length, language)
    
    async def extract_and_rank_keywords(self, text: str, min_length: int = 3, language: str = 'spanish', top_n: int = 10):
        return await self.nlp_controller.extract_and_rank_keywords(text, min_length, language, top_n)
    
    async def extract_phrases(self, text: str, phrase_length: int = 2, language: str = 'spanish'):
        return await self.nlp_controller.extract_phrases(text, phrase_length, language)


def init_nlp():
    """Inicializa las dependencias del módulo NLP"""
    return NLPDependencies()
