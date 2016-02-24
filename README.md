# BookmarkStats
A python application to get statistics from a browser bookmark export

# Features
* Counts all bookmarks in a browser bookmark HTML export
* Counts all bookmarks in folders and sub-folders
* Calculates percentage of bookmarks in each folder/sub-folder
* Visually nests (tabs) sub-folders
* Counts duplicates (and possible duplicates) based on matching links, matching ignoring protocol, and matching ignoring querystring
* Cross browser support (tested in the newest versions of Chrome, Firefox, and IE11)
* Generic case (just calculates total links without visualization or folder break down) for unsupported browsers

# TODO
* Organize and straighten methods
* General code cleanup
* Show in which folders the dupes actually reside
* Add sorting options (based on count, etc.)
* Add timeout checking (HEAD request)
* Look into visual representations (pie chart?)
