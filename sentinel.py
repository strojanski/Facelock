import random
import string
import os, os.path

import cherrypy


class StringGenerator(object):
    @cherrypy.expose
    def index(self, cas=0):
        if(cas):
            return open('set.html')
        return open('index.html')


    @cherrypy.expose
    def generate(self, cas):
        #open('set.html')
        return 'Spremenljivke: ' + cas


if __name__ == '__main__':
    cherrypy.quickstart(StringGenerator())
