from flask import Blueprint, jsonify, request
from src.util.token_decorator import token_decorator
from src.route_obj.o_Rpt import  oRpt

rpt = Blueprint('rpt', __name__)

@rpt.route('/generate-report-pdf', methods=['POST'])
@token_decorator().token_required
def qualification():
    params = request.get_json()
    json = oRpt(params).Get_rpt()
    response = jsonify(json)
    response.status_code = 200
    if(json['msm'] != 'success'):
        response.status_code = 403
    return response

