from nntplib import NNTP
from time import strftime, time, localtime
from email import message_from_string
from urllib import urlopen
import textwrap
import re

day = 24 * 60 * 60 #Number of seconds in a day

def wrap(string, max=70):
    return '\n'.join(textwrap.wrap(string)) + '\n'
    
    
class NewsItem:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        
class NewsAgent:
    def __init__(self):
        self.sources = []
        self.destinations = []
        
    def addSource(self, source):
        self.sources.append(source)
        
    def addDestination(self, dest):
        self.destinations.append(dest)
        
    def distribute(self):
        items = []
        for source in self.sources:
            items.extend(source.getItems())
        for dest in self.destinations:
            dest.receiveItems(items)
            
class NNTPSource:
    def __init__(self, servername, group, window):
        self.servername = servername
        self.group = group
        self.window = window
        
    def getItems(self):
        start = localtime(time() - self.window*day)
        date = strftime('%y%m%d', start)
        hour = strftime('%H%M%S', start)

        server = NNTP(self.servername)

        ids = server.newnews(self.group, date, hour)[1]

        for id in ids:
            lines = server.article(id)[3]
            message = message_from_string('\n'.join(lines))
            
            title = message['subject']
            body = message.get_payload()
            if message.is_multipart():
                body = body[0]
                
            yield NewsItem(title, body)
            
        server.quit()

class SimpleWebSource:
    def __init__(self, url, titlePattern, bodyPattern):
        self.url = url
        self.titlePattern = re.compile(titlePattern)
        self.bodyPattern = re.compile(bodyPattern)
        
    def getItems(self):
        text = urlopen(self.url).read()
        titles = self.titlePattern.findall(text)
        bodies = self.bodyPattern.findall(text)
        for title, body in zip(titles, bodies):
            yield NewsItem(title, wrap(body))
 
class Destination:
    def receiveItems(self, items):
        pass
        
class PlainDestination(Destination):
    def receiveItems(self, items):
        for item in items:
            print(item.title)
            print('-'*len(item.title))
            print('\n'.join(item.body))
        
class HTMLDestination(Destination):
    def __init__(self, filename):
        self.filename = filename
        
    def receiveItems(self, items):
        out = open(self.filename, 'w')
        out.write("""
        <html>
            <head>
                <title>Today's News</title>
            </head>
            <body>
                <h1>Today's News</h1>
        """)
        
        out.write("<ul>")
        id = 0
        for item in items:
            id += 1
            out.write('<li><a href="#%i">%s</a></li>'%(id, item.title))
        out.write("</ul>")
        
        id = 0
        for item in items:
            id += 1
            out.write('<h2><a href="%i">%s</a></h2>'%(id, item.title))
            out.write('<pre>%s</pre>'%(item.body))
            
        out.write("""
            </body>
        </html>    
        """)
       
def runDefaultSetup():
    agent = NewsAgent()
    bbc_url = 'http://news.bbc.co.uk/text_only.stm'
    bbc_title = r'(?s)a href="[^"]*\s*<b>\s*(.*?)\s*</b>">'
    bbc_body = r'(?s)</a>\s*<br />\s*(.*?)\s*<'
    bbc = SimpleWebSource(bbc_url, bbc_title, bbc_body)
    
    agent.addSource(bbc)
    
    nntp_servername = 'news-archive.icm.edu.pl'
    nntp_group = 'junk'
    nntp_window = 7
    nntp_source = NNTPSource(nntp_servername, nntp_group, nntp_window)
    
    agent.addSource(nntp_source)
    
    agent.addDestination(PlainDestination())
    agent.addDestination(HTMLDestination('news.html'))
    
    agent.distribute()
    
if __name__ == "__main__":
    runDefaultSetup()