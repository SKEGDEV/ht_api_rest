from flask import Blueprint, request, jsonify
from src.route_obj.o_student import o_student
from src.util.token_decorator import token_decorator

student = Blueprint("student", __name__)

@student.route('/create-student-list', methods=['POST'])
@token_decorator().token_required
def create():
    data = request.get_json()
    token = request.headers['Authorization'].split(" ")[1]
    token_data = token_decorator().decrypt_token(token)
    json = o_student().make_class_list(data, token_data.get("id"))
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 402
    return response

