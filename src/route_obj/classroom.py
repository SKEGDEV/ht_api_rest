from src.util.database import DB

class o_classroom:

    def create_classroom(self, params, document_number:str):
        sp = "sp_create_classroom"
        o_Result = DB().exec_query(sp, [params["class_name"], params["type"], document_number])
        if(not o_Result.get("err")):
            return {"msm":"Se ha creado con exito el curso", "data":o_Result.get("data")} 
        return o_Result

    def list2classroom(self, params):
        if(not self.isL2C_available(params)):
            return{
                    "not_available":"true",
                    "msm":"El listado ya esta asignado al curso intente con otro nuevamente"
                    }
        sp = "sp_list_2_classroom"
        o_Result = DB().exec_query(sp, [params["classroom_id"], params["list_id"]])
        if(not o_Result.get("err")):
            return{
                    "msm":"El listado de estudiantes se agrego correctamente al curso"
                    }
        return o_Result

    def isL2C_available(self, params):
        sp = "sp_is_available_c2l"
        o_Result = DB().exec_query(sp, [params["list_id"], params["classroom_id"]])
        if(not o_Result.get("err") and (len(o_Result.get("data"))==0)):
            return True
        return False
            

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

    def get_clist(self, classroom_id):
        sp = "sp_get_clist"
        o_Result = DB().exec_query(sp, [classroom_id])
        if(o_Result.get("err")):
            return o_Result
        if(len(o_Result.get("data")) == 0):
            return{
                    "msm":"success",
                    "isEmpty":"true"
                    }
        if(len(o_Result.get("data")) == 1):
            return{
                    "msm":"success",
                    "isUnique":"true",
                    "data":o_Result.get("data")
                    }
        return {
                "msm":"success",
                "data":o_Result.get("data")
                }

