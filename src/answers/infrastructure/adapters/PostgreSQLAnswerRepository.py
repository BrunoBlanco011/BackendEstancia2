from typing import Optional, List
from datetime import datetime
from src.core.db_postgresql import MySQLConnection
from src.answers.domain.IAnswerRepository import IAnswerRepository
from src.answers.domain.entities.Answer import Answer


class PostgreSQLAnswerRepository(IAnswerRepository):
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    async def save(self, answer: Answer) -> Answer:
        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor(dictionary=True)

            insert_query = """
                INSERT INTO answers (
                    response_id, question_id, answer_text, 
                    selected_option_id, scale_value
                ) 
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                answer.response_id,
                answer.question_id,
                answer.answer_text,
                answer.selected_option_id,
                answer.scale_value
            ))

            answer_id = cursor.lastrowid
            
            select_query = """
                SELECT answer_id, created_at FROM answers WHERE answer_id = %s
            """
            cursor.execute(select_query, (answer_id,))
            result = cursor.fetchone()

            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if result:
                answer.answer_id = result['answer_id']
                answer.created_at = result['created_at']
            else:
                answer.answer_id = answer_id
                
            return answer

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to save answer: {str(error)}")

    async def get_all(self) -> List[Answer]:
        query = """
            SELECT answer_id, response_id, question_id, answer_text, 
                   selected_option_id, scale_value, created_at
            FROM answers 
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

            answers = []
            for row in results:
                answers.append(Answer(
                    answer_id=row[0],
                    response_id=row[1],
                    question_id=row[2],
                    answer_text=row[3],
                    selected_option_id=row[4],
                    scale_value=row[5],
                    created_at=row[6]
                ))

            return answers

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get all answers: {str(error)}")

    async def get_by_id(self, answer_id: int) -> Optional[Answer]:
        query = """
            SELECT answer_id, response_id, question_id, answer_text, 
                   selected_option_id, scale_value, created_at
            FROM answers 
            WHERE answer_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (answer_id,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return Answer(
                answer_id=result[0],
                response_id=result[1],
                question_id=result[2],
                answer_text=result[3],
                selected_option_id=result[4],
                scale_value=result[5],
                created_at=result[6]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get answer by id: {str(error)}")

    async def get_by_response(self, response_id: int) -> List[Answer]:
        query = """
            SELECT answer_id, response_id, question_id, answer_text, 
                   selected_option_id, scale_value, created_at
            FROM answers 
            WHERE response_id = %s
            ORDER BY created_at
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (response_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            answers = []
            for row in results:
                answers.append(Answer(
                    answer_id=row[0],
                    response_id=row[1],
                    question_id=row[2],
                    answer_text=row[3],
                    selected_option_id=row[4],
                    scale_value=row[5],
                    created_at=row[6]
                ))

            return answers

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get answers by response: {str(error)}")

    async def get_by_question(self, question_id: int) -> List[Answer]:
        query = """
            SELECT answer_id, response_id, question_id, answer_text, 
                   selected_option_id, scale_value, created_at
            FROM answers 
            WHERE question_id = %s
            ORDER BY created_at DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (question_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            answers = []
            for row in results:
                answers.append(Answer(
                    answer_id=row[0],
                    response_id=row[1],
                    question_id=row[2],
                    answer_text=row[3],
                    selected_option_id=row[4],
                    scale_value=row[5],
                    created_at=row[6]
                ))

            return answers

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get answers by question: {str(error)}")

    async def update(self, answer: Answer) -> None:
        query = """
            UPDATE answers 
            SET answer_text = %s,
                selected_option_id = %s,
                scale_value = %s
            WHERE answer_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (
                answer.answer_text,
                answer.selected_option_id,
                answer.scale_value,
                answer.answer_id
            ))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Answer not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to update answer: {str(error)}")

    async def delete(self, answer_id: int) -> None:
        query = "DELETE FROM answers WHERE answer_id = %s"

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (answer_id,))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Answer not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to delete answer: {str(error)}")