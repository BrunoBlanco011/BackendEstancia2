from typing import Optional, List
from datetime import datetime
from src.core.db_postgresql import MySQLConnection
from src.question_options.domain.IQuestionOptionRepository import IQuestionOptionRepository
from src.question_options.domain.entities.QuestionOption import QuestionOption


class PostgreSQLQuestionOptionRepository(IQuestionOptionRepository):
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    async def save(self, option: QuestionOption) -> QuestionOption:
        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor(dictionary=True)

            insert_query = """
                INSERT INTO question_options (
                    question_id, option_text, order_position
                ) 
                VALUES (%s, %s, %s)
            """

            cursor.execute(insert_query, (
                option.question_id,
                option.option_text,
                option.order_position
            ))
            
            option_id = cursor.lastrowid
            
            select_query = """
                SELECT option_id, created_at FROM question_options WHERE option_id = %s
            """
            cursor.execute(select_query, (option_id,))
            result = cursor.fetchone()

            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if result:
                option.option_id = result['option_id']
                option.created_at = result['created_at']
            else:
                option.option_id = option_id
                
            return option

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to save question option: {str(error)}")

    async def get_all(self) -> List[QuestionOption]:
        query = """
            SELECT option_id, question_id, option_text, order_position, created_at
            FROM question_options 
            ORDER BY question_id, order_position
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            options = []
            for row in results:
                options.append(QuestionOption(
                    option_id=row[0],
                    question_id=row[1],
                    option_text=row[2],
                    order_position=row[3],
                    created_at=row[4]
                ))

            return options

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get all question options: {str(error)}")

    async def get_by_id(self, option_id: int) -> Optional[QuestionOption]:
        query = """
            SELECT option_id, question_id, option_text, order_position, created_at
            FROM question_options 
            WHERE option_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (option_id,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return QuestionOption(
                option_id=result[0],
                question_id=result[1],
                option_text=result[2],
                order_position=result[3],
                created_at=result[4]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get question option by id: {str(error)}")

    async def get_by_question(self, question_id: int) -> List[QuestionOption]:
        query = """
            SELECT option_id, question_id, option_text, order_position, created_at
            FROM question_options 
            WHERE question_id = %s
            ORDER BY order_position
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (question_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            options = []
            for row in results:
                options.append(QuestionOption(
                    option_id=row[0],
                    question_id=row[1],
                    option_text=row[2],
                    order_position=row[3],
                    created_at=row[4]
                ))

            return options

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get question options by question: {str(error)}")

    async def update(self, option: QuestionOption) -> None:
        query = """
            UPDATE question_options 
            SET option_text = %s,
                order_position = %s
            WHERE option_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (
                option.option_text,
                option.order_position,
                option.option_id
            ))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Question option not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to update question option: {str(error)}")

    async def delete(self, option_id: int) -> None:
        query = "DELETE FROM question_options WHERE option_id = %s"

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (option_id,))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Question option not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to delete question option: {str(error)}")