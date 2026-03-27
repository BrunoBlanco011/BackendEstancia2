from typing import Optional, List
from datetime import datetime
from src.core.db_postgresql import MySQLConnection
from src.survey.domain.ISurveyRepository import ISurveyRepository
from src.survey.domain.entities.Survey import Survey


class PostgreSQLSurveyRepository(ISurveyRepository):
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    async def save(self, survey: Survey) -> Survey:
        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor(dictionary=True)

            insert_query = """
                INSERT INTO survey (
                    name_survey, description, created_by, is_active
                ) 
                VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                survey.title,
                survey.description,
                survey.created_by,
                True
            ))
            
            survey_id = cursor.lastrowid

            select_query = """
                SELECT survey_id, created_at, updated_at FROM survey WHERE survey_id = %s
            """
            cursor.execute(select_query, (survey_id,))
            result = cursor.fetchone()

            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if result:
                survey.survey_id = result['survey_id']
                survey.created_at = result['created_at']
                survey.updated_at = result['updated_at']
            else:
                survey.survey_id = survey_id
                
            return survey

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to save survey: {str(error)}")

    async def get_all(self) -> List[Survey]:
        query = """
            SELECT survey_id, name_survey, description, created_by, 
                   created_at, updated_at, is_active
            FROM survey 
            ORDER BY created_at DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            surveys = []
            for row in results:
                surveys.append(Survey(
                    survey_id=row[0],
                    name_survey=row[1],
                    description=row[2],
                    created_by=row[3],
                    created_at=row[4],
                    updated_at=row[5],
                    is_active=row[6]
                ))

            return surveys

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get all surveys: {str(error)}")

    async def get_by_id(self, survey_id: int) -> Optional[Survey]:
        query = """
            SELECT survey_id, name_survey, description, created_by, 
                   created_at, updated_at, is_active
            FROM survey 
            WHERE survey_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (survey_id,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return Survey(
                survey_id=result[0],
                name_survey=result[1],
                description=result[2],
                created_by=result[3],
                created_at=result[4],
                updated_at=result[5],
                is_active=result[6]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get survey by id: {str(error)}")

    async def get_by_user(self, user_id: int) -> List[Survey]:
        query = """
            SELECT survey_id, name_survey, description, created_by, 
                   created_at, updated_at, is_active
            FROM survey 
            WHERE created_by = %s
            ORDER BY created_at DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            surveys = []
            for row in results:
                surveys.append(Survey(
                    survey_id=row[0],
                    name_survey=row[1],
                    description=row[2],
                    created_by=row[3],
                    created_at=row[4],
                    updated_at=row[5],
                    is_active=row[6]
                ))

            return surveys

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get surveys by user: {str(error)}")

    async def update(self, survey: Survey) -> None:
        query = """
            UPDATE survey 
            SET name_survey = %s, 
                description = %s,
                is_active = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE survey_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (
                survey.name_survey,
                survey.description,
                survey.is_active,
                survey.survey_id
            ))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Survey not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to update survey: {str(error)}")

    async def delete(self, survey_id: int) -> None:
        query = "DELETE FROM survey WHERE survey_id = %s"

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (survey_id,))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Survey not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to delete survey: {str(error)}")