from flask import Blueprint, redirect, url_for, json
from .action.api_ref import getImdbProfile, get_id

api_bp = Blueprint('api_bp', __name__, url_prefix="/api")

@api_bp.route('/')
def api_index():
	return redirect(url_for('web_bp.index'))

@api_bp.route('/<id>')
def api(id=0):
	data_id = get_id(id)
	if(data_id):
		data = getImdbProfile(data_id)
		if data["code"] == 200:
			return json.jsonify(data["info"])
		elif data["code"] == 500:
			return json.jsonify({"Error":True}), 500
		else:
			return json.jsonify({"Error":True}), 404
	else:
		return json.jsonify({"Error":True}), 404
