import re 
from htmlentitydefs import name2codepoint as n2cp

config = None

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
    
    
def remove_html_tags(data):
    #removes all html tags from a given string
    p = re.compile(r'<.*?>')
    return p.sub('', data)