import os
import mysql.connector
from mysql.connector import pooling
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class MySQLConnection:
    _instance: Optional['MySQLConnection'] = None

    def __init__(self):
        database_url = os.getenv("DATABASE_URL")

        if not database_url:
            raise Exception("Error: DATABASE_URL no esta configurada en .env")

        try:
            config = self._parse_mysql_url(database_url)
            
            self.connection_pool = pooling.MySQLConnectionPool(
                pool_name="backend_pool",
                pool_size=5,
                pool_reset_session=True,
                **config
            )

            print("Pool de conexiones MySQL inicializado")
            self._test_connection()

        except Exception as error:
            print(f"Error al conectar con MySQL: {error}")
            raise

    def _parse_mysql_url(self, database_url: str) -> dict:
        """Parse MySQL connection URL"""
        # Format: mysql://user:password@host:port/database
        try:
            url = database_url.replace("mysql://", "")
            user_pass, host_db = url.split("@")
            user, password = user_pass.split(":")
            host_port, database = host_db.split("/")
            
            if ":" in host_port:
                host, port = host_port.split(":")
                port = int(port)
            else:
                host = host_port
                port = 3306
            
            return {
                "user": user,
                "password": password,
                "host": host,
                "port": port,
                "database": database
            }
        except Exception as e:
            raise Exception(f"Error parsing DATABASE_URL: {e}")

    def _test_connection(self):
        try:
            conn = self.connection_pool.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            print(f"Conexion a MySQL exitosa - {version}")

        except Exception as error:
            print(f"Error al verificar conexion: {error}")

    def get_connection(self):
        return self.connection_pool.get_connection()

    def put_connection(self, conn):
        """Retorna la conexion al pool"""
        if conn:
            conn.close()

    async def query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute(query, params or ())
            results = cursor.fetchall()

            cursor.close()

            return results

        except Exception as error:
            print(f"Error en query: {error}")
            raise
        finally:
            if conn:
                self.put_connection(conn)

    async def execute(self, query: str, params: Optional[tuple] = None) -> int:
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute(query, params or ())
            
            # For INSERT queries, return the lastrowid; otherwise return rowcount
            last_id = cursor.lastrowid if cursor.lastrowid else cursor.rowcount

            conn.commit()
            cursor.close()

            return last_id

        except Exception as error:
            if conn:
                conn.rollback()
            print(f"Error en execute: {error}")
            raise
        finally:
            if conn:
                self.put_connection(conn)

    async def execute_many(self, query: str, params_list: List[tuple]) -> int:
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.executemany(query, params_list)
            rows_affected = cursor.rowcount

            conn.commit()
            cursor.close()

            return rows_affected

        except Exception as error:
            if conn:
                conn.rollback()
            print(f"Error en execute_many: {error}")
            raise
        finally:
            if conn:
                self.put_connection(conn)

    def close(self):
        try:
            # MySQLConnectionPool does not have close_all or disconnect
            # Just log that we're closing (connections will be garbage collected)
            print("Pool de conexiones MySQL - cerrando conexiones...")
        except Exception as error:
            print(f"Error al cerrar el pool: {error}")


def get_db_connection() -> MySQLConnection:
    if MySQLConnection._instance is None:
        MySQLConnection._instance = MySQLConnection()
    return MySQLConnection._instance