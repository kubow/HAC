# HAC
[![Architecture x64|ARM](https://img.shields.io/badge/Architecture-x64|ARM-yellowgreen.svg)](http://www.arm.com/products/processors/instruction-set-architectures/index.php)
[![Platform Linux|Win](https://img.shields.io/badge/Platform-Linux|Win-orange.svg)](https://sqlite.org/features.html)
[![Bash Script](https://img.shields.io/badge/Bash-Script-blue.svg)](https://www.gnu.org/software/bash/)
[![Visual Basic Script|VBA](https://img.shields.io/badge/Visual%20Basic-Script%20%7C%20VBA-lightgrey.svg)](https://msdn.microsoft.com/en-us/vstudio/ms788229.aspx)
[![Python 2.7|3.0](https://img.shields.io/badge/Python-2.7%20%7C%203.0-yellow.svg)](https://www.python.org/)
[![HTML [5]](https://img.shields.io/badge/HTML-%5B5%5D-brightgreen.svg)](http://www.w3schools.com/html/default.asp)
[![CSS [3]](https://img.shields.io/badge/CSS-%5B3%5D-ff69b4.svg)](http://www.w3schools.com/css/default.asp)

[![Data SQLite|XML](https://img.shields.io/badge/Data-SQLite|XML-green.svg)](https://sqlite.org/features.html)

Home Automation Central.
Used for communicating with various datasources (and also some live data) and presenting results in on localhosts.
Main configuration should be platform independent, I guess Android & iOS not for now.
(x86/x64/arm//linux/windows/apache/nginx/sqlite/postgre)

## Connector
Used for connecting to various datasources. This connectow will be used for pushing data to reader and further to presenter. Currently supporting these ones:
### Database
#### - tk fromtend python tables
#### - MySQL database (hosted on apache/nginx)
#### - PostgreSQL database
#### - sqlite databases (*.db)
### Geoinfromation
#### - OpenLayers
### Directory Control


## Presenter
Presenting images in containing directory using java script.
#### Word Play

## Reader
Used for reading and processing text to standard fromat.
#### Log Reader
Processing log files with excel sheet
