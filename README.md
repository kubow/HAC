# HAC (Home Automation Central)
[![Architecture x64|ARM](https://img.shields.io/badge/Architecture-x64|ARM-yellowgreen.svg)](http://www.arm.com/products/processors/instruction-set-architectures/index.php) [![Platform Linux|Win](https://img.shields.io/badge/Platform-Linux|Win-orange.svg)](https://sqlite.org/features.html) [![Data SQLite|XML](https://img.shields.io/badge/Data-SQLite|XML|JSON|CSV-green.svg)](https://sqlite.org/features.html) [![Bash Script](https://img.shields.io/badge/Heartbeat-shellscripts*sh|cmd-blue.svg)](https://www.gnu.org/software/bash/) [![Python 2.x|3.x](https://img.shields.io/badge/Python-2.x%20%7C%203.x-yellow.svg)](https://www.python.org/) [![HTML [5]](https://img.shields.io/badge/HTML-%5B5%5D-brightgreen.svg)](http://www.w3schools.com/html/default.asp) [![CSS [3]](https://img.shields.io/badge/CSS-%5B3%5D-ff69b4.svg)](http://www.w3schools.com/css/default.asp)

<i class="icon-file"></i><i class="icon-pencil"></i><i class="icon-refresh"></i><i class="icon-cog"></i>

Used for communicating with various data sources and presenting results on hosts.
Main configuration is platform independent, sqlite based, data generated are mostly JSON and CSV.

[TOC]
## Database (DB74.py)
used for browse/compare sqlite databases.

 - parameters:
   	- -m (mode:compare/browse)
   	- -l (first file)
   	- -r (second file)
###DBView.py 
used to GUI browse database (Tk)
## Device (DV72.py)
reading inputs and outputs from defined connections (settings in Settings.sqlite)

 - parameters:
	 - -d (device) - name of device currently running the script (win/rpi)
	 - -s (sensor)  - luxo/all
	 - -l (location) - Praha, CZ
## H808E (H808E.py)
main application to browse file structure (settings in Settings.sqlite)

 - parameters:
	 - -c (encyklopedia sqlite database) (Cherry Tree application)
	 - -d (directory with encyklopedia) (local file storage)
## Operating System (OS74.py)
Directory browser/lister

 - parameters:
	 - -b (browse directory)
	 - -l (list directory)
	 -  -f (output file - usually index.html)
## Software (SO74.py)
Several paths to retrieve multimedia information

 - modes:
	 - weather
	 - internet browser (html, rss, restaurants...)
 - parameters:
	 - -g (mode: weather/rss/rest...)
	 - -w (destination)
	 - -p (place/location where user wants to read weather or a link to a web page, which will be read)
	 -  -l (log file - usually logfile.log)
## Text proccessing (TX74.py)
Used for reading and processing text to standard formats.

 - parameters:
	 - -i (input directory)
	 - -o (output directory)
	 -  -l (logic)
## Extra Modules
### Log Reader
Processing log files with excel sheet
### Tester
Testing main functions of the whole system

| File      | Test class                   | Description                   |
|-----------| ---------------------------- | ------------------------------|
| DV72      | `Device()`                   | Determine device prepare run  |
| OS74      | `TestPlatform()`             | Determine platform            |
| 1         | `TestWeather()`              | Retrieve weather              |
| 1         | `TestWebContent()`           | Retrieve content of a website |

And flow charts like this:

```flow
st=>start: Start
e=>end
op=>operation: My Operation
cond=>condition: Yes or No?

st->op->cond
cond(yes)->e
cond(no)->op
```


