import json, urllib2, time

def searchByTitle(title):
    try:
        apikey = open("tmdbapikey").read()
        url = 'http://api.themoviedb.org/2.1/Movie.search/en/json/%s/%s' % (apikey, urllib2.quote(title))
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)"),
                             ('Range', "bytes=0-40960")]
        pagetmp = opener.open(url).read()
        tmdbjson = json.loads(pagetmp)
        opener.close()
        movieResults = []
        for movie in tmdbjson:
            if movie == "Nothing found.": break
            if 'released' in movie:   
                year = time.strftime("%Y", time.strptime(movie['released'], "%Y-%m-%d"))
            else: year = ""
            name = movie['name'] + " (%s)" % year
            desc = movie['overview']
            id = "TMDbId=%s&IMDB=%s" % (str(movie['id']), movie['imdb_id'])
            movieResults.append({"name": name, "desc": desc, "id": id})
        return movieResults
    except Exception as inst:
        print inst

searchByTitle.searchkw = "tmdbtitle" 
searchByTitle.desc = "Search themoviedb.org by movie title"

class fetcher(object):
    datasource = "tmdb"
    mediatype = "movie"
    tmdbjson = None
    identifiers = ["TMDbId", "IMDB"]
    HasData = False
    
    _identifier = ""
    def __init__ (self, identifier):
        #print identifier
        self._identifier = identifier
        apikey = open("tmdbapikey").read()
        
        if 'TMDbId' in identifier:
            url = "http://api.themoviedb.org/2.1/Movie.getInfo/en/json/%s/%s" % (apikey, urllib2.quote(identifier['TMDbId']))
        elif 'IMDB' in identifier:
            url = "http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/%s/%s" % (apikey, urllib2.quote(identifier['IMDB']))   
        else:
            self.HasData = False 
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)"),
                             ('Range', "bytes=0-40960")]
        pagetmp = opener.open(url).read()
        self.tmdbjson = json.loads(pagetmp)
        
        self.tmdbjson = self.tmdbjson[0]

        opener.close()
        if self.tmdbjson == "Nothing found.":
            self.HasData = False
        else:
            self.HasData = True
    
#    @property
#    def AspectRatio(self):
#        return None
    
    @property
    def LocalTitle(self):
        return self.tmdbjson['name']
    
    @property
    def OriginalTitle(self):
        return self.tmdbjson['original_name']
    
    @property
    def SortTitle(self):
        if self.tmdbjson['alternative_name']:
            title = self.tmdbjson['alternative_name']
        else:
            title = self.LocalTitle
            if title[0:4].lower() == "the ":
                title = title[4:] + ", The"
            if title[0:2].lower() == "a ":
                title = title[2:] + ", A"
        return title
    
    @property
    def ProductionYear(self):
        return time.strftime("%Y", time.strptime(self.tmdbjson['released'], "%Y-%m-%d"))

    @property
    def RunningTime(self):
        if self.tmdbjson['runtime']:
            return str(self.tmdbjson['runtime'])
    
    @property
    def MPAARating(self):
        return self.tmdbjson['certification']
    
    @property
    def Description(self):
        return self.tmdbjson['overview']
    
    @property
    def IMDBrating(self):
        return str(self.tmdbjson['rating'])
    
    @property
    def Genres(self):
        genres = []
        if 'genres' in self.tmdbjson:
            for genre in self.tmdbjson['genres']:
                genres.append(genre['name'])
        print genres
        return genres
    
    @property
    def Studios(self):
        studios = []
        if 'studios' in self.tmdbjson:
            for studio in self.tmdbjson['studios']:
                studios.append(studio['name'])
        return studios
    
    @property
    def IMDB(self):
        return self.tmdbjson['imdb_id']
    
    @property
    def TMDbId(self):
        return str(self.tmdbjson['id'])
    
    @property
    def Persons (self):
        if 'cast' in self.tmdbjson:
            persons = []
            for person in self.tmdbjson['cast']:
                if person['job'] == "Actor" or person['job'] == "Director":
                    persons.append({"Name" : person['name'], "Type" : person['job'], "Role" : person['character']})
                    
            return persons
    
    @property
    def posterimages(self):
        return self.imageURLs("poster")
    
    @property
    def backdropimages(self):
        return self.imageURLs("backdrop")
    
    def imageURLs(self, imgtype): 
        images = []
        imgid = 0       
        for img in self.tmdbjson[imgtype + "s"]:
            img = img['image']
            if img["size"] == "original":
                images.append({"thumb" : "", "full" : img['url'], "imgtype" : imgtype, "imageid" : imgid, "resolution" : str(img['width']) + "x" + str(img['height']) })
            if img["size"] == "thumb":
                images[imgid]['thumb'] = img['url']
                imgid += 1
        return images