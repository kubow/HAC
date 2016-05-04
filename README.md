# HAC
Home Automation Central.
Used for communicating with various datasources (and also some live data) and presenting results in most convenient way on localhost site (apache/nginx)

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
