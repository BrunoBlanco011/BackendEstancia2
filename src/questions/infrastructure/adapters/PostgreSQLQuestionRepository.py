from typing import Optional, List
from datetime import datetime
from src.core.db_postgresql import MySQLConnection
from src.questions.domain.IQuestionRepository import IQuestionRepository
from src.questions.domain.entities.Question import Question


class PostgreSQLQuestionRepository(IQuestionRepository):
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    async def save(self, question: Question) -> Question:
        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor(dictionary=True)

            insert_query = """
                INSERT INTO questions (
                    survey_id, question_text, question_type, 
                    is_required, order_position
                ) 
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                question.survey_id,
                question.question_text,
                question.question_type,
                question.is_required,
                question.order_position
            ))

            question_id = cursor.lastrowid
            
            select_query = """
                SELECT question_id, created_at FROM questions WHERE question_id = %s
            """
            cursor.execute(select_query, (question_id,))
            result = cursor.fetchone()

            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if result:
                question.question_id = result['question_id']
                question.created_at = result['created_at']
            else:
                question.question_id = question_id
                
            return question

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to save question: {str(error)}")

    async def get_all(self) -> List[Question]:
        query = """
            SELECT question_id, survey_id, question_text, question_type, 
                   is_required, order_position, created_at
            FROM questions 
            ORDER BY survey_id, order_position
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            questions = []
            for row in results:
                questions.append(Question(
                    question_id=row[0],
                    survey_id=row[1],
                    question_text=row[2],
                    question_type=row[3],
                    is_required=row[4],
                    order_position=row[5],
                    created_at=row[6]
                ))

            return questions

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get all questions: {str(error)}")

    async def get_by_id(self, question_id: int) -> Optional[Question]:
        query = """
            SELECT question_id, survey_id, question_text, question_type, 
                   is_required, order_position, created_at
            FROM questions 
            WHERE question_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (question_id,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return Question(
                question_id=result[0],
                survey_id=result[1],
                question_text=result[2],
                question_type=result[3],
                is_required=result[4],
                order_position=result[5],
                created_at=result[6]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get question by id: {str(error)}")

    async def get_by_survey(self, survey_id: int) -> List[Question]:
        query = """
            SELECT question_id, survey_id, question_text, question_type, 
                   is_required, order_position, created_at
            FROM questions 
            WHERE survey_id = %s
            ORDER BY order_position
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (survey_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            questions = []
            for row in results:
                questions.append(Question(
                    question_id=row[0],
                    survey_id=row[1],
                    question_text=row[2],
                    question_type=row[3],
                    is_required=row[4],
                    order_position=row[5],
                    created_at=row[6]
                ))

            return questions

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get questions by survey: {str(error)}")

    async def update(self, question: Question) -> None:
        query = """
            UPDATE questions 
            SET question_text = %s, 
                question_type = %s,
                is_required = %s,
                order_position = %s
            WHERE question_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (
                question.question_text,
                question.question_type,
                question.is_required,
                question.order_position,
                question.question_id
            ))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Question not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to update question: {str(error)}")

    async def delete(self, question_id: int) -> None:
        query = "DELETE FROM questions WHERE question_id = %s"

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (question_id,))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Question not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to delete question: {str(error)}")