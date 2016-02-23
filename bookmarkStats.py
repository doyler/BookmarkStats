import collections

from bs4 import BeautifulSoup
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/

browser = "chrome"

with open ("./bookmarks_" + browser + ".html", "r") as myfile:
    html = myfile.read()

parsed_html = BeautifulSoup(html)

soup = BeautifulSoup(html, 'html.parser')

linkList = soup.find_all('a')

# Firefox only
for link in linkList[:]:
        if link['href'].startswith('place'):
            linkList.remove(link)

total = len(linkList)
print "Total number of bookmarks: " + str(total) + "\n"

if browser == 'chrome':
    headerList = soup.findAll('h3')
    headerList.pop(0) # Remove "Bookmarks Toolbar"

    for node in headerList:
        header = ''.join(node.findAll(text=True))
        s = node
        while getattr(s, 'name', None) != 'dl':
            s = s.nextSibling
        parents = len(node.findParents('dl')) - 2
        count = len(s.findAll('a'))
        percentage = "{0:.2f}%".format(((count + 0.0)/total) * 100)
        prepend = (parents * "\t")
        print  prepend + header + " - " + str(count) #+ " = " + percentage

    urlList = []
    urlListNoProtocol = []
    urlListNoQueryString = []

    for link in linkList:
        urlList.append(str(link['href']))
        noProtocol = link['href'].split('://', 1)[-1]
        urlListNoProtocol.append(str(noProtocol))
        questionSplit = link['href'].rsplit('?', 1)
        if len(questionSplit) > 1:
            noQueryString = questionSplit[0]
            urlListNoQueryString.append(str(noQueryString))
            
    dupes1 = [item for item, c in collections.Counter(urlList).items() if c > 1]
    print "\n\nDUPLICATE LINKS = " + str(len(dupes1)) + "\n----------------"
    for dupe in dupes1:
        print dupe

    dupes2 = [item for item, c in collections.Counter(urlListNoProtocol).items() if c > 1]
    print "\nDUPLICATE LINKS (IGNORING PROTOCOL) = " + str(len(dupes2)) + "\n------------------------------------"
    for dupe in dupes2:
        print dupe

    dupes3 = [item for item, c in collections.Counter(urlListNoQueryString).items() if c > 1]
    print "\nDUPLICATE LINKS (IGNORING QUERYSTRING) = " + str(len(dupes3)) + "\n---------------------------------------"
    for dupe in dupes3:
        print dupe
        
if browser == 'firefox':
    headerList = soup.findAll('h3')
    headerList.pop(0) # Remove "Bookmarks Toolbar"
    
    for node in headerList:
        header = ''.join(node.findAll(text=True))
        s = node
        while getattr(s, 'name', None) != 'dl':
            s = s.findNext('dl')
        parents = len(node.findParents('dl')) - 2
        count = len(s.findAll('a'))
        percentage = "{0:.2f}%".format(((count + 0.0)/total) * 100)
        prepend = (parents * "\t")
        print  prepend + header + " - " + str(count) #+ " = " + percentage