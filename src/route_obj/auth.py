from src.util.database import DB
from src.util.token_decorator import token_decorator
from src.util.bcrypt import bcrypt

class o_auth:
    
    def create_account(self, params, IP:str):
        if(self.userExist(params["document"])):
            return {"msm":"El numero de documento ya ha sido utilizado", "userExist":"yes"}
        public_pwd = bcrypt().generate_public_password(12)
        sp = "sp_create_account"
        o_Result = DB().exec_query(sp, [params["first_name"],
                                        params["last_name"],
                                        params["birthday"],
                                        bcrypt().generate(params["usr_password"]),
                                        params["document"],
                                        params["email"],
                                        params["phone"],
                                        params["document_type"]])
        if(not o_Result.get("err")): 
            return self.create_session_token({"document":params["document"], "password":public_pwd, "variant":1}, IP)
        return o_Result

    def validate_user(self, params, IP:str):
        public_pwd = bcrypt().generate_public_password(12)
        sp = "sp_get_teacher_session"
        o_Result = DB().exec_query(sp, [params["document_number"]])
        password = ""
        if(o_Result.get("err")):
            return o_Result
        if(not len(o_Result.get("data"))>0):
            return{"msm":"El usuario y/o la contrasena son incorrectos", "isValid":"not"}
        for d in o_Result.get("data"):
            password = d[0]
        if(not bcrypt().match(params["password"], password)):
            return{"msm":"El usuario y/o la contrasena son incorrectos", "isValid":"not"}
        return self.create_session_token({"document":params["document_number"], "password":public_pwd, "variant":2}, IP)

    def logout(self, document_number):
        sp = "sp_update_teacher_session"
        o_Result = DB().exec_query(sp, [document_number, "", "", 3])
        if(o_Result.get("err")):
            return o_Result
        if(len(o_Result.get("data"))<0):
            return {"msm":"Ocurrio un error durante el cierre de sesion", "err":"La sesion no se pudo cerrar por parte de la DB"}
        return {"msm":"Que tenga un buen dia, vuelva pronto!"}


    def create_session_token(self, data:dict, IP:str):
        try: 
            token_db = token_decorator().generate_token({'document':data.get('document'), "ip":IP})
            sp = "sp_update_teacher_session"
            o_Result = DB().exec_query(sp, [data.get("document"), bcrypt().generate(str(data.get("password"))), token_db, data.get("variant")])
            if(not o_Result.get("err")):
                name = ""
                for d in o_Result.get("data"):
                   name = d[0] 
                return {"msm":("Bienvenido/a gracias por su preferencia sr/sra: "+name),
                        "name":name,
                        "token":token_decorator().generate_token({
                            "document":data.get("document"),
                            "password":data.get("password")
                            })}
            return o_Result 
        except Exception as e:
            return {"msm":"Ocurrio un error durante la generacion del token", "err":str(e)}

    def userExist(self, document_number:str):
        sp = 'sp_get_teacher_session'
        o_Result = DB().exec_query(sp, [document_number]) 
        if(not o_Result.get("err") and len(o_Result.get("data"))<1):
            return False
        return True 

