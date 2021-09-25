from flask import flash
from .imdb import extract_data, get_id, make_request
from .imdb import getImdbProfile as gIP

from ..model import Record
from ..main import db

def getImdbProfile(id):
	data = Record.query.filter_by(imdbid = id).first()
	if(not data):
		reply = gIP(id)
		if(reply.get("code",404) == 200):
			try:
				r = Record(imdbid=id)
				r.set_record(reply.get("info"))
				db.session.add(r)
				db.session.commit()
				flash("New Record Saved to DB","info")
			except:
				flash("Error in DB","info")
		return reply
	flash("Record queried from DB","info")
	return {"code":200,"info":data.get_record()}




