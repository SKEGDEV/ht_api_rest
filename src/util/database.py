import winreg
import mysql.connector as mysql
from os import getenv
from src.util.token import token 

class DB:

    def get_key(self, key_name:str):
        path=r"SOFTWARE\happyt"
        try:
            key_connect = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ)
            key = winreg.QueryValueEx(key_connect, key_name)
            winreg.CloseKey(key_connect) 
            return key
        except:
            try:
                path = r"SOFTWARE\WOW6432Node\happyt"
                key_connect = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path, 0, winreg.KEY_READ)
                key = winreg.QueryValueEx(key_connect, key_name)
                winreg.CloseKey(key_connect) 
                return key
            except Exception as e:
                return ["Ha ocurrido un error",str(e)]

    def get_connect(self):
        try:
            key = token().decrypt_token(self.get_key(str(getenv("db_happyT")))[0]) 
            connect = mysql.connect(
                    host=key.get("host"),
                    user=key.get("usr"),
                    password=key.get("pssw"),
                    database=key.get("db")
                    ) 
            return connect
        except Exception as e:
            return{"msm":"Ha ocurrido un error de conexion con la base de datos", "err":str(e)}

    def exec_query(self, sp_name:str, params):
        try:
            data = []
            connect = self.get_connect()
            cursor = connect.cursor()
            query_result = cursor.callproc(sp_name, params)
            result = cursor.stored_results()
            connect.commit()
            for d in result:
                data = d.fetchall()
            return{"data":data, "result":query_result, "msm":"Consulta realizada con exito"}
        except Exception as e:
            return {"msm":"Ocurrio un error durante la consulta","err":str(e)}

