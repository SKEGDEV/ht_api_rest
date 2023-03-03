from flask_bcrypt import check_password_hash, generate_password_hash
import secrets, string

class bcrypt: 

    def generate(self, password:str):
        return generate_password_hash(password.encode(),10)

    def match(self, password:str, password_db:str):
        return check_password_hash(password_db.encode(), password.encode())

    def generate_public_password(self, length:int):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        password = ''
        for i in range(length):
            password += ''.join(secrets.choice(alphabet))
        return password
