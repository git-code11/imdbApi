from .app import db
import json

class Record(db.Model):
	__table_name__ = "records"

	id = db.Column(db.Integer, primary_key=True)
	imdbid = db.Column(db.String(24), primary_key=True, index=True)
	link = db.Column(db.Text)
	name = db.Column(db.Text)
	rating = db.Column(db.Text)
	summary = db.Column(db.Text)
	genres = db.Column(db.Text)
	runtime = db.Column(db.Text)
	releasedate = db.Column(db.Text)
	country = db.Column(db.Text)
	language = db.Column(db.Text)
	directors =db.Column(db.Text)
	cast = db.Column(db.Text)
	extra = db.Column(db.Text)

	def set_record(data):
		if(data):
			for k,v in data:
				self.__setattr__(k,json.dumps(v) if v else None)

	def get_record():
		r_dbs = {}
		for k in Record.__table__.c.keys():
			val = self.__getattr__(k)
			r_dbs[k] = json.loads(val) if val else None;
		r_dbs["imdbid"].pop()
		return r_dbs