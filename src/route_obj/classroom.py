from src.util.database import DB

class o_classroom:

    def create_classroom(self, params, document_number:str):
        sp = "sp_create_classroom"
        o_Result = DB().exec_query(sp, [params["class_name"], params["type"], document_number])
        if(not o_Result.get("err")):
            return {"msm":"Se creo con exito el salon de clases", "data":o_Result.get("data")} 
        return o_Result

    def list2classroom(self, params):
        sp = "sp_list_2_classroom"
        o_Result = DB().exec_query(sp, [params["classroom_id"], params["list_id"]])
        if(not o_Result.get("err")):
            return{
                    "msm":"El listado de estudiantes se agrego correctamente al curso"
                    }
        return o_Result

    def get_classrooms(self, document_number:str):
        sp = "sp_get_all_classroom"
        o_Result = DB().exec_query(sp, [document_number])
        if(not o_Result.get("err")):
            return{
                    "msm":("Total clases encontradas: " + str(len(o_Result.get("data")))),
                    "data": o_Result.get("data")
                    }
        return o_Result

    def get_all_Ustudents(self, unit_number:int, Clist_id:int):
        sp = "sp_get_classroom_student"
        o_Result = DB().exec_query(sp, [Clist_id, unit_number])
        if(not o_Result.get("err")):
            return {
                    "msm":("Total estudiantes encontrados: " + str(len(o_Result.get("data")))),
                    "data": o_Result.get("data")
                    }
        return o_Result

