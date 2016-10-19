# HAC
[![Architecture x64|ARM](https://img.shields.io/badge/Architecture-x64|ARM-yellowgreen.svg)](http://www.arm.com/products/processors/instruction-set-architectures/index.php)
[![Platform Linux|Win](https://img.shields.io/badge/Platform-Linux|Win-orange.svg)](https://sqlite.org/features.html)
[![Bash Script](https://img.shields.io/badge/Bash-Script-blue.svg)](https://www.gnu.org/software/bash/)
[![Visual Basic Script|VBA](https://img.shields.io/badge/Visual%20Basic-Script%20%7C%20VBA-lightgrey.svg)](https://msdn.microsoft.com/en-us/vstudio/ms788229.aspx)
[![Python 2.x|3.x](https://img.shields.io/badge/Python-2.7%20%7C%203.0-yellow.svg)](https://www.python.org/)
[![HTML [5]](https://img.shields.io/badge/HTML-%5B5%5D-brightgreen.svg)](http://www.w3schools.com/html/default.asp)
[![CSS [3]](https://img.shields.io/badge/CSS-%5B3%5D-ff69b4.svg)](http://www.w3schools.com/css/default.asp)

[![Data SQLite|XML](https://img.shields.io/badge/Data-SQLite|XML-green.svg)](https://sqlite.org/features.html)

Home Automation Central.
Used for communicating with various datasources (and also some live data) and presenting results on localhosts.
Main configuration should be platform independent, I guess Android & iOS not for now.
Prequisities:
-python 2.x/3.x installed

## Connector
Used for connecting to various datasources. This connectow will be used for pushing data to reader and further to presenter. Currently supporting these ones:
### Database
#### &nbsp;&nbsp;&nbsp;&nbsp; tk frontend python tables
#### &nbsp;&nbsp;&nbsp;&nbsp; MySQL database (hosted on apache/nginx)
#### &nbsp;&nbsp;&nbsp;&nbsp; PostgreSQL database
#### &nbsp;&nbsp;&nbsp;&nbsp; sqlite databases (*.db)
### Geoinfromation
#### &nbsp;&nbsp;&nbsp;&nbsp; OpenLayers
### Directory Control

## Presenter
Presenting images in containing directory using java script.
#### &nbsp;&nbsp;&nbsp;&nbsp; Word Play

## Reader
Used for reading and processing text to standard fromat.
#### &nbsp;&nbsp;&nbsp;&nbsp; Log Reader
Processing log files with excel sheet
