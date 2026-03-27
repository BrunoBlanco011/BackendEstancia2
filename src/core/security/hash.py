import bcrypt


class HashService:
    SALT_ROUNDS = 10

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt(rounds=HashService.SALT_ROUNDS)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def check_password(hashed_password: str, password: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception:
            return False