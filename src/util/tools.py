from src.util.database import DB

class tools:

    def get_catalogs(self, catalog):
        sp = "sp_get_catalogs"
        o_Result = DB().exec_query(sp, [catalog])
        if(not o_Result.get("err")):
            return{"msm":"success", "data":o_Result.get("data")}
        return o_Result
