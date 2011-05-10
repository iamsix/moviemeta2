import cherrypy, xml.etree.ElementTree as ET
from cherrypy.lib.static import serve_file
import mymovies, sys, os, ConfigParser
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
    
    def unprocessed_movies(self): 
        
        root = ET.Element("movies")
        for movie in self.moviesdb:
            if not movie.HasXML:
                movietag = ET.SubElement(root, 'movie')
                ET.SubElement(movietag, 'LocalTitle').text = movie.LocalTitle
                ET.SubElement(movietag, 'ProductionYear').text = movie.ProductionYear
                ET.SubElement(movietag, 'Link').text = movie.ID
        ET.SubElement(root, 'unprocessed').text = str(self.unprocessedcount)
        output = '<?xml-stylesheet type="text/xsl" href="Templates/index.xsl"?>' + ET.tostring(root)
        return output
    
    def movie_list(self):
        root = ET.Element("movies")
        ET.SubElement(root, 'unprocessed').text = str(self.unprocessedcount)
        for movie in self.moviesdb:
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

def main():
    cherrypy.quickstart(MainProgram(), "/", 'cherrypy.conf')

if __name__ == '__main__':
    main()