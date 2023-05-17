from src.util.database import DB

class tools:

    def get_catalogs(self, catalog, country):
        sp = "sp_get_catalogs"
        o_Result = DB().exec_query(sp, [catalog, country])
        if(not o_Result.get("err")):
            return{"msm":"success", "data":o_Result.get("data")}
        return o_Result
