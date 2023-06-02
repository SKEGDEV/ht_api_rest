from flask import Blueprint, jsonify, request
from werkzeug.wrappers import response
from src.util.token_decorator import token_decorator
from src.route_obj.o_activity import o_activity

activity = Blueprint("activity", __name__)

@activity.route('/create-activity', methods=['POST'])
@token_decorator().token_required
def create():
    data = request.get_json()
    json = o_activity().create_activity(data)
    response = jsonify(json)
    if(not json.get('err')):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@activity.route('/get-activities/<int:clist>/<int:unit>', methods=['GET'])
@token_decorator().token_required
def get_activities(clist, unit):
    json = o_activity().get_all_activities(clist, unit)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@activity.route('/get-activity-students/<int:id>', methods=['GET'])
@token_decorator().token_required
def get_students(id):
    json = o_activity().get_all_students(id)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@activity.route('/qualified-activity', methods=['PUT']) 
@token_decorator().token_required
def qualified():
    data = request.get_json()
    json = o_activity().qualified(data)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

@activity.route('/get-student-information/<int:id>', methods=['GET'])
@token_decorator().token_required
def get_information(id):
    json = o_activity().get_student(id)
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response
