import secrets


class SecurityUtils:

    @staticmethod
    def generate_random_string(length: int) -> str:
        random_bytes = secrets.token_bytes((length + 1) // 2)
        hex_string = ''.join(f'{byte:02x}' for byte in random_bytes)
        return hex_string[:length]