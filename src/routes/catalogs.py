from flask import Blueprint, jsonify
from src.util.tools import tools

catalogs = Blueprint('catalogs', __name__)

@catalogs.route('/get-catalog/<int:id>/<int:country>')
def get(id, country):
    json = tools().get_catalogs(id, country)
    response = jsonify(json)
    if (not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 403
    return response

