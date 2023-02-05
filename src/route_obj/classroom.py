from src.util.database import DB

class o_classroom:

    def create_classroom(self, params, user_id:int):
        sp = "sp_create_classroom"
        o_Result = DB().exec_query(sp, [params["class_name"], params["type"], user_id, params["list"]])
        if(not o_Result.get("err")):
            return {"msm":"Se creo con exito el salon de clases"} 
        return o_Result

    def get_classrooms(self, user_id:int):
        sp = "sp_get_all_classroom"
        o_Result = DB().exec_query(sp, [user_id])
        if(not o_Result.get("err")):
            return{
                    "msm":("Total clases encontradas: " + str(len(o_Result.get("data")))),
                    "data": o_Result.get("data")
                    }
        return o_Result

    def get_all_unit(self, classroom_id:int):
        sp = "sp_get_all_units"
        o_Result = DB().exec_query(sp, [classroom_id])
        if(not o_Result.get("err")):
            return{
                    "msm":"success",
                    "data":o_Result.get("data")
                    }
        return o_Result

    def get_all_Ustudents(self, unit_id):
        sp = "sp_get_unit_students"
        o_Result = DB().exec_query(sp, [unit_id])
        if(not o_Result.get("err")):
            return {
                    "msm":("Total estudiantes encontrados: " + str(len(o_Result.get("data")))),
                    "data": o_Result.get("data")
                    }
        return o_Result

