from flask import request, jsonify, Blueprint
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

@classroom.route("/get-classrooms", methods=["GET"])
@token_decorator().token_required
def get():
    token = request.headers["Authorization"].split(" ")[1]
    token_data = token_decorator().decrypt_token(token)
    json = o_classroom().get_classrooms(token_data.get("document"))
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code=403
    return response

@classroom.route("/get-all-unit/<int:id>", methods=["GET"])
@token_decorator().token_required
def get_unit(id):
    json = o_classroom().get_all_unit(id)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@classroom.route("/get-all-unit-student/<int:id>", methods = ["GET"])
@token_decorator().token_required
def get_Ustudent(id):
    json = o_classroom().get_all_Ustudents(id)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response
