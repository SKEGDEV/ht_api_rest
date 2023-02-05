from flask_bcrypt import check_password_hash, generate_password_hash

class bcrypt: 

    def generate(self, password:str):
        return generate_password_hash(password.encode(),10)

    def match(self, password:str, password_db:str):
        return check_password_hash(password_db.encode(), password.encode())
