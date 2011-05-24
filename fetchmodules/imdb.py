import urllib2, json, re
from htmlentitydefs import name2codepoint as n2cp

class fetcher(object):
    datasource = "imdb"
    mediatype = "movie"
    
    _identifier = ""
    def __init__ (self, identifier):
        self._identifier = identifier
        
    def searchByTitle(self, title):
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
                title = decode_htmlentities(p.sub('',result['titleNoFormatting'].replace(" - IMDb", "")))
                content = decode_htmlentities(p.sub('',result['content']))
                print result['content']
                imdbid = re.search("tt\\d{7}", result['url']).group(0)
                movieResults.append({"name":title, "desc":content, "id":imdbid})
                
        return movieResults
                   
    searchByTitle.searchkw = "imdbtitle" 
    searchByTitle.searchdesc = "Search IMDB by Title"
    
    def getByIMDBID(self, ID):
        pass
    getByIMDBID.searchkw = "imdbid"
    getByIMDBID.searchdesc = "Get IMDB data by ID"
    
    
def decode_htmlentities(string):
    #decodes things like &amp
    entity_re = re.compile("&(#?)(x?)(\w+);")
    return entity_re.subn(substitute_entity, string)[0]

def substitute_entity(match):
    try:
        ent = match.group(3)
        
        if match.group(1) == "#":
            if match.group(2) == '':
                return unichr(int(ent))
            elif match.group(2) == 'x':
                return unichr(int('0x'+ent, 16))
        else:
            cp = n2cp.get(ent)
        
            if cp:
                return unichr(cp)
            else:
                return match.group()
    except:
        return ""