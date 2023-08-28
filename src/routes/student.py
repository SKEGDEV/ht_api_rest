from flask import Blueprint, Response, request, jsonify
from werkzeug.wrappers import response
from src.route_obj.o_student import o_student
from src.util.token_decorator import token_decorator

student = Blueprint("student", __name__)

@student.route('/create-student-list', methods=['POST'])
@token_decorator().token_required
def create():
    data = request.get_json()
    token = request.headers['Authorization'].split(" ")[1]
    token_data = token_decorator().decrypt_token(token)
    json = o_student().make_class_list(data, token_data.get("document"))
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 402
    return response

@student.route('/get-all-list', methods=['GET'])
@token_decorator().token_required
def get():
    token = request.headers["Authorization"].split(" ")[1]
    token_data = token_decorator().decrypt_token(token)
    json = o_student().get_all_teacher_list(token_data.get("document"))
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@student.route('/get-all-student/<int:id>', methods=["GET"])
@token_decorator().token_required
def get_list(id):
    json = o_student().get_student_list(id)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@student.route('/create-student-out-list', methods=['POST'])
@token_decorator().token_required
def create_out_list():
    o_Data = request.get_json();
    json = o_student().add_student_out(o_Data)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@student.route('/get-student-2-update/<int:s_id>', methods=['GET'])
@token_decorator().token_required
def get_student2update(s_id):
    json = o_student().get_student2update(s_id)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@student.route('/update-student-information', methods=["PUT"])
@token_decorator().token_required
def update_information():
    o_Data = request.get_json()
    json = o_student().update_student_info(o_Data)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code=200
        return response
    response.status_code=403
    return response

@student.route('/get-student-file/<int:s_id>', methods=['GET'])
@token_decorator().token_required
def get_file(s_id):
    json = o_student().get_student_file(s_id)
    response = jsonify(json)
    response.status_code=200
    if(json.get("err")):
        response.status_code=403
    return response

@student.route('/get-student-qualification', methods=["GET"])
@token_decorator().token_required
def get_file_qualification():
    json = o_student().get_qualification()
    response = jsonify(json)
    response.status_code = 200
    if(json['msm'] != "success"):
        response.status_code = 403
    return response
    
@student.route('/get-catalogs', methods=['GET'])
@token_decorator().token_required
def get_catalogs():
    json = o_student().get_list_catalogs()
    response = jsonify(json)
    response.status_code = 200
    if(json.get("err")):
        response.status_code = 403
    return response
