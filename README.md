# HAC
[![Architecture x64|ARM](https://img.shields.io/badge/Architecture-x64|ARM-yellowgreen.svg)](http://www.arm.com/products/processors/instruction-set-architectures/index.php)
[![Platform Linux|Windows](https://img.shields.io/badge/Platform-Linux|Windows-orange.svg)](https://sqlite.org/features.html)
[![Data SQLite|XML](https://img.shields.io/badge/Data-SQLite|XML-green.svg)](http://www.arm.com/products/processors/instruction-set-architectures/index.php)
[![Bash Script](https://img.shields.io/badge/Bash-Script-blue.svg)](https://www.gnu.org/software/bash/)
[![Visual Basic Script|VBA](https://img.shields.io/badge/Visual%20Basic-Script%20%7C%20VBA-lightgrey.svg)](https://msdn.microsoft.com/en-us/vstudio/ms788229.aspx)
[![Python 2.7|3.0](https://img.shields.io/badge/Python-2.7%20%7C%203.0-yellow.svg)](https://www.python.org/)
[![HTML [5]](https://img.shields.io/badge/HTML-%5B5%5D-brightgreen.svg)](http://www.w3schools.com/html/default.asp)
[![CSS [3]](https://img.shields.io/badge/CSS-%5B3%5D-ff69b4.svg)](http://www.w3schools.com/css/default.asp)


Home Automation Central.
Used for communicating with various datasources (and also some live data) and presenting results in on localhosts.
Main configuration should be platform independent, I guess Android & iOS not for now.
(x86/x64/arm//linux/windows/apache/nginx/sqlite/postgre)

## Connector
Used for communicating with databases. Currently supporting these ones:
- MySQL database (hosted on apache/nginx)
- PostgreSQL database
- sqlite databases (*.db)
This connectow will be used for pushing data to reader and further to presenter

## Presenter
Presenting images in containing directory using java script.

## Reader
Used for reading given websites.
Currently only under windows using MS Access database automated with VBA code.
