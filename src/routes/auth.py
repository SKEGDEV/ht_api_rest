from flask import Blueprint, jsonify, request
from src.route_obj.auth import o_auth
from src.util.token_decorator import token_decorator


auth = Blueprint('auth', __name__)

@auth.route('/create-account', methods=['POST'])
def create():
    data = request.get_json()
    json = o_auth().create_account(data, str(request.remote_addr))
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 401
    return response

@auth.route('/login', methods=['POST'])
def validate():
    data = request.get_json()
    json = o_auth().validate_user(data, str(request.remote_addr))
    response = jsonify(json)
    if(not json.get("err")):
        response.status_code = 200
        return response
    response.status_code = 401
    return response

@auth.route('/logout', methods=["POST"])
@token_decorator().token_required
def signout():
    try: 
        token = request.headers['Authorization'].split(" ")[1]
        data = token_decorator().decrypt_token(token)
        json = o_auth().logout(data.get("document"))
        response = jsonify(json)
        if(not json.get("err")):
            response.status_code = 200
            return response
        response.status_code=401
        return response
    except Exception as e:
        response = jsonify({
            "msm":"Ocurrio un error inesperado",
            "err":str(e)
            })
        response.status_code = 500
        return response


@auth.route('/verify-session', methods=["GET"])
@token_decorator().token_required
def verify():
    return jsonify({
        "msm":"success",
        "auth":"true"
        });
