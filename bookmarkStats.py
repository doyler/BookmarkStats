from bs4 import BeautifulSoup

with open ("./bookmarks.html", "r") as myfile:
    html = myfile.read()

parsed_html = BeautifulSoup(html)

soup = BeautifulSoup(html, 'html.parser')

total = len(soup.find_all('a'))
print "Total number of bookmarks: " + str(total) + "\n"

headerList = soup.findAll('h3')
headerList.pop(0) # Remove "Bookmarks Toolbar"

for node in headerList:
    header = ''.join(node.findAll(text=True))
    s = node
    while getattr(s, 'name', None) != 'dl':
        s = s.nextSibling
    count = len(s.findAll('a'))
    print header + " - " + str(count) + " = " + "{0:.2f}%".format(((count + 0.0)/total) * 100)