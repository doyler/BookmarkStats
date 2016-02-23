import collections

from bs4 import BeautifulSoup
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/

def createSoup(browser):
    with open ("./bookmarks_" + browser + ".html", "r") as myfile:
        html = myfile.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def headerList(browser, theSoup, linkList):
    headerList = theSoup.findAll('h3')
    
    if browser == "chrome" or browser == "firefox":
        headerList.pop(0) # Remove "Bookmarks Toolbar"

    for node in headerList:
        header = ''.join(node.findAll(text=True))
        s = node
        while getattr(s, 'name', None) != 'dl':
            if browser == "chrome" or browser == "ie11":
                s = s.nextSibling
            elif browser == "firefox":
                s = s.findNext('dl')
        if browser == "chrome" or browser == "firefox":
            parents = len(node.findParents('dl')) - 2
        elif browser == "ie11":
            parents = len(node.findParents('dl')) - 1
        count = len(s.findAll('a'))
        percentage = "{0:.2f}%".format(((count + 0.0)/len(linkList)) * 100)
        prepend = (parents * "\t")
        print prepend + header + " - " + str(count) + " = " + percentage

def populateList(linkList, urlType):
    urlList = []
    
    for link in linkList:
        if urlType == "normal":
            urlList.append(str(link['href']))
        elif urlType == "noProtocol":
            noProtocol = link['href'].split('://', 1)[-1]
            urlList.append(str(noProtocol))
        elif urlType == "noQueryString":
            questionSplit = link['href'].rsplit('?', 1)
            if len(questionSplit) > 1:
                noQueryString = questionSplit[0]
                urlList.append(str(noQueryString))
    return urlList

def getDupes(inList):        
    return [item for item, c in collections.Counter(inList).items() if c > 1]
        
def main():
    browser = "ie11"
    
    mySoup = createSoup(browser)
    linkList = mySoup.find_all('a')
    
    # Firefox only fix
    for link in linkList[:]:
        if link['href'].startswith('place'):
            linkList.remove(link)
    
    total = len(linkList)
    print "Total number of bookmarks: " + str(total) + "\n"
    
    headerList(browser, mySoup, linkList)

    urlList = populateList(linkList, "normal")    
    dupes = getDupes(urlList)
    print "\n\nDUPLICATE LINKS = " + str(len(dupes))
    print "----------------"
    for dupe in dupes:
        print dupe
        
    urlList = populateList(linkList, "noProtocol")    
    dupes = getDupes(urlList)    
    print "\nDUPLICATE LINKS (IGNORING PROTOCOL) = " + str(len(dupes))
    print "------------------------------------"
    for dupe in dupes:
        print dupe

    """
    # Maybe remove? This isn't super useful, and hasn't caught any actual dupes    
    urlList = populateList(linkList, "noQueryString")    
    dupes = getDupes(urlList)
    print "\nDUPLICATE LINKS (IGNORING QUERYSTRING) = " + str(len(dupes))
    print "---------------------------------------"
    for dupe in dupes:
        print dupe
    """
        
if __name__=="__main__":
	main()