import unittest
from app.main import create_app, db
from app.model import Record
from app.action.imdb import extract_data, get_id

class ModelTestSuite(unittest.TestCase):

	def setUp(self):
		self.app = create_app()
		self.app_ctx = self.app.app_context()
		self.app_ctx.push()
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()
		self.app_ctx.pop()

	def test1(self):
		with open("=t3.html", encoding="utf-8") as file:
			data = extract_data(file)
		r1 = Record(imdbid=get_id(data["link"]))
		r1.set_record(data)
		db.session.add(r1)
		db.session.commit()
		m1 = Record.query.first()
		ds = m1.get_record()
		self.assertEqual(data["link"], ds["link"])


