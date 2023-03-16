from src.util.database import DB

class o_activity:

    def create_activity(self, params): 
        if(self.isActivityAvailable(params["Clist"], params["number"], params["qualification"])):
            return{"err":"error", "msm":"Perdon la calificacion para esta actividad excede el punteo total del curso"}
        sp = "sp_create_activity"
        o_Result = DB().exec_query(sp, [
                                        params["name"],
                                        params["qualification"],
                                        params["Clist"],
                                        params["type"],
                                        params["subtype"],
                                        params["number"]
                                        ])
        if(not o_Result.get("err")):
            return{"msm":"se ha creado con exito la actividad"}
        return o_Result

    def isActivityAvailable(self, clist:int, number:int, activity_qualification:float):
        sp = "sp_get_total_points"
        o_Result = DB().exec_query(sp, [clist, number]) 
        if(not o_Result.get("err") and len(o_Result.get("data")) != 0):
            db_points = 0
            for d in o_Result.get("data"): 
                db_points = d[0]
            if(not (float(db_points) + activity_qualification) > 100):
                return False
            return True
        return True

    def get_all_activities(self, clist:int, unit_number:int):
        sp = "sp_get_all_activity"
        o_Result = DB().exec_query(sp, [clist, unit_number])
        if(not o_Result.get("err")):
            return{
                    "msm":("Total actividades encontradas: " + str(len(o_Result.get("data")))),
                    "data":o_Result.get("data")
                    }
        return o_Result

    def get_all_students(self, activity_id):
        sp = "sp_get_activity_student"
        o_Result = DB().exec_query(sp, [activity_id])
        if(not o_Result.get("err")):
            return{
                    "msm":"success",
                    "data":o_Result.get("data")
                    }
        return o_Result

    def qualified(self, params):
        sp = "sp_update_activity"
        qualification = params["qualification"]
        if(params["type"] == 1):
            qualification = params["qualification"] * (-1)
        o_Result = DB().exec_query(sp, [params["id"], qualification])
        if(not o_Result.get("err")):
            return{
                    "msm":"Se ha calificado correctamente"
                    }
        return o_Result

