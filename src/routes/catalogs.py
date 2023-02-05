from flask import Blueprint, request, jsonify
from src.util.tools import tools
from src.util.token_decorator import token_decorator

catalogs = Blueprint('catalogs', __name__)

@catalogs.route('/get-catalog/<int:id>')
@token_decorator().token_required
def get(id):
    json = tools().get_catalogs(id)
    response = jsonify(json)
    if (not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

