from src.util.database import DB

class o_student:

    def make_class_list(self, params, document:str):
        sp = "sp_create_class_list"
        o_Result = DB().exec_query(sp, [params["name"], document])
        if(not o_Result.get("err")):
            list_id = 0
            for d in  o_Result.get("data"):
               list_id = d[0]
            return self.insert_students(params["data"], list_id)
        return o_Result


    def insert_students(self, student_list, list_id:int):
        sp = "sp_create_student"
        o_Result = {}
        for d in student_list:
            o_Result = DB().exec_query(sp, [
                 d["first_name"],
                 d["last_name"],
                 d["code"],
                 list_id,
                 d["birthday"],
                 d["mother_number"],
                 d["father_number"],
                 d["phone_number"]
                ])
        if(not o_Result.get("err")):
            return {"msm":"Se ha creado el listado de estudiantes correctamente"}
        return o_Result

    def get_all_teacher_list(self, document_number):
        sp = "sp_get_all_list"
        o_Result = DB().exec_query(sp, [document_number])
        if(not o_Result.get("err")):
            return {"msm":"Estos son todos los listados creados por ti", "data":o_Result.get("data")}
        return o_Result



