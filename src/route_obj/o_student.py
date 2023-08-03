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

    def get_student_list(self, list_id:int):
        sp = "sp_getstudent_list"
        o_Result = DB().exec_query(sp, [list_id])
        if(not o_Result.get("err")):
            return {
                    "msm":"success",
                    "data":o_Result.get("data")
                    }
        return o_Result

    def add_student_out(self, params):
        sp = "sp_add_student_out_list"
        o_Result = DB().exec_query(sp, [
            params["list_id"],
            params["first_name"],
            params["last_name"],
            params["code"],
            params["birthday"],
            params["mother_number"],
            params["father_number"],
            params["phone_number"]
            ])
        if(not o_Result.get("err")):
            return{
                    "msm":"El estudiante se ha agregado correctamente, tanto en actividades como en cursos"
                    }
        return o_Result

    def get_student2update(self, student_id:int):
        sp = "sp_get_student2update"
        o_Result = DB().exec_query(sp, [student_id])
        if(not o_Result.get("err")):
            return{
                    "msm":"success",
                    "data":o_Result.get("data")
                    }
        return o_Result
    
    def update_student_info(self, params):
        sp="sp_update_student"
        o_Result=DB().exec_query(sp, [
            params["s_id"],
            params["first_name"],
            params["last_name"],
            params["code"],
            params["birthday"],
            params["mother_number"],
            params["father_number"],
            params["phone_number"]
            ])
        if(not o_Result.get("err")):
            return{
                    "msm":"Se ha actualizado la informacion del estudiante con exito"
                    }
        return o_Result

    def get_student_file(self, s_id:int):
        sp="sp_get_student_file"
        o_student = DB().exec_query(sp,[s_id, 0])
        o_classroom = DB().exec_query(sp, [s_id, 1])
        o_activities = DB().exec_query(sp, [s_id, 2])
        if(not o_student.get('err') or not o_classroom.get("err") or not o_activities.get("err")):
            return{
                    "msm":"success",
                    "o_student":o_student.get("data"),
                    "o_classroom":o_classroom.get("data"),
                    "o_activities":o_activities.get("data")
                    }
        if(o_student.get("err")):
            return o_student
        if(o_classroom.get("err")):
            return o_classroom
        if(o_activities.get("err")):
            return o_activities

