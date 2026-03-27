from src.questions.domain.IQuestionRepository import IQuestionRepository


class DeleteQuestionUseCase:
    def __init__(self, repository: IQuestionRepository):
        self.repository = repository

    async def execute(self, question_id: int) -> None:
        if question_id < 1:
            raise ValueError("El ID de la pregunta debe ser mayor a 0")

        existing_question = await self.repository.get_by_id(question_id)
        if not existing_question:
            raise ValueError("Pregunta no encontrada")

        await self.repository.delete(question_id)