import random
import string
import os, os.path

import cherrypy


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def generate(self, cas, cas1, cas2, cas3):
        print(self)
        return 'Spremenljivke: ' + cas + ' '+ cas1 + ' ' + cas2 + ' ' + cas3


if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())
