from flask import Flask, flash, render_template, request, redirect, url_for, json
from action.imdb import getImdbProfile, get_id
app = Flask(__name__)
app.config['SECRET_KEY'] = "134hhf99s"

@app.route('/')
def index():
	return render_template("page.html")

@app.route('/props', methods=['GET'])
def get_props():
	if(request.args.get('theid')):
		data_id = get_id(request.args.get('theid', False))
		if(data_id):
			data = getImdbProfile(data_id)
			if data:
				flash("Query Found", "success")
				return render_template('main.html', search_key=data_id,data=data, type=type)
			else:
				flash("Error occured","fail")
					
		else:
			flash(f"Not a valid id - `{request.args.get('theid')}`","warning")
	else:
		flash("Empty value input the Imbd Id", "warning")
	return redirect(url_for('.index'))

@app.route('/api')
def api_index():
	return redirect(url_for('.index'))

@app.route('/api/<id>')
def api(id=0):
	data_id = get_id(id)
	if(data_id):
		data = getImdbProfile(data_id)
		if(data):
			return json.jsonify(data)
	else:
		return json.jsonify({"Error":True}), 404

if __name__=='__main__':
	app.run(debug=True)