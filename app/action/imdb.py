from bs4 import BeautifulSoup
from bs4.element import NavigableString
import re, pprint
import requests, urllib.parse as urlparse

regex = re.compile('(.*/).*?')
def remove_string(lst):
	return list(filter((lambda x:type(x) != NavigableString and type(x) != str), lst))

def extract_data(file):
	soup = BeautifulSoup(file);
	dbase = {}

	link = soup.find(attrs={"data-testid":"hero-title-block__metadata"}).select('a')[0]['href']
	link = regex.match(link)[0]
	dbase['link'] = link

	name_of_movie = soup.find('h1', attrs={"data-testid":"hero-title-block__title"}).text.strip()
	dbase['name'] = name_of_movie

	imbd_rating = soup.find('span',class_="AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV").text.strip();
	dbase['rating'] = imbd_rating

	description = soup.find('div',attrs={"data-testid":"storyline-plot-summary"})
	description = description.select("div.ipc-html-content.ipc-html-content--base div")[0].contents[0].strip()
	dbase['summary'] = description

	genres = soup.find('li',attrs={"data-testid":"storyline-genres"}).select('ul li')
	genres = [g.text.strip() for g in genres]
	dbase['genres'] = genres

	runtime = soup.find('li',attrs={"data-testid":"title-techspec_runtime"}).select('ul li')[0].text.strip()
	dbase['runtime'] = runtime

	releasedate = soup.find('li',attrs={"data-testid":"title-details-releasedate"}).select('ul li')[0].text.strip()
	dbase['releasedate'] = releasedate

	countryoforigin = soup.find('li',attrs={"data-testid":"title-details-origin"}).select('ul li')
	countryoforigin = [country.text.strip() for country in countryoforigin]
	dbase['country'] = countryoforigin

	language = soup.find('li',attrs={"data-testid":"title-details-languages"}).select('ul li')
	language = [l.text.strip() for l in language]
	dbase['language'] = language

	directors = soup.find('li',attrs={"data-testid":"title-pc-principal-credit"}).select('ul li')
	directors = [d.text.strip() for d in directors]
	dbase['directors'] = directors

	cast = soup.find('section',attrs={"data-testid":"title-cast"}).select('div[data-testid=title-cast-item]')
	cast_list = []
	for c in cast:
		q = {}
		q["name"] = c.select('[data-testid="title-cast-item__actor"]')[0].text.strip()
		xtr = c.select('[data-testid="cast-item-characters-link"]')[0].contents
		q["cast_name"] = remove_string(xtr)[0].text.strip()
		cast_list.append(q)

	dbase['casts'] = cast_list

	wd = soup.find('div',attrs={"data-testid":"title-pc-wide-screen"}).select('li[data-testid="title-pc-principal-credit"]')
	wd_list = {}
	for w in wd:
		w_l = w.select('ul li')
		wd_list[remove_string(w.contents)[0].text.strip()] = [wl.text.strip() for wl in w_l]

	dbase['extra'] = wd_list;

	return dbase

BASE_URL = "http://imdb.com/title/tt23402"
headers = {"user-agent":"chrome"}
test1 = re.compile("(tt.*)/?")
test2 = re.compile("(?:.*)?(?:/?title)/(tt.*)/?")
id_get = re.compile(".*(tt.*)/?")

def test_param(val):
	return test1.test(val) or test2.test(val)

def get_id(val):
	m = id_get.match(val)
	if(not m):
		return False
	return m[0]
	
def make_request(url):
	url = urlparse.urljoin(BASE_URL,url.strip('/'))
	try:
		r = requests.get(url,headers=headers)
		if(r.status_code == 200):
			return r.text
		else:
			return False
	except:
		return False

def getImdbProfile(id):
	reply = {}
	data = make_request(id)
	#print("getting property of id")
	if(data):
		try:
			reply["info"] = extract_data(data)
			reply["code"] = 200
		except:
			reply["code"] = 404
	else:
		reply["code"] = 500
	return reply
