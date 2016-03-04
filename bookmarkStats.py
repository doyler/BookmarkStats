import collections
import requests

from bs4 import BeautifulSoup
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/


# http://www.quesucede.com/page/show/id/python-3-tree-implementation
(_ROOT, _DEPTH, _BREADTH) = range(3)

class Node:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    def add_child(self, identifier):
        self.__children.append(identifier)
        
class Tree:
    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print identifier
        else:
            print "\t" * depth + str(identifier)

        depth += 1
        for child in children:
            self.display(child, depth)  # recursive call

    def traverse(self, identifier, mode=_DEPTH):
        # Python generator. Loosly based on an algorithm from 
        # 'Essential LISP' by John R. Anderson, Albert T. Corbett, 
        # and Brian J. Reiser, page 239-241
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item


def createSoup(browser):
    with open ("./bookmarks_" + browser + ".html", "r") as myfile:
        html = myfile.read()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getChildren(theNode, level):
    children = []
    
    theChildren = theNode.findAll('dl')
    for child in theChildren:
        parents = len(child.findParents('dl'))
        header = child.findPrevious('h3')
        if parents == level + 1:
            children.append(str(''.join(header.findAll(text=True))))
            #children.append(child)
    return children
    
def genHeaderTree(browser, theSoup):
    headerList = theSoup.findAll('h3')
    firstHeader = str(headerList[0].text)

    headerTree = Tree()
    headerTree.add_node(firstHeader)
    
    for item in theSoup.findAll('dl')[1:]:
        parents = len(item.findParents('dl'))
        children = getChildren(item, parents)
        #print children
        if children:
            for child in children:
                #print child + " - " + str(item.findPrevious('h3').text)
                headerTree.add_node(child, str(item.findPrevious('h3').text))
    return headerTree

def printHeaderList(browser, theTree, theSoup, linkList):
    headerList = theSoup.findAll('h3')
    
    if browser == "chrome" or browser == "firefox":
        headerList.pop(0) # Remove "Bookmarks Toolbar"

    for node in headerList:
        header = ''.join(node.findAll(text=True))
        s = node
        while getattr(s, 'name', None) != 'dl':
            if browser == "chrome" or browser == "ie":
                s = s.nextSibling
            elif browser == "firefox":
                s = s.findNext('dl')
        count = len(s.findAll('a'))
        percentage = "{0:.2f}%".format(((count + 0.0)/len(linkList)) * 100)

    theTree.display("Bookmarks bar")
    #print header + " - " + str(count) + " = " + percentage

def populateList(linkList, urlType):
    urlList = []
    
    for link in linkList:
        if urlType == "normal":
            urlList.append(str(link['href']))
        elif urlType == "noProtocol":
            noProtocol = link['href'].split('://', 1)[-1]
            urlList.append(str(noProtocol))
    return urlList

def getDupes(inList):        
    return [item for item, c in collections.Counter(inList).items() if c > 1]
    
def checkStatus(link):
    resp = requests.head(link)
    return resp
        
def main():
    supportedBrowsers = ["chrome", "firefox"]#, "ie"]
    browser = "chrome"
    
    mySoup = createSoup(browser)
    linkList = mySoup.find_all('a')
    
    # Firefox only fix
    for link in linkList[:]:
        if link['href'].startswith('place'):
            linkList.remove(link)
            
    myTree = genHeaderTree(browser, mySoup)
    
    total = len(linkList)
    print "Total number of bookmarks: " + str(total) + "\n"
    
    if any(browser in s for s in supportedBrowsers):
        printHeaderList(browser, myTree, mySoup, linkList)
    
        """
        print("\n --DFS-- \n"")
        for node in myTree.traverse("Bookmarks bar"):
            print(node)
        """

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
    print "\nERROR CONNECTS"
    print "---------------"    
    for link in linkList:
        try:
            response = checkStatus(link['href'])
        except:
            print "ERROR?!"
        if response.status_code != 200:
            print str(response.status_code) + " - " + link['href']
    """

        
if __name__=="__main__":
	main()