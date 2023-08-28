from flask import request, jsonify, Blueprint
from werkzeug.wrappers import response
from src.util.token_decorator import token_decorator
from src.route_obj.classroom import o_classroom

classroom = Blueprint("classroom", __name__)

@classroom.route("/create-classroom", methods=["POST"])
@token_decorator().token_required
def create():
    data = request.get_json()
    token = request.headers["Authorization"].split(" ")[1]
    token_data = token_decorator().decrypt_token(token)
    json = o_classroom().create_classroom(data, token_data.get("document"))
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@classroom.route("/get-classrooms/<int:variant>/<int:year>", methods=["GET"])
@token_decorator().token_required
def get(variant, year):
    token = request.headers["Authorization"].split(" ")[1]
    token_data = token_decorator().decrypt_token(token)
    json = o_classroom().get_classrooms(token_data.get("document"), variant, year)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code=403
    return response

@classroom.route("/student_2_classroom", methods=["POST"])
@token_decorator().token_required
def get_unit():
    data = request.get_json()
    json = o_classroom().list2classroom(data)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@classroom.route("/get-all-unit-student/<int:c_id>/<int:unit_number>", methods = ["GET"])
@token_decorator().token_required
def get_Ustudent(c_id, unit_number):
    json = o_classroom().get_all_Ustudents(unit_number, c_id)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@classroom.route("/get-clist/<int:id>", methods=["GET"])
@token_decorator().token_required
def get_Clist(id):
    json = o_classroom().get_clist(id)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code=200
        return response
    response.status_code=403
    return response
