from typing import Optional, List
from datetime import datetime
from src.core.db_postgresql import MySQLConnection
from src.users.domain.IUserRepository import IUserRepository
from src.users.domain.entities.User import User


class PostgreSQLUserRepository(IUserRepository):
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    async def save(self, user: User) -> User:
        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            insert_query = """
                INSERT INTO users (
                    name, last_name, email, password, 
                    role_id, registration_date, profile_image
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                user.name,
                user.last_name,
                user.email,
                user.password,
                user.role_id,
                user.registration_date,
                user.profile_image
            ))

            user_id = cursor.lastrowid
            
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            user.user_id = user_id
            return user

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to save user: {str(error)}")

    async def get_by_email(self, email: str) -> Optional[User]:
        query = """
            SELECT user_id, name, last_name, email, password, 
                   role_id, registration_date, profile_image
            FROM users 
            WHERE email = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (email,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return User(
                user_id=result[0],
                name=result[1],
                last_name=result[2],
                email=result[3],
                password=result[4],
                role_id=result[5],
                registration_date=result[6],
                profile_image=result[7]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get user by email: {str(error)}")

    async def get_all(self) -> List[User]:
        query = """
            SELECT user_id, name, last_name, email, password, 
                   role_id, registration_date, profile_image
            FROM users 
            ORDER BY registration_date DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            users = []
            for row in results:
                users.append(User(
                    user_id=row[0],
                    name=row[1],
                    last_name=row[2],
                    email=row[3],
                    password=row[4],
                    role_id=row[5],
                    registration_date=row[6],
                    profile_image=row[7]
                ))

            return users

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get all users: {str(error)}")

    async def get_by_id(self, user_id: int) -> Optional[User]:
        query = """
            SELECT user_id, name, last_name, email, password, 
                   role_id, registration_date, profile_image
            FROM users 
            WHERE user_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return User(
                user_id=result[0],
                name=result[1],
                last_name=result[2],
                email=result[3],
                password=result[4],
                role_id=result[5],
                registration_date=result[6],
                profile_image=result[7]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get user by id: {str(error)}")

    async def update(self, user: User) -> None:
        query = """
            UPDATE users 
            SET name = %s, 
                last_name = %s, 
                email = %s,
                profile_image = %s
            WHERE user_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (
                user.name,
                user.last_name,
                user.email,
                user.profile_image,
                user.user_id
            ))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("User not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to update user: {str(error)}")

    async def delete(self, user_id: int) -> None:
        query = "DELETE FROM users WHERE user_id = %s"

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (user_id,))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("User not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to delete user: {str(error)}")