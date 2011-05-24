#! /usr/bin/env python

import cherrypy, imp
import lxml.etree as ET
from cherrypy.lib.static import serve_file
from PIL import Image
import mymovies, sys, os, ConfigParser, urllib2, json, re
from operator import itemgetter

current_dir = os.path.dirname(os.path.abspath(__file__))
class MainProgram:
    moviesdb = []
    unprocessedcount = 0
    config = None
    def __init__(self):
        cherrypy.config.update({'error_page.404': self.error_page_404})
        self.config = ConfigParser.ConfigParser()

        try:
            cfgfile = open("main.conf")
            self.config.readfp(cfgfile)
        except:
            self.config.add_section("general")
            self.config.set("general", "Directories", "")
            self.config.set("general", "FileExtensions", "avi,mkv,mp4,ts")
            self.config.write(open("main.conf", "w"))
        
        filenames = []
        for fn in os.listdir('./fetchmodules'):
            if fn.endswith('.py') and not fn.startswith('_'):
                filenames.append(os.path.join('./fetchmodules', fn))
        
        self.fetchers = {}
        self.moviesearchers = {}
        self.moviedatafetchers = {}
               
        for filename in filenames:
            name = os.path.basename(filename)[:-3]
            try:
                module = imp.load_source(name, filename)
            except Exception as inst: 
                print "Error loading module " + name + " : " + str(inst)
            else:
                self.fetchers[module.fetcher.datasource] = module.fetcher
                for name, func in vars(module.fetcher).iteritems():
                    if hasattr(func, 'searchkw'):
                        searchkw = str(func.searchkw)
                        self.moviesearchers[searchkw] = func
        
        self.refresh_movielist()

        
        
    def refresh_movielist(self):
        self.unprocessedcount = 0
        self.moviesdb = []
        for dir in [d.strip() for d in self.config.get("general","Directories").split(",")]:
            if dir: mymovies.scandirectory(self, dir)
        self.moviesdb.sort(key=itemgetter("SortTitle"))
#        for movie in self.moviesdb:
#            movie.ID = str(self.moviesdb.index(movie))
    refresh_movielist.exposed = True
    
    def unprocessed_movies(self): 
        
        root = ET.Element("movies")
        
        moviecount = 0
        for movie in self.moviesdb:
            if not movie.HasXML:
                moviecount +=1
                movietag = ET.SubElement(root, 'movie')
                ET.SubElement(movietag, 'LocalTitle').text = movie.LocalTitle
                ET.SubElement(movietag, 'ProductionYear').text = movie.ProductionYear
                ET.SubElement(movietag, 'Link').text = movie.ID
        ET.SubElement(root, 'unprocessed').text = str(self.unprocessedcount)
        ET.SubElement(root, 'listname').text = "Unprocessed Movies (%s)" % moviecount
        
        transform = ET.XSLT(ET.XML(open('Templates/index.xsl').read()))
        editcontrols = (cherrypy.request.remote.ip == "192.168.1.100")
        doc = transform(root, EditControls="'%s'" % editcontrols)
        return str(doc)
    
    def movie_list(self):
        root = ET.Element("movies")
        ET.SubElement(root, 'unprocessed').text = str(self.unprocessedcount)
        
        moviecount = 0
        for movie in self.moviesdb:
            moviecount +=1
            movietag = ET.SubElement(root, 'movie')
            if not movie.HasXML: 
                ET.SubElement(movietag, 'XML').text = "none"
            elif movie.XMLComplete: 
                ET.SubElement(movietag, 'XML').text = "complete"
            else: 
                ET.SubElement(movietag, 'XML').text = "incomplete"
            ET.SubElement(movietag, 'LocalTitle').text = movie.LocalTitle
            ET.SubElement(movietag, 'ProductionYear').text = movie.ProductionYear
            ET.SubElement(movietag, 'Link').text = movie.ID
            ET.SubElement(movietag, 'Path').text = movie.Dir.decode("utf-8", "ignore")
            
        ET.SubElement(root, 'listname').text = "Movie List (%s)" % moviecount
        #indent(root)
        transform = ET.XSLT(ET.XML(open('Templates/index.xsl').read()))
        editcontrols = (cherrypy.request.remote.ip == "192.168.1.100")
        doc = transform(root, EditControls="'%s'" % editcontrols)
        return str(doc)
    
    def list(self):
        return self.movie_list()
    list.exposed = True
    
    def settings(self):
        root = ET.Element("Settings")
        
       
        x = 0
        for dir in [d.strip() for d in self.config.get("general","Directories").split(",")]:
            x += 1
            moviedir = ET.SubElement(root, 'MovieDir')
            ET.SubElement(moviedir, "Dir").text = dir
            ET.SubElement(moviedir, "DirID").text = "dir" + str(x)
        
        ET.SubElement(root, 'moviedircount').text = str(x + 1)
        ET.SubElement(root, 'unprocessed').text = str(self.unprocessedcount)
        ET.SubElement(root, 'fileExtensions').text = self.config.get("general","FileExtensions")
        #indent(root)
        output = '<?xml-stylesheet type="text/xsl" href="/Templates/settings.xsl"?>\n' + ET.tostring(root)
        response = cherrypy.response
        response.headers['Content-Type'] = 'text/xml'
        return output
    settings.exposed = True

    def savesettings(self, **kwargs):
        self.config.set("general", "Directories", ",".join(kwargs["mdirectory"]))
        self.config.write(open("main.conf", "w"))
    savesettings.exposed = True
    
    def buildmovielist(self, movie, XMLRoot):
        pass

    
    def Person(self, Name):
        root = ET.Element("movies")
        ET.SubElement(root, 'unprocessed').text = str(self.unprocessedcount)
        moviecount = 0
        for movie in self.moviesdb:
            if Name.strip().lower() in movie.Actors:
                moviecount += 1
                movietag = ET.SubElement(root, 'movie')
                if not movie.HasXML: 
                    ET.SubElement(movietag, 'XML').text = "none"
                elif movie.XMLComplete: 
                    ET.SubElement(movietag, 'XML').text = "complete"
                else: 
                    ET.SubElement(movietag, 'XML').text = "incomplete"
                ET.SubElement(movietag, 'LocalTitle').text = movie.LocalTitle
                ET.SubElement(movietag, 'ProductionYear').text = movie.ProductionYear
                ET.SubElement(movietag, 'Link').text = movie.ID
                ET.SubElement(movietag, 'Path').text = movie.Dir.decode("utf-8", "ignore")
        
        imdburl = google_url("site:imdb.com/name " + Name, "imdb.com/name/nm[0-9]*/")
        
        title = ET.SubElement(root, 'listname') #.text = 'Movies with %s (%s)' % (Name, moviecount)
        ET.SubElement(title, 'a', {"href" : imdburl}).text = 'Movies with %s (%s)' % (Name, moviecount)
        #indent(root)
        output = '<?xml-stylesheet type="text/xsl" href="/Templates/index.xsl"?>\n' + ET.tostring(root)
        response = cherrypy.response
        response.headers['Content-Type'] = 'text/xml'
        return output
    Person.exposed = True
    
    def Genre(self, Genre):
        root = ET.Element("movies")
        ET.SubElement(root, 'unprocessed').text = str(self.unprocessedcount)
        moviecount = 0
        for movie in self.moviesdb:
            if Genre.strip() in movie.Genres:
                moviecount += 1
                print "cats"
                movietag = ET.SubElement(root, 'movie')
                if not movie.HasXML: 
                    ET.SubElement(movietag, 'XML').text = "none"
                elif movie.XMLComplete: 
                    ET.SubElement(movietag, 'XML').text = "complete"
                else: 
                    ET.SubElement(movietag, 'XML').text = "incomplete"
                ET.SubElement(movietag, 'LocalTitle').text = movie.LocalTitle
                ET.SubElement(movietag, 'ProductionYear').text = movie.ProductionYear
                ET.SubElement(movietag, 'Link').text = movie.ID
                ET.SubElement(movietag, 'Path').text = movie.Dir.decode("utf-8", "ignore")
        
        ET.SubElement(root, 'listname').text = "%s Movies (%s)" % (Genre, moviecount)
        #indent(root)
        output = '<?xml-stylesheet type="text/xsl" href="/Templates/index.xsl"?>\n' + ET.tostring(root)
        response = cherrypy.response
        response.headers['Content-Type'] = 'text/xml'
        return output
    Genre.exposed = True
        
    def validatedirectory(self, dir):
        response = cherrypy.response
        if os.path.isdir(dir):
            response.status = 200
        else:
            response.status = 404
        return ""
    validatedirectory.exposed = True
    
    def searchsuggestions(self, search):
        output = ""
        if len(search) >= 1:
            output = '<ul style="list-style-type: none; padding: 0; margin: 0;">'
            for movie in self.moviesdb:
                if re.search("\\b" + search, movie.LocalTitle, re.IGNORECASE):
                    link = "/movie/" + movie.ID
                    name = "%s (%s)" % (movie.LocalTitle, movie.ProductionYear)
                    if not movie.HasXML: 
                        xml = "movieXMLnone"
                    elif movie.XMLComplete: 
                        xml = "movieXMLcomplete"
                    else: 
                        xml = "movieXMLincomplete"
                    output = output + '<a href="%s" class="%s"><li style="padding-left: 5px; padding-right: 5px;">%s</li></a>' % (link, xml, name)
            if output == '<ul style="list-style-type: none; padding: 0; margin: 0;">': 
                output = "No movies found"
            else:
                output = output + '</ul>'
            return output
    searchsuggestions.exposed = True
    
    def movie(self, movieid, filename=None):
        dbmovie = None 
        for m in self.moviesdb:
            if m.ID == movieid: dbmovie = m
        response = cherrypy.response
        if dbmovie:
            if filename == "folder.jpg":
                if os.path.isfile(os.path.join(dbmovie.Dir, filename)):
                    img = Image.open(os.path.join(dbmovie.Dir, filename))
                    response.headers['Content-Type'] = 'image/jpg'
                    img.thumbnail((180,270), Image.ANTIALIAS)
                    return img.tostring('jpeg','RGB')
                    #return serve_file(os.path.join(self.moviesdb[int(movieid)].Dir, filename), content_type='image/jpg')
                else:
                    
                    return serve_file(os.path.join(os.getcwd(), "Images", "noposter.png"), content_type='image/png')
            elif filename == "backdrop.jpg":
                if os.path.isfile(os.path.join(dbmovie.Dir, filename)):
                    img = Image.open(os.path.join(dbmovie.Dir, filename))
                    response.headers['Content-Type'] = 'image/jpg'
                    img.thumbnail((450,250), Image.ANTIALIAS)
                    return img.tostring('jpeg','RGB')
                    #return serve_file(os.path.join(self.moviesdb[int(movieid)].Dir, filename), content_type='image/jpg')
                else:
                    return serve_file(os.path.join(os.getcwd(), "Images", "nobackdrop.png"), content_type='image/png')
            elif filename == "nfo":
                pass
            
            #if self.moviesdb[int(movieid)].HasXML:
            movie = mymovies.MyMovie(os.path.join(dbmovie.Dir, "mymovies.xml"))
            ET.SubElement(movie.dom, 'unprocessed').text = str(self.unprocessedcount)
            ET.SubElement(movie.dom, 'movieID').text = dbmovie.ID
            transform = ET.XSLT(ET.XML(open('Templates/moviepage.xsl').read()))
            editcontrols = (cherrypy.request.remote.ip == "192.168.1.100")
            doc = transform(movie.dom, EditControls="'%s'" % editcontrols)
    
            return str(doc)
        else:
            pass

    movie.exposed = True
    
    def error_page_404(self, status, message, traceback, version):
        if message.find("ImagesByName") != -1:
            return serve_file(os.path.join(os.getcwd(), "Images", "noactorpic.png"), content_type='image/png')
        else:
            return "%s\n%s\n%s\n" % (status, message, traceback)
    
    def index(self): 
        return self.unprocessed_movies()
    index.exposed = True
    
    def saveMovieXML(self, movieID):
        #Saves an edit page back to the mymovies.xml
        #the form is returned back as JSON with properties of every mymovies element.
        for m in self.moviesdb:
            if m.ID == movieID: dbmovie = m
        jsonBody = cherrypy.request.body.read()
        #TODO - Fix this remote IP
        if cherrypy.request.remote.ip == "192.168.1.100":
            mm = mymovies.MyMovie(os.path.join(dbmovie.Dir, "mymovies.xml"))
            mm.loadFromDictionary(json.loads(jsonBody))
            mm.save() #disabled for testing purposes
        else:
            cherrypy.response.status = 403
            return "You are not authorized to edit metadata"
        #print 
        #root = ET.fromstring(xmlBody)
        
        
        pass
    saveMovieXML.exposed = True
    
    def getMovieXML(self, movieID):
        #Returns pure XML copies of the requested xml element
        #Can return the full children of an XML element
        for m in self.moviesdb:
            if m.ID == movieID: dbmovie = m

        if cherrypy.request.remote.ip == "192.168.1.100":
            try: 
                open(os.path.join(dbmovie.Dir, "mymovies.xml"))
                return serve_file(os.path.join(dbmovie.Dir, "mymovies.xml"), content_type='text/xml')
            except:
                movie = mymovies.MyMovie(os.path.join(dbmovie.Dir, "mymovies.xml"))
                response = cherrypy.response
                response.headers['Content-Type'] = 'text/xml'
                return ET.tostring(movie.dom)
        else:
            cherrypy.response.status = 403
            return "You are not authorized to edit metadata"
    getMovieXML.exposed = True
    
    def fetchmedia(self, movieid, type, identifier):
        fetcher = self.fetchers['imdb'](identifier)
        results = fetcher.searchByTitle(identifier)
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'
        return json.JSONEncoder().encode(results)
    fetchmedia.exposed = True
    
    def exit(self):
        sys.exit(0)
    exit.exposed = True
    
def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
        
def google_url(searchterm, regexstring):
    #uses google to get a URL matching the regex string
    try:
        url = ('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + urllib2.quote(searchterm))
        request = urllib2.Request(url, None, {'Referer': 'http://irc.00id.net'})
        response = urllib2.urlopen(request)

        results_json = json.load(response)
        results = results_json['responseData']['results']
    
        for result in results:
            m = re.search(regexstring,result['url'])   
            if (m):
                url = result['url']
                url = url.replace('%25','%')
                return url
        return
    except:
        return



def main():
    cherrypy.quickstart(MainProgram(), "/", 'cherrypy.conf')

if __name__ == '__main__':
    main()