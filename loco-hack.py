import gtk.gdk
from googlesearch.googlesearch import GoogleSearch
import os
import webbrowser
import urllib
from bs4 import BeautifulSoup
import urllib2
import re

w = gtk.gdk.get_default_root_window()
sz = w.get_size()
#print "The size of the window is %d x %d" % sz
pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
pb = pb.get_from_drawable(w,w.get_colormap(),1015,290,0,0,300,300)
if (pb != None):
    pb.save("screenshot.png","png")
    print "Screenshot saved to screenshot.png."
else:
    print "Unable to get the screenshot." 

os.system("convert -trim screenshot.png screenshot.png")
os.system("convert -resize 300% screenshot.png screenshot.png")
os.system("tesseract /home/elcot/screenshot.png loco001")
fi=open("loco001.txt","r")
m=fi.read()

m=''.join([i if ord(i) < 128 else ' ' for i in m])
m=re.sub(' +',' ',m)

if(m.find("?")!=-1):
  m=list(m.split("?"))
else:
  m=list(m.split("."))

url =str("+".join((m[0].lstrip()).split()))+"?"

n=m[1]
n=list((n.lstrip()).split("\n"))

url="http://www.google.com.tr/search?q={}".format(url)
chro= '/usr/bin/chromium %s'

headers={}
headers["User-Agent"]='Mozilla/5.0'
urls=urllib2.Request(url,headers=headers)
html = urllib2.urlopen(urls).read()
soup = BeautifulSoup(html)

# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
l=[]
for i in range(len(text)):
    if(text[i].isalpha() or text[i].isdigit() or text[i]==" "):
      l.append(text[i])
     
strr="".join(l)
strr=strr.lower()
fun=1

l=list(map(str,strr.split()))
#print(strr)
#print(url)
for i in n:
   if(i!="" and i!=" "):
     k=0; sco=[]
     for j in list(i.split()):
       kco=strr.count(j.lower())
       k+=kco
       sco.append(kco)
     if(k!=0):
         fun=0
     print sco,"\t",(i,k)


def simil(x,f):
  p=0
  for i in f:
    z=len(set(x) & set(i))
    if((z==len(x)-1 or z==len(i)-1) and abs(len(x)-len(i))<=2):
      p+=1
  return p


if(fun==1):
  for i in n:
    if(i!="" and i[0]!=" "):
       for j in list(i.split()):
         k=0
         k+=simil(j.lower(),l)
    print(i,k)

