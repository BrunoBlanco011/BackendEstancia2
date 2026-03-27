from typing import Optional, List
from datetime import datetime
from src.core.db_postgresql import MySQLConnection
from src.answer_options.domain.IAnswerOptionRepository import IAnswerOptionRepository
from src.answer_options.domain.entities.AnswerOption import AnswerOption


class PostgreSQLAnswerOptionRepository(IAnswerOptionRepository):
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    async def save(self, answer_option: AnswerOption) -> AnswerOption:
        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor(dictionary=True)

            insert_query = """
                INSERT INTO answer_options (
                    answer_id, option_id
                ) 
                VALUES (%s, %s)
            """

            cursor.execute(insert_query, (
                answer_option.answer_id,
                answer_option.option_id
            ))
            
            answer_option_id = cursor.lastrowid
            
            select_query = """
                SELECT answer_option_id, created_at FROM answer_options WHERE answer_option_id = %s
            """
            cursor.execute(select_query, (answer_option_id,))
            result = cursor.fetchone()

            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if result:
                answer_option.answer_option_id = result['answer_option_id']
                answer_option.created_at = result['created_at']
            else:
                answer_option.answer_option_id = answer_option_id
                
            return answer_option

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to save answer option: {str(error)}")

    async def get_all(self) -> List[AnswerOption]:
        query = """
            SELECT answer_option_id, answer_id, option_id, created_at
            FROM answer_options 
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

            answer_options = []
            for row in results:
                answer_options.append(AnswerOption(
                    answer_option_id=row[0],
                    answer_id=row[1],
                    option_id=row[2],
                    created_at=row[3]
                ))

            return answer_options

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get all answer options: {str(error)}")

    async def get_by_id(self, answer_option_id: int) -> Optional[AnswerOption]:
        query = """
            SELECT answer_option_id, answer_id, option_id, created_at
            FROM answer_options 
            WHERE answer_option_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (answer_option_id,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return AnswerOption(
                answer_option_id=result[0],
                answer_id=result[1],
                option_id=result[2],
                created_at=result[3]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get answer option by id: {str(error)}")

    async def get_by_answer(self, answer_id: int) -> List[AnswerOption]:
        query = """
            SELECT answer_option_id, answer_id, option_id, created_at
            FROM answer_options 
            WHERE answer_id = %s
            ORDER BY created_at
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (answer_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            answer_options = []
            for row in results:
                answer_options.append(AnswerOption(
                    answer_option_id=row[0],
                    answer_id=row[1],
                    option_id=row[2],
                    created_at=row[3]
                ))

            return answer_options

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get answer options by answer: {str(error)}")

    async def delete(self, answer_option_id: int) -> None:
        query = "DELETE FROM answer_options WHERE answer_option_id = %s"

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (answer_option_id,))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("Answer option not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to delete answer option: {str(error)}")