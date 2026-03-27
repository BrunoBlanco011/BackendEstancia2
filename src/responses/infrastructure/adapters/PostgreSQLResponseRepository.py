from typing import Optional, List
from datetime import datetime
from src.core.db_postgresql import MySQLConnection
from src.responses.domain.IResponseRepository import IResponseRepository
from src.responses.domain.entities.Response import Response


class PostgreSQLResponseRepository(IResponseRepository):
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    async def save(self, response: Response) -> Response:
        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor(dictionary=True)

            insert_query = """
                INSERT INTO responses (
                    survey_id, respondent_email, respondent_user_id, ip_address
                ) 
                VALUES (%s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                response.survey_id,
                response.respondent_email,
                response.respondent_user_id,
                response.ip_address
            ))

            response_id = cursor.lastrowid
            
            select_query = """
                SELECT response_id, submitted_at FROM responses WHERE response_id = %s
            """
            cursor.execute(select_query, (response_id,))
            result = cursor.fetchone()

            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if result:
                response.response_id = result['response_id']
                response.submitted_at = result['submitted_at']
            else:
                response.response_id = response_id
                
            return response

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to save response: {str(error)}")

    async def get_all(self) -> List[Response]:
        query = """
            SELECT response_id, survey_id, respondent_email, respondent_user_id, 
                   submitted_at, ip_address
            FROM responses 
            ORDER BY submitted_at DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            responses = []
            for row in results:
                responses.append(Response(
                    response_id=row[0],
                    survey_id=row[1],
                    respondent_email=row[2],
                    respondent_user_id=row[3],
                    submitted_at=row[4],
                    ip_address=row[5]
                ))

            return responses

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get all responses: {str(error)}")

    async def get_by_id(self, response_id: int) -> Optional[Response]:
        query = """
            SELECT response_id, survey_id, respondent_email, respondent_user_id, 
                   submitted_at, ip_address
            FROM responses 
            WHERE response_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (response_id,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return Response(
                response_id=result[0],
                survey_id=result[1],
                respondent_email=result[2],
                respondent_user_id=result[3],
                submitted_at=result[4],
                ip_address=result[5]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get response by id: {str(error)}")

    async def get_by_survey(self, survey_id: int) -> List[Response]:
        query = """
            SELECT response_id, survey_id, respondent_email, respondent_user_id, 
                   submitted_at, ip_address
            FROM responses 
            WHERE survey_id = %s
            ORDER BY submitted_at DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (survey_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            responses = []
            for row in results:
                responses.append(Response(
                    response_id=row[0],
                    survey_id=row[1],
                    respondent_email=row[2],
                    respondent_user_id=row[3],
                    submitted_at=row[4],
                    ip_address=row[5]
                ))

            return responses

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get responses by survey: {str(error)}")

    async def get_by_user(self, user_id: int) -> List[Response]:
        query = """
            SELECT response_id, survey_id, respondent_email, respondent_user_id, 
                   submitted_at, ip_address
            FROM responses 
            WHERE respondent_user_id = %s
            ORDER BY submitted_at DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            responses = []
            for row in results:
                responses.append(Response(
                    response_id=row[0],
                    survey_id=row[1],
                    respondent_email=row[2],
                    respondent_user_id=row[3],
                    submitted_at=row[4],
                    ip_address=row[5]
                ))

            return responses

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get responses by user: {str(error)}")

    async def delete(self, response_id: int) -> None:
        query = "DELETE FROM responses WHERE response_id = %s"

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (response_id,))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Response not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to delete response: {str(error)}")