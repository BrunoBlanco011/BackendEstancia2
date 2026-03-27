from src.answers.domain.IAnswerRepository import IAnswerRepository
from src.answers.domain.entities.Answer import Answer


class CreateAnswerUseCase:
    def __init__(self, repository: IAnswerRepository):
        self.repository = repository

    async def execute(self, answer: Answer) -> Answer:
        if not answer.response_id or answer.response_id < 1:
            raise ValueError("El ID de la respuesta es obligatorio")

        if not answer.question_id or answer.question_id < 1:
            raise ValueError("El ID de la pregunta es obligatorio")

        # Validar que al menos uno de los campos de respuesta esté presente
        has_answer = (
            (answer.answer_text and answer.answer_text.strip()) or
            answer.selected_option_id is not None or
            answer.scale_value is not None
        )

        if not has_answer:
            raise ValueError("Debe proporcionar al menos un tipo de respuesta")

        # Validar rango de escala
        if answer.scale_value is not None and (answer.scale_value < 1 or answer.scale_value > 5):
            raise ValueError("El valor de escala debe estar entre 1 y 5")

        return await self.repository.save(answer)