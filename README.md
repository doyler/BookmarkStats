# BookmarkStats
A python application to get statistics from a browser (Chrome, Firefox, and IE are currently supported) bookmark export

# Features
* Counts all bookmarks in a browser bookmark HTML export
* Counts all bookmarks in folders and sub-folders
* Calculates percentage of bookmarks in each folder/sub-folder
* Visually nests (tabs) sub-folders

![Visual Nesting](http://i.imgur.com/BSdfJr2.png)
* Counts duplicates (and possible duplicates) based on exact matching links or matching links ignoring protocol

![Dupe Checking](http://i.imgur.com/Qo7kTo3.png)
* Cross browser support (tested in the newest versions of Chrome, Firefox, and IE11)
* Generic case (just calculates total links without visualization or folder break down) for unsupported browsers

# TODO
* Organize and straighten methods
* General code cleanup
* Show in which folders the dupes actually reside
* Add sorting options (based on count, etc.)
* Add timeout checking (HEAD request)
* Look into visual representations (pie chart?)
* Add support (recently broken) for duplicate folder names, or at least checking/combining
* Fix IE support
