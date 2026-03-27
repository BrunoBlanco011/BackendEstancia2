from src.responses.domain.IResponseRepository import IResponseRepository
from src.responses.domain.entities.Response import Response


class CreateResponseUseCase:
    def __init__(self, repository: IResponseRepository):
        self.repository = repository

    async def execute(self, response: Response) -> Response:
        if not response.survey_id or response.survey_id < 1:
            raise ValueError("El ID de la encuesta es obligatorio")

        # Validar que al menos tenga email o user_id
        if not response.respondent_email and not response.respondent_user_id:
            raise ValueError("Debe proporcionar al menos un email o ID de usuario")

        # Validar formato de IP si se proporciona
        if response.ip_address and len(response.ip_address) > 45:
            raise ValueError("La dirección IP no puede exceder 45 caracteres")

        return await self.repository.save(response)