from jwt import encode, decode
from datetime import datetime, timedelta
from os import getenv


class token:

    def generate_token(self, token_data:dict): 
        return encode(
                payload={**token_data, "expiration":str(datetime.now() + timedelta(days=7))},
                key=str(getenv("token_key")),
                algorithm=str(getenv("algorithm"))
                )

    def decrypt_token(self, token:str): 
        return decode(token, key=str(getenv("token_key")), algorithms=[str(getenv("algorithm"))])  

