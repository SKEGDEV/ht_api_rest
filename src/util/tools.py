from src.util.database import DB
from os import getenv
import requests
import json

class tools:

    def get_catalogs(self, catalog, country):
        sp = "sp_get_catalogs"
        o_Result = DB().exec_query(sp, [catalog, country])
        if(not o_Result.get("err")):
            return{"msm":"success", "data":o_Result.get("data")}
        return o_Result

    def consume_reportApi(self, oData:dict, oRpt:dict):
        request = {
                "oauth":{
                    "usr":str(getenv("rpt_usr")),
                    "pass":str(getenv("rp_pss")),
                    },
                "oData":oData,
                "oRpt":oRpt
                } 
        try:
            response = requests.post(str(getenv("rp_uri_base")), json=json.dumps(request)) 
            if(response.status_code == 404):
                return{
                        "msm":"Ocurrio un error inesperado",
                        "err":"La ruta a la que se ha intentado acceder no existe por favor contacte con el soporte IT"
                        } 
            return json.loads(response.content)  
        except Exception as e:
            return{
                    "msm":"Ocurrio un error al consumir la report API",
                    "err":str(e)
                    }
