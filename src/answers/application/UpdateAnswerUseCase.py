from src.answers.domain.IAnswerRepository import IAnswerRepository
from src.answers.domain.entities.Answer import Answer


class UpdateAnswerUseCase:
    def __init__(self, repository: IAnswerRepository):
        self.repository = repository

    async def execute(self, answer: Answer) -> None:
        if not answer.answer_id or answer.answer_id < 1:
            raise ValueError("El ID de la respuesta es obligatorio")

        existing_answer = await self.repository.get_by_id(answer.answer_id)
        if not existing_answer:
            raise ValueError("Respuesta no encontrada")

        # Validar rango de escala si se proporciona
        if answer.scale_value is not None and (answer.scale_value < 1 or answer.scale_value > 5):
            raise ValueError("El valor de escala debe estar entre 1 y 5")

        await self.repository.update(answer)