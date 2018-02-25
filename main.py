#!/usr/bin/env python
import os
import jinja2
import webapp2
from random import randrange


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class Prestolnica:
    def __init__(self, ime, drzava, slika):
        self.ime = ime
        self.drzava = drzava
        self.slika = slika

ljubljana = Prestolnica("Ljubljana", "Slovenija", "https://www.slovenia.info/uploads/mesta/cities-tromostovje-ljubljana.jpg")
zagreb = Prestolnica("Zagreb", "Hrvaska", "https://www.intrepidtravel.com/adventures/wp-content/uploads/2017/10/croatia_zagreb_night-city.jpg")
dunaj = Prestolnica("Dunaj", "Avstrija", "http://citymagazine.si/wp-content/uploads/2016/10/stadtansicht-wien-oesterreich-werbung-julius-silver-d.jpg.3146489-1000x500.jpg")
budimpesta = Prestolnica("Budimpesta", "Madzarska", "http://www.srpskacafe.com/wp-content/uploads/2017/12/budimpe%C5%A1ta.jpg")
rim = Prestolnica("Rim", "Italija", "https://www.planatours.rs/images/stories/evropa/italija/rim//rim041.jpg")

niz_prestolnic = [ljubljana, zagreb, dunaj, budimpesta, rim]

class MainHandler(BaseHandler):
    def get(self):

        random_index = randrange(0, len(niz_prestolnic))
        prestolnica = niz_prestolnic[random_index]

        podatki = {"prestolnica": prestolnica, "random_index": random_index}

        return self.render_template("hello.html", podatki)

class CalculateHandler(BaseHandler):
    def post(self):

        odgovor = self.request.get("prestolnica")
        random_index = int(self.request.get("random_index"))
        drzava = self.request.get("drzava")

        prestolnica = niz_prestolnic[random_index]
        pravilen_odgovor = prestolnica.ime



        podatki = {"pravilen_odgovor": pravilen_odgovor, "odgovor": odgovor, "drzava": drzava}



        return self.render_template("rezultat.html", podatki)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', CalculateHandler),
], debug=True)
