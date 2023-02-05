from src.util.database import DB
from src.util.token_decorator import token_decorator
from src.util.bcrypt import bcrypt

class o_auth:
    
    def create_account(self, params, IP:str):
        if(self.userExist(params["usr_name"])):
            return {"msm":"El nombre de usuario ya esta siendo utilizado actualmente", "userExist":"yes"}
        sp = "sp_create_account"
        o_Result = DB().exec_query(sp,[ 
            params["first_name"],
            params["last_name"],
            params["birthday"],
            params["document"],
            params["email"],
            params["phone"],
            params["usr_name"],
            bcrypt().generate(params["usr_password"])
            ])
        if(not o_Result.get("err")): 
            return self.create_session_token(o_Result.get("data"), IP)
        return o_Result

    def validate_user(self, params, IP:str):
        sp = "sp_get_teacher_session"
        o_Result = DB().exec_query(sp, [params["usr_name"]])
        password = ""
        if(o_Result.get("err")):
            return o_Result
        if(not len(o_Result.get("data"))>0):
            return{"msm":"El usuario y/o la contrasena son incorrectos", "isValid":"not"}
        for d in o_Result.get("data"):
            password = d[2]
        if(not bcrypt().match(params["password"], password)):
            return{"msm":"El usuario y/o la contrasena son incorrectos", "isValid":"not"}
        return self.create_session_token(o_Result.get("data"), IP)

    def logout(self, user_id:int):
        sp = "sp_update_teacher_token"
        o_Result = DB().exec_query(sp, ["", user_id])
        if(o_Result.get("err")):
            return o_Result
        if(len(o_Result.get("data"))<0):
            return {"msm":"Ocurrio un error durante el cierre de sesion", "err":"La sesion no se pudo cerrar por parte de la DB"}
        return {"msm":"Que tenga un buen dia, vuelva pronto!"}


    def create_session_token(self, data, IP:str):
        try:
            token_data = {}
            name = ""
            usr_id = 0
            for d in data:
                usr_id = d[0]
                token_data = {
                        "id":d[0]
                        }
                name=d[1]
            token_db = token_decorator().generate_token({"id":usr_id, "ip":IP})
            sp = "sp_update_teacher_token"
            o_Result = DB().exec_query(sp, [token_db, usr_id])
            if(not o_Result.get("err") and len(o_Result.get("data")) > 0):
                return {"msm":("Bienvenido/a gracias por su preferencia sr/sra: "+name),
                        "name":name,
                        "token":token_decorator().generate_token(token_data)}
            return o_Result 
        except Exception as e:
            return {"msm":"Ocurrio un error durante la generacion del token", "err":str(e)}

    def userExist(self, usr_name:str):
        sp = 'sp_get_teacher_session'
        o_Result = DB().exec_query(sp, [usr_name]) 
        if(not o_Result.get("err") and len(o_Result.get("data"))<1):
            return False
        return True 

