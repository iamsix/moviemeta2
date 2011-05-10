import os, xml.etree.ElementTree as ET, re

def scandirectory(self, path):
    moviedirectories = []
    for fn in os.listdir(path):
        if os.path.isdir(os.path.join(path, fn)):
            files = os.listdir(os.path.join(path, fn))
            
            if "mymovies.dna" in files:
                continue
            elif "mymovies.xml" in files:
                moviedirectories.append(fn)
            else:
                for fi in files:
                    if True in [fi.find("." + x.strip()) !=-1 for x in self.config.get("general", "FileExtensions").split(",")]:
                        moviedirectories.append(fn)
                        break
    
    
    for di in moviedirectories:
        
        try:
            mymovie = MyMovie(os.path.join(path, di, "mymovies.xml"))
            HasXML = True
            movie = movies(mymovie.SortTitle, mymovie.LocalTitle, mymovie.ProductionYear, os.path.join(path, di), HasXML, mymovie.XMLComplete, [],[])
        except Exception as inst:
            print inst
            self.unprocessedcount += 1
            HasXML = False
            year = re.search("\([0-9]*\)", di)
            year = year.group(0).replace("(", "")
            year = year.replace(")", "")
            di = re.sub("\(.*\)", "", di).strip()
            di = re.sub("\[.*\]", "", di).strip()
            movie = movies(di, di, year, os.path.join(path, di), HasXML, False, [],[])
        
        #ADD IMDB RATING TO MOVIES DB    
        self.moviesdb.append(movie)  
    
class movies:
    def __init__(self, SortTitle, LocalTitle, ProductionYear, Dir, HasXML, XMLComplete, Genres, Actors):
        self._SortTitle = SortTitle
        self._LocalTitle = LocalTitle
        self._ProductionYear = ProductionYear
        self._Dir = Dir
        self._HasXML = HasXML
        self._XMLComplete = XMLComplete
        self._Genres = Genres
        self._Actors = Actors
    
    def __getitem__(self, key):
        if key == "SortTitle": return self._SortTitle 
        else: raise KeyError
        pass
    
    @property
    def Dir(self):
        return self._Dir

    @property
    def ID(self):
        return str(self._ID)
    @ID.setter
    def ID(self, value):
        self._ID = value

    @property
    def LocalTitle(self):
        return self._LocalTitle
    @LocalTitle.setter
    def LocalTitle(self, value):
        self._LocalTitle = value
        
    @property
    def SortTitle(self):
        return self._LocalTitle
    @SortTitle.setter
    def SortTitle(self, value):
        self._SortTitle = value

    @property
    def ProductionYear(self):
        return self._ProductionYear
    @ProductionYear.setter
    def ProductionYear(self, value):
        self._ProductionYear = value
        
    @property
    def HasXML(self):
        return self._HasXML
    @HasXML.setter
    def HasXML(self, value):
        self._HasXML = value
        
    @property
    def XMLComplete(self):
        return self._XMLComplete
    @XMLComplete.setter
    def XMLComplete(self, value):
        self._XMLComplete = value
    
    @property
    def Genres(self):
        return self._Genres
    @Genres.setter
    def Genres(self, value):
        self._Genres = value
        
    @property
    def Actors(self):
        return self._Actors
    @Actors.setter
    def Actors(self, value):
        self._Actors = value
    
class MyMovie:
    class Person:
        def __init__(self, Name, Type, Role):
            self._Name = Name
            self._Type = Type
            self._Role = Role
        
        @property
        def Name (self):
            return self._Name
        
        @property
        def Type (self):
            return self._Type
        
        @property
        def Role (self):
            return self._Role
    
    dom = None
    def __init__(self, Path):
        xml = open(Path)
        self.dom = ET.parse(xml)
        #print tree.find('LocalTitle').text
        
    @property
    def LocalTitle(self):
        element = self.dom.find('LocalTitle')
        if element is not None:
            return element.text
        else:
            return ""
    @LocalTitle.setter
    def LocalTitle(self, value):
        self.dom.find('LocalTitle').text = value
        
    @property
    def SortTitle(self):
        element = self.dom.find('SortTitle')
        if element is not None:
            return element.text
        else:
            return ""
    @SortTitle.setter
    def SortTitle(self, value):
        self.dom.find('SortTitle').text = value

    @property
    def ProductionYear(self):
        element = self.dom.find('ProductionYear')
        if element is not None:
            return element.text
        else:
            return ""
    @ProductionYear.setter
    def ProductionYear(self, value):
        self.dom.find('ProductionYear').text = value
        
    @property
    def OriginalTitle(self):
        element = self.dom.find('OriginalTitle')
        if element is not None:
            return element.text
        else:
            return ""
    @OriginalTitle.setter
    def OriginalTitle(self, value):
        self.dom.find('OriginalTitle').text = value
        
    @property
    def Added(self):
        element = self.dom.find('Added')
        if element is not None:
            return element.text
        else:
            return ""
    @Added.setter
    def Added(self, value):
        self.dom.find('Added').text = value
        
    @property
    def RunningTime(self):
        element = self.dom.find('RunningTime')
        if element is not None:
            return element.text
        else:
            return ""
    @RunningTime.setter
    def RunningTime(self, value):
        self.dom.find('RunningTime').text = value
    
    @property
    def IMDBrating(self):
        element = self.dom.find('IMDBrating')
        if element is not None:
            return element.text
        else:
            return ""
    @IMDBrating.setter
    def IMDBrating(self, value):
        self.dom.find('IMDBrating').text = value
        
    @property
    def MPAARating(self):
        element = self.dom.find('MPAARating')
        if element is not None:
            return element.text
        else:
            return ""
    @MPAARating.setter
    def MPAARating(self, value):
        self.dom.find('MPAARating').text = value
        
    @property
    def Description(self):
        element = self.dom.find('Description')
        if element is not None:
            return element.text
        else:
            return ""
    @Description.setter
    def Description(self, value):
        self.dom.find('Description').text = value
    
    @property
    def Type(self):
        element = self.dom.find('Type')
        if element is not None:
            return element.text
        else:
            return ""
    @Type.setter
    def Type(self, value):
        self.dom.find('Type').text = value
    
    @property
    def AspectRatio(self):
        element = self.dom.find('AspectRatio')
        if element is not None:
            return element.text
        else:
            return ""
    @AspectRatio.setter
    def AspectRatio(self, value):
        self.dom.find('AspectRatio').text = value
        
    @property
    def IMDB(self):
        element = self.dom.find('IMDB')
        if element is not None:
            return element.text
        else:
            return ""
    @IMDB.setter
    def IMDB(self, value):
        self.dom.find('IMDB').text = value
        
    @property
    def TMDbId(self):
        element = self.dom.find('TMDbId')
        if element is not None:
            return element.text
        else:
            return ""
    @TMDbId.setter
    def TMDbId(self, value):
        self.dom.find('TMDbId').text = value
        
    @property
    def Genres(self):
        genres = []
        elements = self.dom.findall('Genres/Genre')
        for g in elements:
            genres.append(g.text)
        
        return genres
    
    @property
    def Studios(self):
        studios = []
        elements = self.dom.findall('Studios/Studio')
        for s in elements:
            studios.append(s.text)
        
        return studios
    
    @property
    def Persons (self):
        persons = []
        elements = self.dom.findall('Persons/Person')
        for p in elements:
            name = ""
            type = ""
            role = ""
            if p.find('Name') is not None:
                name = str(p.find('Name').text)
            if p.find('Type') is not None:
                type = str(p.find('Type').text)
            if p.find('Role') is not None:
                type = str(p.find('Role').text)
                    
            person = self.Person(name, type, role)
            persons.append(person)
        return persons
     
        
    @property
    def XMLComplete(self):
        #print self.IMDB
        if (self.LocalTitle and\
                self.OriginalTitle and\
                self.SortTitle and\
                self.Added and\
                self.ProductionYear and\
                self.RunningTime and\
                self.IMDBrating and\
                self.MPAARating and\
                self.Description and\
                self.Type and\
                self.AspectRatio and\
                self.IMDB and\
                self.TMDbId and\
                self.Genres and\
                self.Persons):
            return True
        else:
            return False
    