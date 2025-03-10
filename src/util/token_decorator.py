from src.util.token import token
from src.util.bcrypt import bcrypt
from functools import wraps
from flask import request, jsonify
from datetime import datetime as time
from src.util.database import DB


class token_decorator(token):

#this function is to validate all information of the token, and in here you can add new conditions for the token
    def verify_token(self):
        try:
            auth_token = request.headers.get('Authorization') 
            if(not auth_token or 'Bearer' not in auth_token):
                return{"msm":"Authorization","err":"Error, no se encontro el token correspondiente"}
            if(not len(auth_token.split(" ")) == 2):
                return{"msm":"Authorization","err":"Error el token recibido no es valido"}
            token_data = self.decrypt_token(token = request.headers['Authorization'].split(" ")[1]) 
            token_date = time.strptime(token_data.get("expiration"), "%Y-%m-%d %H:%M:%S.%f") 
            DB_Result = self.get_tokenDB(token_data.get("document"))   
            if(DB_Result == {}):
                return{"msm":"Authorization","err":"Sesion no iniciada por favor dirigirse a: para poder iniciar sesion o a: para crear una cuenta"}  
            tokenDB_data = self.decrypt_token(DB_Result.get("token")) 
            if(not (tokenDB_data.get("document")==token_data.get("document")) or not (tokenDB_data.get("ip") == request.remote_addr)):
                return{"msm":"Authorization", "err":"este token pertenece a otro usuario, error al validar"}
            if(not bcrypt().match(token_data.get("password"), DB_Result.get("password"))):
                return{"msm":"Authorization", "err":"La sesion es incorrecta, por favor contacte a soporte tecnico si el error persiste"}
            if(time.now() > token_date):
                return{"msm":"Authorization", "err":"El token de sesion ha expirado"}
            return{"success":"AUTHORIZE"}
        except Exception as e:
            return{
                    "err":str(e),
                    "msm":"Authorization"
                    }

#this funciton is to be a decorator, and stoped any endpoint if the token is invalid or any situation
    def token_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            res = self.verify_token() 
            if(not res.get("success")):
                response = jsonify(res) 
                response.status_code=401
                return response
            return f( *args, **kwargs)   
        return decorator


    def get_tokenDB(self, document_number):
        sp = "sp_get_teacher_token"
        o_Result = DB().exec_query(sp, [document_number])
        if(not o_Result.get("err")):
            token = ""
            isActive = False
            public_pswd = ""
            for d in o_Result.get("data"):
                isActive = d[0]
                public_pswd = d[1]
                token = d[2]
            return {"token":token, "isActive":isActive, "password":public_pswd} 
        return  {}
