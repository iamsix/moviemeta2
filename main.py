#! /usr/bin/env python

import cherrypy, imp, time, cStringIO, traceback
import lxml.etree as ET
from cherrypy.lib.static import serve_file
from PIL import Image
import mymovies, sys, os, ConfigParser, urllib2, json, re, thread
from operator import itemgetter

#current_dir = os.path.dirname(os.path.abspath(__file__))
class MainProgram:
    moviesdb = []
    unprocessedcount = 0
    config = None
    def __init__(self): 
        cherrypy.config.update({'error_page.404': self.error_page_404})
        self.config = ConfigParser.ConfigParser()

        try:
            self.config.optionxform = str
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
                for name, func in vars(module).iteritems():
                    if hasattr(func, 'searchkw'):
                        searchkw = str(func.searchkw)
                        self.moviesearchers[searchkw] = func
        
        thread.start_new_thread(self.autoprocessnew, ()) 


        
        
    def refresh_movielist(self): 
        print "SUPERCAAAAAATS"
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
        editcontrols = (cherrypy.request.remote.ip == cherrypy.config.get("server.socket_host"))
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
        editcontrols = (cherrypy.request.remote.ip == cherrypy.config.get("server.socket_host"))
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
        ET.SubElement(title, 'a', {"href" : imdburl}).text = 'Movies with %s (%s)' % (Name.decode('UTF-8'), moviecount)
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
                files = os.listdir(dbmovie.Dir)
                for fi in files:
                    ext = os.path.splitext(fi)[1]
                    if ext.lower() == ".nfo":
                        return serve_file(os.path.join(dbmovie.Dir, fi), content_type='text/plain')
            
            #if self.moviesdb[int(movieid)].HasXML:
            movie = mymovies.MyMovie(os.path.join(dbmovie.Dir, "mymovies.xml"))
            ET.SubElement(movie.dom, 'unprocessed').text = str(self.unprocessedcount)
            ET.SubElement(movie.dom, 'movieID').text = dbmovie.ID
            transform = ET.XSLT(ET.XML(open('Templates/moviepage.xsl').read()))
            editcontrols = (cherrypy.request.remote.ip == cherrypy.config.get("server.socket_host"))
            doc = transform(movie.dom, EditControls="'%s'" % editcontrols)
    
            return str(doc)
        else:
            pass

    movie.exposed = True
    
    def error_page_404(self, status, message, tr, version):
        if message.find("ImagesByName") != -1:
            return serve_file(os.path.join(os.getcwd(), "Images", "noactorpic.png"), content_type='image/png')
        else:
            return "%s\n%s\n%s\n" % (status, message, tr)
    
    def index(self): 
        return self.unprocessed_movies()
    index.exposed = True
    
    def saveMovieXML(self, movieID):
        #Saves an edit page back to the mymovies.xml
        #the form is returned back as JSON with properties of every mymovies element.
        #TODO - Fix this remote IP
        if cherrypy.request.remote.ip == cherrypy.config.get("server.socket_host"):
            jsonBody = json.loads(cherrypy.request.body.read())
            for m in self.moviesdb:
                if m.ID == movieID: dbmovie = m
            self.saveXML(jsonBody, dbmovie)

        else:
            cherrypy.response.status = 403
            return "You are not authorized to edit metadata"
        #print 
        #root = ET.fromstring(xmlBody)
        
        
        pass
    saveMovieXML.exposed = True
    
    def saveXML(self, mymovieDICT, dbmovie):
            mm = mymovies.MyMovie(os.path.join(dbmovie.Dir, "mymovies.xml"))
            mm.loadFromDictionary(mymovieDICT)
            mm.save() #disabled for testing purposes
            
            if not dbmovie.HasXML: self.unprocessedcount -= 1
            dbmovie.LocalTitle = mm.LocalTitle
            dbmovie.SortTitle = mm.SortTitle
            dbmovie.ProductionYear = mm.ProductionYear
            dbmovie.HasXML = True
            dbmovie.Genres = mm.Genres
            dbmovie.XMLComplete = mm.XMLComplete
            self.moviesdb.sort(key=itemgetter("SortTitle")) 
    
    def getMovieXML(self, movieID):
        #Returns pure XML copies of the requested xml element
        #Can return the full children of an XML element
        for m in self.moviesdb:
            if m.ID == movieID: dbmovie = m

        if cherrypy.request.remote.ip == cherrypy.config.get("server.socket_host"):
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
    
    def fetchmediasearch(self, movieid, identifier, searcher='imdbtitle'):
        for f in self.config.get("moviefetchers", "searcher").split(","):
            results = self.moviesearchers[f](identifier)
            if results: break
        #results = self.moviesearchers[str(searcher)](identifier)
        response = cherrypy.response
        response.headers['Content-Type'] = 'application/json'
        return json.JSONEncoder().encode(results)
    fetchmediasearch.exposed = True
    
    def fetchmetadata(self, movieid, replaceonlymissing=True, fetchimages=True, **identifier):
        for m in self.moviesdb:
            if m.ID == movieid: dbmovie = m
        if replaceonlymissing == "true": replaceonlymissing = True
        else: replaceonlymissing = False
        mmdata = self.metadatafetcher(dbmovie, identifier, fetchimages)
            
        mm = mymovies.MyMovie(os.path.join(dbmovie.Dir, "mymovies.xml"))
        mm.loadFromDictionary(mmdata, replaceonlymissing)

        response = cherrypy.response
        response.headers['Content-Type'] = 'text/xml'
        return ET.tostring(mm.dom)
    
    fetchmetadata.exposed = True
    
    def metadatafetcher(self, dbmovie, identifier, fetchimages=True):
        fetcher = {}
        for f in self.fetchers:
            if [id for id in identifier if id in self.fetchers[str(f)].identifiers]:
                fi = self.fetchers[str(f)](identifier)
                if fi.HasData:
                    fetcher[f] = fi 

        mmdata = {}
        for item,value in self.config.items("moviefetchers"):
            for f in value.split(','):
                if f in fetcher and hasattr(fetcher[f], item) and (item not in mmdata or mmdata[item] == ""):
                    prop = getattr(fetcher[f], item)
                    mmdata[item] = prop
        
        if mmdata: mmdata['Added'] = str(time.strftime("%m/%d/%Y %I:%M:%S %p", time.localtime()))
        #mmdata['Type'] = ""
        if 'tmdb' in fetcher: #REMOVE THIS HACK LATER
            if fetchimages and not dbmovie.HasPoster and fetcher['tmdb'].posterimages:
                self.downloadimage(fetcher['tmdb'].posterimages[0]['full'], os.path.join(dbmovie.Dir, "folder.jpg"))
                dbmovie.HasPoster = True
            if fetchimages and not dbmovie.HasBackdrop and fetcher['tmdb'].backdropimages:
                
                self.downloadimage(fetcher['tmdb'].backdropimages[0]['full'], os.path.join(dbmovie.Dir, "backdrop.jpg"))
                dbmovie.HasBackdrop = True 
                
        return mmdata    
    
    def fetchimagelist(self, movieid, imagetype, **kwargs):
        fetcher = self.fetchers['tmdb'](kwargs)
        results = []
        if imagetype=="poster":  
            results = fetcher.posterimages
            self.fetchimagelist.posters[movieid] = results
        if imagetype=="backdrop":
            results = fetcher.backdropimages
            self.fetchimagelist.backdrops[movieid] = results
        if results:
            print "THERE ARE %s RESULTS IN THE LIST" % len(results)
            response = cherrypy.response
            response.headers['Content-Type'] = 'application/json'
            return json.JSONEncoder().encode(results)
    fetchimagelist.exposed = True
    fetchimagelist.posters={}
    fetchimagelist.backdrops={}
    
    def fetchedpicthumbs(self, movieid, picture, imgtype):
        if imgtype == "poster":
            url = self.fetchimagelist.posters[movieid][int(picture)]['thumb']
        elif imgtype == "backdrop":
            url = self.fetchimagelist.backdrops[movieid][int(picture)]['thumb']
        print "cats " + url
        try:
            imgdata = urllib2.urlopen(url).read()
            img = Image.open(cStringIO.StringIO(imgdata))
            response = cherrypy.response
            response.headers['Content-Type'] = 'image/jpg' 
            response.headers['Pragma'] = 'no-cache'
            response.headers['Cache-Control'] = 'no-cache'
            img.thumbnail((155,155), Image.ANTIALIAS)
            return img.tostring('jpeg','RGB')
        except Exception as inst:
            print "ESDFJSDFJHSDFJKHSDKFHJDSKJHSDF" + str(inst)
    fetchedpicthumbs.exposed = True
    
    def savemovieimage(self, movieid, picture, imgtype):
        for m in self.moviesdb:
            if m.ID == movieid: dbmovie = m
        if imgtype=="poster":
            url = self.fetchimagelist.posters[movieid][int(picture)]['full']
            self.downloadimage(url, os.path.join(dbmovie.Dir, "folder.jpg"))
        if imgtype=="backdrop":
            url = self.fetchimagelist.backdrops[movieid][int(picture)]['full']
            self.downloadimage(url, os.path.join(dbmovie.Dir, "backdrop.jpg"))
    savemovieimage.exposed = True
    
    def downloadimage(self, imgurl, diskfilename):
        imgdata = urllib2.urlopen(imgurl).read()
        img = Image.open(cStringIO.StringIO(imgdata))
        try:
            file = open(diskfilename, "rb+")
            file.truncate()
        except IOError:
            file = open(diskfilename, "wb")
        img.save(file, "JPEG")
    
    
    def exit(self):
        sys.exit(0)
    exit.exposed = True
    
    
    def autoprocessnew(self):
        self.refresh_movielist()
        try:
            while True:
                print "CATS" 
                self.refresh_movielist()
                if self.unprocessedcount > 0:
                    for m in self.moviesdb:
                        if m.HasXML == False and m.ID not in self.autoprocessnew.failedcheck:
                            try:
                                title = (m.LocalTitle + " " + m.ProductionYear).strip()
                                response = json.loads(self.fetchmediasearch(m.ID, title))
                                #print response
                                if len(response) == 1: #given only one result, it's very likely it's the one the user wants
                                    did = {}
                                    for name,val in [id.split("=") for id in response[0]['id'].split("&")]:
                                        did[name] = val
                                    print did
                                    result = self.metadatafetcher(m, did, True)
                                    print result
                                    self.saveXML(result, m)
                                else:
                                    self.autoprocessnew.failedcheck.append(m.ID)
                            except Exception as inst:
                                self.autoprocessnew.failedcheck.append(m.ID)
                                print "innerautothing " + str(inst)
                                traceback.print_exc()
                time.sleep(120)
        except Exception as inst: 
            print "mainautothing " + str(inst)
    autoprocessnew.failedcheck = [] 
        
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
        return ""
    except:
        return ""



def main():
    cherrypy.quickstart(MainProgram(), "/", 'cherrypy.conf')

if __name__ == '__main__':
    main()