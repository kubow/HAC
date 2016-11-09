import os, sys
import datetime

# htm template definition
pageTemplateBegin = '''<HTML>
<HEAD>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=windows-1250">
<TITLE>Directory Listing on XXX</TITLE>
<STYLE TYPE="text/css">
<!--
BODY{background:"white";}
a:link {color:#FFFF00;}
a:visited {color:#F3D900;}
a:hover {color:#00FF00;}
a:active {color:#FFFF00;}
.Head{background-color:#404040;color:#ffffff;border:1px solid #000000;text-align:center;font-size:8pt;font-family:"MS Sans Serif";font-style:normal;font-weight:normal;}
.File{background-color:#e8e8ff;color:#080000;border:1px solid #000000;font-size:8pt;font-family:"MS Sans Serif";font-style:normal;font-weight:normal;}
.Fldr{background-color:#404080;color:#ffffff;border:1px solid #000000;font-size:8pt;font-family:"MS Sans Serif";font-style:normal;font-weight:normal;}-->
</STYLE>
</HEAD>
<BODY>
<table><tr class="Head"><td>'''
pageTemplateEnd='''</table>
</BODY>
</HTML>'''
head='List Generated on {0} / Total Folder Size - {1} / {2} Subfolders </td></tr>'
table_row='<tr class="{0}"><td>{1}</td><td>{2}</td></tr>'
# Determine if passed parguments for running over a directory
if len(sys.argv)>1:
    directory = sys.argv[1:]
    # might chceck for trailing \
else:
    directory = os.getcwd()
# Write head of htm file
htm=open(directory+'/ListOfFiles.htm', 'w+')
htm.write(pageTemplateBegin.replace('XXX', directory))
htmContent = ''
total_size = 0
folder_count = 0
# Walk the directory tree
for root, directories, files in os.walk(directory):
    print root
    folder_size = 0
    file_count = 0
    tmpContent = ''
    for filename in files:
        # Join the two strings in order to form the full filepath.
        filesize = str('{0:.2f}'.format(os.path.getsize(root+'/'+filename)/1024))+' kb'
        folder_size = folder_size+(os.path.getsize(root+'/'+filename)/1024)
        tmpContent = tmpContent+table_row.format('File', filename, filesize)+'\n'
        file_count += 1
    ref = '<a href="file:///'+root+'">'+root+'</a> ('+str(file_count)+' files in folder)'
    htmContent = htmContent+'\n'+table_row.format('Fldr', ref, str(folder_size)+' kb')+'\n'+tmpContent
    total_size = total_size+folder_size
    folder_count += 1
htm.write(head.format(datetime.datetime.now(), str(total_size)+' kb', folder_count))
htm.write(htmContent)
htm.write(pageTemplateEnd)
