# BookmarkStats
A python application to get statistics from a browser bookmark export

# Features
* Counts all bookmarks in a (Chrome and Firefox only) bookmark HTML export
* Counts all bookmarks in folders and sub-folders
* Calculates percentage of bookmarks in each folder/sub-folder
* Visually nests (tabs) sub-folders
* Counts duplicates (and possible duplicates) based on matching links, matching ignoring protocol, and matching ignoring querystring

# TODO
* Add methods and clean up code
* Add support for more browsers
* Add generic case (maybe just total links and don't do visual stuff)
* Add sorting options (based on count, etc.)
* Add timeout checking (HEAD request)
* Look into visual representations (pie chart?)
