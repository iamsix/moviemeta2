import urllib2, json, re
from BeautifulSoup import BeautifulSoup
import tools

def searchByTitle(title):
        #uses google instead of IMDB search because it's better and easier to parse
        url = ('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + urllib2.quote("site:imdb.com/title " + title))
        request = urllib2.Request(url, None, {'Referer': 'http://irc.00id.net'})
        response = urllib2.urlopen(request)

        results_json = json.load(response)
        results = results_json['responseData']['results']
        movieResults = []
        p = re.compile(r'<.*?>')    
        for result in results:
            if not re.search("TV [a-zA-Z]",result['titleNoFormatting']) and re.search("imdb.com/title/tt\\d{7}/$",result['url']):
                title = tools.decode_htmlentities(p.sub('',result['titleNoFormatting'].replace(" - IMDb", "")))
                content = tools.decode_htmlentities(p.sub('',result['content']))
                print result['content']
                imdbid = re.search("tt\\d{7}", result['url']).group(0)
                movieResults.append({"name":title, "desc":content, "id":imdbid})
                
        return movieResults
                   
searchByTitle.searchkw = "imdbtitle" 
searchByTitle.desc = "Search IMDb with Google by movie title"
    

class fetcher(object):
    datasource = "imdb"
    mediatype = "movie"
    imdbpage = None
    
    _identifier = ""
    def __init__ (self, identifier):
        self._identifier = identifier
        imdburl = ('http://www.imdb.com/title/' + identifier + '/')
        opener = urllib2.build_opener()
        opener.addheaders = [('User-Agent',"Opera/9.10 (YourMom 8.0)"),
                             ('Range', "bytes=0-40960")]
        pagetmp = opener.open(imdburl)
        self.imdbpage = BeautifulSoup(pagetmp.read())
        opener.close()
        
    @property
    def LocalTitle(self):
        movietitle = tools.decode_htmlentities(tools.remove_html_tags(str(self.imdbpage.find('title'))).replace(" - IMDb", ""))
        movietitle = re.sub("\(.*\)", "", movietitle).strip()
        return movietitle
    
    @property
    def OriginalTitle(self):
        if self.imdbpage.find("span", "title-extra") != None:
            otitle = self.imdbpage.find("span", "title-extra").text.replace("(original title)", "").strip()
            return otitle
        else:
            return self.LocalTitle
        
    @property
    def SortTitle(self):
        title = self.LocalTitle
        if title[0:4].lower() == "the ":
            title = title[4:] + ", The"
        if title[0:2].lower() == "a ":
            title = title[2:] + ", A"
        return title
    
    @property
    def ProductionYear(self):
        movietitle = tools.decode_htmlentities(tools.remove_html_tags(str(self.imdbpage.find('title'))).replace(" - IMDb", ""))
        movietitle = re.search("\(.*\)", movietitle).group(0).strip()
        return re.search("[1-2][0-9]{3}", movietitle).group(0).strip()
    
    @property
    def RunningTime(self):
        if self.imdbpage.find(text="Runtime:"):
            time = re.search("\d.*? min", unicode(self.imdbpage.find(text="Runtime:").parent.parent)).group(0).replace(" min", "").strip()
            #more needs to be done here
            #it might even be easier to do a regex digit search..
            return time
    
    @property
    def IMDBrating(self):
        return tools.remove_html_tags(str(self.imdbpage.find(id="star-bar-user-rate").b))
    
    @property
    def MPAARating(self):
        if self.imdbpage.find("img", attrs={'src' : re.compile("certificates\/us\/")}):
            rating = self.imdbpage.find("img", attrs={'src' : re.compile("certificates\/us\/")})
            rating = rating['alt']
            return rating
        else:
            return "NR"
    
    @property
    def AspectRatio(self):
        if self.imdbpage.find(text="Aspect Ratio:"):
            ar = re.search("\d\.\d{2} : 1", unicode(self.imdbpage.find(text="Aspect Ratio:").parent.parent)).group(0).replace(" : ", ":").strip()
            return ar

    @property
    def Genres(self):
        if self.imdbpage.find(text="Genres:"):
            genres = self.imdbpage.find(text="Genres:").parent.parent
            genres = genres.findAll("a")
            genrelist = []
            for genre in genres:
                genrelist.append(genre.text)
            return genrelist

    @property
    def Studios(self):
        if self.imdbpage.find(text="Production Co:"):
            studios = self.imdbpage.find(text="Production Co:").parent.parent
            studios = studios.findAll("a")
            studiolist = []
            for studio in studios:
                if studio.text != "See more":
                    studiolist.append(studio.text)
            return studiolist

    @property
    def Persons(self):
        personlist = []
        if self.imdbpage.find(text=re.compile("Directors?:")):
            directors = self.imdbpage.find(text=re.compile("Directors?:")).parent.parent
            directors = directors.findAll("a")
            for person in directors:
                if person.text.find('more credits') == -1:
                    personlist.append({"Name" : person.text, "Type" : "Director", "Role" : ""})
            
        if self.imdbpage.find("table", "cast_list"):
            cast = self.imdbpage.find("table", "cast_list")
            cast = cast.findAll('tr')
            for person in cast:
                name = tools.decode_htmlentities(tools.remove_html_tags(str(person.find('td', 'name'))).strip()).replace("\n", " ")
                role = tools.decode_htmlentities(tools.remove_html_tags(str(person.find('td', 'character'))).strip()).replace("\n", " ")
                name = re.sub('\s+', ' ', name)
                role = re.sub('\s+', ' ', role)
                if name != "None":
                    if role == "None": role = ""
                    personlist.append({"Name" : name, "Type" : "Actor", "Role" : role})
        
        return personlist
        
    @property
    def IMDB(self):
        return self._identifier
    
    @property
    def Description(self):
        page = self.imdbpage.find(id="overview-top")
        if len(page.findAll('p')) == 2:
    
            summary = str(page.findAll('p')[1])
    
            removelink = re.compile(r'\<a.*\/a\>')
            summary = removelink.sub('',summary)
            summary = tools.remove_html_tags(summary)
            summary = summary.replace('&raquo;', "")
            summary = tools.decode_htmlentities(summary.decode("utf-8", 'ignore'))
            summary = summary.replace("\n", " ")
            return summary
    
    def getByIMDBID(self, ID):
        pass
    getByIMDBID.datagetter = "imdbid"
    getByIMDBID.desc = "Get IMDb data by ID"
    
    
