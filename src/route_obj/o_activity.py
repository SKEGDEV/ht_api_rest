from src.util.database import DB

class o_activity:

    def create_activity(self, params): 
        declarative = params["declarative"]
        attitudinal = params["attitudinal"]
        procedural = params["procedural"]
        activity = params["activity"]
        qualification = float(declarative["qualification"]) + float(attitudinal["qualification"]) + float(procedural["qualification"])
        if(self.isActivityAvailable(int(activity["Clist"]), int(activity["number"]), qualification)):
            return{"msm":"La calificacion excede el limite de 100 pts", "isMax":"true"}
        sp = "sp_create_activity"
        o_Result = DB().exec_query(sp, [
                                        declarative["name"],
                                        procedural["name"],
                                        attitudinal["name"],
                                        declarative["qualification"],
                                        procedural["qualification"],
                                        attitudinal["qualification"],
                                        activity["Clist"],
                                        activity["subtype"],
                                        activity["number"]
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
            if(not db_points):
                db_points =0
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

    def get_all_students(self, activity_id:int):
        sp = "sp_get_activity_student"
        o_Result = DB().exec_query(sp, [activity_id])
        if(not o_Result.get("err")):
            return{
                    "msm":"success",
                    "data":o_Result.get("data")
                    }
        return o_Result

    def get_student(self, student_id:int):
        sp = "sp_get_student2qualified"
        o_Result = DB().exec_query(sp, [student_id])
        if(not o_Result.get("err")):
            return{
                    "msm":"success",
                    "data":o_Result.get("data")
                    }
        return o_Result

    def qualified(self, params):
        declarative = params["declarative"]
        procedural = params["procedural"]
        attitudinal = params["attitudinal"]
        qualification = params["qualification"]
        isDeclarativeValid = self.isQualificationValid(declarative, int(qualification["type"]))
        isAttitudinalValid = self.isQualificationValid(attitudinal, int(qualification["type"]))
        isProceduralValid = self.isQualificationValid(procedural, int(qualification["type"]))
        if(isDeclarativeValid.get("result") != "success"):
            return isDeclarativeValid
        if(isAttitudinalValid.get("result") != "success"):
            return isAttitudinalValid
        if(isProceduralValid.get("result") != "success"):
            return isProceduralValid
        sp = "sp_update_activity"
        q_declarative = float(declarative["s_points"])
        q_attitudinal = float(attitudinal["s_points"])
        q_procedural = float(procedural["s_points"])
        if(int(qualification["type"]) == 2):
            q_declarative *= -1
            q_attitudinal *= -1
            q_procedural *= -1
        o_Result = DB().exec_query(sp, [qualification["id"], q_declarative, q_attitudinal, q_procedural])
        if(not o_Result.get("err")):
            return{
                    "msm":"Se ha calificado correctamente"
                    }
        return o_Result

    def isQualificationValid(self, item, a_type:int):
        studentPoints = float(item["s_points"])
        studentCurrentPoints = float(item["s_current_points"])
        activityQualification = float(item["a_qualification"])
        if(((studentPoints + studentCurrentPoints) > activityQualification) and a_type == 1):
            return{
                    "isValid":"false",
                    "msm":("La calificacion "+item["q_name"]+" no puede ser mayor a: " + str((activityQualification - studentCurrentPoints))),
                    "result":"fail"
                    }
        if(studentCurrentPoints < studentPoints and a_type == 2):
            return{
                    "isValid":"false",
                    "msm":("La calificacion "+item["q_name"]+" no puede ser menor a: " + str(studentCurrentPoints)),
                    "result":"fail"
                    }
        return{
                "result":"success"
                }

