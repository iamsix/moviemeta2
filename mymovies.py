import os, lxml.etree as ET, re

def scandirectory(self, path):
    for di in os.listdir(path):
        if os.path.isdir(os.path.join(path, di)):
            files = os.listdir(os.path.join(path, di))
            HasPoster = False
            HasBackdrop = False
            HasXML = False
            if "folder.jpg" in files: HasPoster = True
            if "backdrop.jpg" in files: HasBackdrop = True
            if "mymovies.xml" in files: HasXML = True
            if "mymovies.dna" in files:  
                continue
            else:
                for fi in files:
                    if True in [fi.find("." + x.strip()) !=-1 for x in self.config.get("general", "FileExtensions").split(",")] or HasXML:
                        mymovie = MyMovie(os.path.join(path, di, "mymovies.xml"))
                        Actors = [person.Name.strip().lower() for person in mymovie.Persons]
                        if not mymovie.HasXML:
                            self.unprocessedcount += 1
                        key = hex(hash(os.path.join(path, di)) & 0xffffffff)[2:10]
                        movie = movies(key, mymovie.SortTitle, mymovie.LocalTitle, mymovie.ProductionYear, os.path.join(path, di), mymovie.HasXML, mymovie.XMLComplete, mymovie.Genres,Actors, mymovie.IMDBrating, mymovie.Added, HasPoster, HasBackdrop)
                          
                        self.moviesdb.append(movie)  
                        break      

    
class movies:
    def __init__(self, ID, SortTitle, LocalTitle, ProductionYear, Dir, HasXML, XMLComplete, Genres, Actors, IMDBRating, DateAdded, HasPoster, HasBackdrop):
        self.SortTitle = SortTitle
        self.LocalTitle = LocalTitle
        self.ProductionYear = ProductionYear
        self._Dir = Dir
        self.HasXML = HasXML
        self.XMLComplete = XMLComplete
        self.Genres = Genres
        self.Actors = Actors
        self.IMDBRating = IMDBRating
        self.DateAdded = DateAdded
        self.ID = ID
        self.HasPoster = HasPoster
        self.HasBackdrop = HasBackdrop
    
    def __getitem__(self, key):
        if key == "SortTitle": return self.SortTitle.lower()
        else: raise KeyError
        pass
    
    @property
    def Dir(self):
        return self._Dir
    
class MyMovie(object):
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
    XMLpath = ""
    _HasXML = False
    
    @property
    def HasXML(self):
        return self._HasXML
    
    def __init__(self, Path):
        try:
            xml = open(Path)
            self._HasXML = True
            parser = ET.XMLParser(remove_blank_text=True)
            self.dom = ET.parse(xml, parser).getroot()
        except IOError:
            self._HasXML = False
            di = os.path.split(os.path.dirname(Path))[1]
            print di
            year = re.search("\([0-9]*\)", di)
            year = year.group(0).replace("(", "")
            year = year.replace(")", "")
            name = re.sub("\(.*\)", "", di).strip()
            name = re.sub("\[.*\]", "", name).strip()
            root = ET.Element("Title")
            ET.SubElement(root, 'LocalTitle').text = name
            ET.SubElement(root, 'SortTitle').text = name
            ET.SubElement(root, 'OriginalTitle')
            ET.SubElement(root, 'ProductionYear').text = year
            ET.SubElement(root, 'Added')
            ET.SubElement(root, 'RunningTime')
            ET.SubElement(root, 'IMDBrating')
            ET.SubElement(root, 'MPAARating')
            ET.SubElement(root, 'Description')
            ET.SubElement(root, 'Type')
            ET.SubElement(root, 'AspectRatio')
            ET.SubElement(root, 'LockData')
            ET.SubElement(root, 'IMDB')
            ET.SubElement(root, 'TMDbId')
            g = ET.SubElement(root, 'Genres')
            ET.SubElement(g, 'Genre')
            ps = ET.SubElement(root, 'Persons')
            p = ET.SubElement(ps, 'Person')
            ET.SubElement(p, 'Name')
            ET.SubElement(p, 'Type')
            ET.SubElement(p, 'Role')
            s = ET.SubElement(root, 'Studios')
            ET.SubElement(s, 'Studio')
            self.dom = root
            
        self.XMLpath = Path
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
            if g.text: genres.append(g.text)
        
        return genres   
    @Genres.setter
    def Genres(self, value):
        g = self.dom.find('Genres')
        g.clear()
        for Genre in value:
            ET.SubElement(g, 'Genre').text = Genre
    
    @property
    def Studios(self):
        studios = []
        elements = self.dom.findall('Studios/Studio')
        for s in elements:
            if s.text: studios.append(s.text)
        
        return studios       
    @Studios.setter
    def Studios(self, value): 
        if value:
            s = self.dom.find('Studios')
            s.clear()
            for Studio in value:
                ET.SubElement(s, 'Studio').text = Studio
    
    @property
    def Persons (self):
        persons = []
        elements = self.dom.findall('Persons/Person')
        for p in elements:
            name = ""
            type = ""
            role = ""
            if p.find('Name') is not None and p.find('Name').text:
                name = str(p.find('Name').text)
                if p.find('Type') is not None:
                    type = str(p.find('Type').text)
                if p.find('Role') is not None:
                    type = str(p.find('Role').text)
                        
                person = self.Person(name, type, role)
                persons.append(person)
                
        return persons   
    @Persons.setter
    def Persons(self, value):
        ps = self.dom.find('Persons')
        ps.clear()
        for Person in value:
            p = ET.SubElement(ps, 'Person')
            ET.SubElement(p, 'Name').text = Person['Name']
            ET.SubElement(p, 'Type').text = Person['Type']
            ET.SubElement(p, 'Role').text = Person['Role']
     
        
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
    
    def save(self):
        print self.XMLpath
        #Open in r+ and truncate() instead of 'w' because 'w' will raise an IOError on a hidden file
        try:
            xml = open(self.XMLpath, "r+")
            xml.truncate()
        except IOError:
            xml = open(self.XMLpath, "w+")   
        xml.write(ET.tostring(self.dom, pretty_print=True))
        xml.close()
        self._HasXML = True
        
    def loadFromDictionary(self, mmdict, replaceonlymissing = False):
        if (replaceonlymissing and not self.LocalTitle) or not replaceonlymissing:
            self.LocalTitle = mmdict['LocalTitle']
        
        if (replaceonlymissing and not self.SortTitle) or not replaceonlymissing:
            self.SortTitle = mmdict['SortTitle']
        
        if (replaceonlymissing and not self.OriginalTitle) or not replaceonlymissing:
            self.OriginalTitle = mmdict['OriginalTitle']
        
        if (replaceonlymissing and not self.ProductionYear) or not replaceonlymissing:
            self.ProductionYear = mmdict['ProductionYear']
        
        if (replaceonlymissing and not self.Added) or not replaceonlymissing:
            self.Added = mmdict['Added']
            
        if (replaceonlymissing and not self.RunningTime) or not replaceonlymissing:
            self.RunningTime = mmdict['RunningTime']
            
        if (replaceonlymissing and not self.IMDBrating) or (replaceonlymissing and self.IMDBrating == "0.0") or not replaceonlymissing:
            self.IMDBrating = mmdict['IMDBrating']
            
        if (replaceonlymissing and not self.MPAARating) or not replaceonlymissing:
            self.MPAARating = mmdict['MPAARating']
            
        if (replaceonlymissing and not self.Description) or not replaceonlymissing:
            self.Description = mmdict['Description']
            
        if (replaceonlymissing and not self.Type) or not replaceonlymissing:
            self.Type = mmdict['Type']
        
        if (replaceonlymissing and not self.AspectRatio) or not replaceonlymissing:
            self.AspectRatio = mmdict['AspectRatio']
        
        if (replaceonlymissing and not self.IMDB) or not replaceonlymissing:
            self.IMDB = mmdict['IMDB']
        
        if (replaceonlymissing and not self.TMDbId) or not replaceonlymissing:
            self.TMDbId = mmdict['TMDbId']
        
        ### need to add special appending code for these 3 that checks existing entries
        ### and adds them if they're not already on the list
        
        if (replaceonlymissing and not self.Genres) or not replaceonlymissing:
            self.Genres = mmdict['Genres']
        
        if (replaceonlymissing and not self.Persons) or not replaceonlymissing:
            self.Persons = mmdict['Persons']
        
        if (replaceonlymissing and not self.Studios) or not replaceonlymissing:
            self.Studios = mmdict['Studios']
    