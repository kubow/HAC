# HAC
[![Python 2.6|2.7](https://img.shields.io/badge/python-2.6|2.7-yellow.svg)](https://www.python.org/)

Home Automation Central.
Used for communicating with various datasources (and also some live data) and presenting results in on localhosts.
Main configuration should be platform independent, I guess not Android & iOS for now.
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
