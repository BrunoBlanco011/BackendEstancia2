from typing import Optional, List
from datetime import datetime
from src.core.db_postgresql import MySQLConnection
from src.files.domain.IFileRepository import IFileRepository
from src.files.domain.entities.File import File


class PostgreSQLFileRepository(IFileRepository):
    def __init__(self, conn: MySQLConnection):
        self.conn = conn

    async def save(self, file: File) -> File:
        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor(dictionary=True)

            # Insert the file
            insert_query = """
                INSERT INTO files (
                    file_name, original_name, file_path, file_size, 
                    file_type, uploaded_by
                ) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            cursor.execute(insert_query, (
                file.file_name,
                file.original_name,
                file.file_path,
                file.file_size,
                file.file_type,
                file.uploaded_by
            ))
            
            file_id = cursor.lastrowid

            # Get the created file with timestamps
            select_query = """
                SELECT file_id, upload_date FROM files WHERE file_id = %s
            """
            cursor.execute(select_query, (file_id,))
            result = cursor.fetchone()
            
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if result:
                file.file_id = result['file_id']
                file.upload_date = result['upload_date']
            else:
                file.file_id = file_id
                
            return file

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to save file: {str(error)}")

    async def get_all(self) -> List[File]:
        query = """
            SELECT file_id, file_name, original_name, file_path, 
                   file_size, file_type, uploaded_by, upload_date
            FROM files 
            ORDER BY upload_date DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query)
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            files = []
            for row in results:
                files.append(File(
                    file_id=row[0],
                    file_name=row[1],
                    original_name=row[2],
                    file_path=row[3],
                    file_size=row[4],
                    file_type=row[5],
                    uploaded_by=row[6],
                    upload_date=row[7]
                ))

            return files

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get all files: {str(error)}")

    async def get_by_id(self, file_id: int) -> Optional[File]:
        query = """
            SELECT file_id, file_name, original_name, file_path, 
                   file_size, file_type, uploaded_by, upload_date
            FROM files 
            WHERE file_id = %s
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (file_id,))
            result = cursor.fetchone()

            cursor.close()
            self.conn.put_connection(connection)

            if not result:
                return None

            return File(
                file_id=result[0],
                file_name=result[1],
                original_name=result[2],
                file_path=result[3],
                file_size=result[4],
                file_type=result[5],
                uploaded_by=result[6],
                upload_date=result[7]
            )

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get file by id: {str(error)}")

    async def get_by_user(self, user_id: int) -> List[File]:
        query = """
            SELECT file_id, file_name, original_name, file_path, 
                   file_size, file_type, uploaded_by, upload_date
            FROM files 
            WHERE uploaded_by = %s
            ORDER BY upload_date DESC
        """

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (user_id,))
            results = cursor.fetchall()

            cursor.close()
            self.conn.put_connection(connection)

            files = []
            for row in results:
                files.append(File(
                    file_id=row[0],
                    file_name=row[1],
                    original_name=row[2],
                    file_path=row[3],
                    file_size=row[4],
                    file_type=row[5],
                    uploaded_by=row[6],
                    upload_date=row[7]
                ))

            return files

        except Exception as error:
            if connection:
                self.conn.put_connection(connection)
            raise Exception(f"Failed to get files by user: {str(error)}")

    async def delete(self, file_id: int) -> None:
        query = "DELETE FROM files WHERE file_id = %s"

        connection = None
        try:
            connection = self.conn.get_connection()
            cursor = connection.cursor()

            cursor.execute(query, (file_id,))

            rows_affected = cursor.rowcount
            connection.commit()
            cursor.close()
            self.conn.put_connection(connection)

            if rows_affected == 0:
                raise Exception("File not found")

        except Exception as error:
            if connection:
                connection.rollback()
                self.conn.put_connection(connection)
            raise Exception(f"Failed to delete file: {str(error)}")