from flask import Blueprint, flash, render_template, request, redirect, url_for
from .action.api_ref import getImdbProfile, get_id

web_bp = Blueprint('web_bp',__name__)

@web_bp.route('/')
def index():
	return render_template("page.html")

@web_bp.route('/props', methods=['GET'])
def get_props():
	if(request.args.get('theid')):
		data_id = get_id(request.args.get('theid', False))
		if(data_id):
			data = getImdbProfile(data_id)
			if data["code"] == 200:
				flash("Query Found", "success")
				return render_template('main.html', search_key=data_id,data=data["info"], type=type)
			elif data["code"] == 500:
				flash("Error occured","fail")
			else:
				flash("Data For ID not Found","fail")
		else:
			flash(f"Not a valid id - `{request.args.get('theid')}`","warning")
	else:
		flash("Empty value input the Imbd Id", "warning")
	return redirect(url_for('.index'))
