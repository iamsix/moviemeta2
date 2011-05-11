import cherrypy, xml.etree.ElementTree as ET
from cherrypy.lib.static import serve_file
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
        
        
        self.refresh_movielist()

        
        
    def refresh_movielist(self):
        self.unprocessedcount = 0
        self.moviesdb = []
        for dir in [d.strip() for d in self.config.get("general","Directories").split(",")]:
            if dir: mymovies.scandirectory(self, dir)
        self.moviesdb.sort(key=itemgetter("SortTitle"))
        for movie in self.moviesdb:
            movie.ID = str(self.moviesdb.index(movie))
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
        output = '<?xml-stylesheet type="text/xsl" href="Templates/index.xsl"?>' + ET.tostring(root)
        return output
    
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
        indent(root)
        output = '<?xml-stylesheet type="text/xsl" href="/Templates/index.xsl"?>\n' + ET.tostring(root)
        return output
    
    def list(self):
        response = cherrypy.response
        response.headers['Content-Type'] = 'text/xml'
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
        indent(root)
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
        indent(root)
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
        indent(root)
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
    
    def movie(self, movieid, filename=None):
        response = cherrypy.response
        if filename == "folder.jpg":
            if os.path.isfile(os.path.join(self.moviesdb[int(movieid)].Dir, filename)):
                return serve_file(os.path.join(self.moviesdb[int(movieid)].Dir, filename), content_type='image/jpg')
            else:
                
                return serve_file(os.path.join(os.getcwd(), "Images", "noposter.png"), content_type='image/png')
        if filename == "backdrop.jpg":
            if os.path.isfile(os.path.join(self.moviesdb[int(movieid)].Dir, filename)): 
                return serve_file(os.path.join(self.moviesdb[int(movieid)].Dir, filename), content_type='image/jpg')
            else:
                return serve_file(os.path.join(os.getcwd(), "Images", "nobackdrop.png"), content_type='image/png')
        if self.moviesdb[int(movieid)].HasXML:
            movie = open(os.path.join(self.moviesdb[int(movieid)].Dir, "mymovies.xml"))
            domroot = ET.parse(movie).getroot()
            ET.SubElement(domroot, 'unprocessed').text = str(self.unprocessedcount)
            ET.SubElement(domroot, 'movieID').text = self.moviesdb[int(movieid)].ID
            #ET.SubElement(domroot, 'poster').text = os.path.join(self.moviesdb[int(movieid)].Dir, "folder.jpg").replace("\\" ,"/")
            output = '<?xml-stylesheet type="text/xsl" href="/Templates/moviepage.xsl"?>\n' + ET.tostring(domroot)
        
        response.headers['Content-Type'] = 'text/xml'
        return output  

    movie.exposed = True
    
    def error_page_404(self, status, message, traceback, version):
        if message.find("ImagesByName") != -1:
            return serve_file(os.path.join(os.getcwd(), "Images", "noactorpic.png"), content_type='image/png')
        else:
            return "%s\n%s\n%s\n" % (status, message, traceback)
    
    def index(self): 
        response = cherrypy.response
        response.headers['Content-Type'] = 'text/xml'
        return self.unprocessed_movies()
        
    index.exposed = True
    
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