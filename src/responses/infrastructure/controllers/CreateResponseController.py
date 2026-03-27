from fastapi import status, Request
from fastapi.responses import JSONResponse
from src.responses.application.CreateResponseUseCase import CreateResponseUseCase
from src.responses.domain.entities.Response import Response
from src.responses.domain.dto.ResponseRequest import CreateResponseRequest
from src.responses.domain.dto.ResponseResponse import CreateResponseResponse, CreatedResponseData


class CreateResponseController:
    def __init__(self, create_response: CreateResponseUseCase):
        self.create_response = create_response

    async def execute(self, request_data: CreateResponseRequest, request: Request):
        try:
            # Obtener IP del cliente
            ip_address = request_data.ip_address
            if not ip_address:
                # Intentar obtener la IP real del cliente
                ip_address = request.client.host if request.client else None

            response = Response(
                survey_id=request_data.survey_id,
                respondent_email=request_data.respondent_email,
                respondent_user_id=request_data.respondent_user_id,
                ip_address=ip_address
            )

            saved_response = await self.create_response.execute(response)

            response_obj = CreateResponseResponse(
                message="Respuesta creada exitosamente",
                response=CreatedResponseData(
                    responseId=saved_response.response_id,
                    surveyId=saved_response.survey_id,
                    respondentEmail=saved_response.respondent_email,
                    respondentUserId=saved_response.respondent_user_id,
                    submittedAt=saved_response.submitted_at.isoformat(),
                    ipAddress=saved_response.ip_address
                )
            )

            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=response_obj.model_dump()
            )

        except ValueError as error:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": str(error)}
            )
        except Exception as error:
            print(f"Error al crear respuesta: {error}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": "Error interno del servidor"}
            )