"""Usage JSON2SQLite.py #.json
parses JSON data to SQLite"""
import sys
import sqlite3
import json

check_select='SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type="table" AND name = "{0}");'

try:
    if len(sys.argv[1:])>0: 
        file_names = sys.argv[1:]
    else:
        
    for json_file in file_names:
        i = 0
        tab_name = json_file.lower().replace('.json', '').replace('.', '_')
        db = sqlite3.connect(tab_name+'.sqlite')
        db.cursor().execute(check_select.format(tab_name))
        print '***********************'
        print db.cursor().fetchone()
        if db.cursor().fetchone():
            db.execute('DROP TABLE '+tab_name+';')
        query = 'INSERT INTO '+tab_name+' VALUES ("{0}");'
        with open(json_file) as json_stream:
            print 'json opened...'
            source_item = [] # for columns
            for line in json_stream:
                source = json.loads(line)
                insert_string = []
                #for j in range(len(source.items())+1):
                if i == 0:
                    for json_item in source:
                        source_item.append(json_item)
                        insert_string.append(source[json_item])
                    columns = ', '.join(source_item)
                    print 'columns: '+columns
                    create_query = 'CREATE TABLE '+tab_name+' ('+' text , '.join(source_item)+' text);'
                    db.execute(create_query)
                else:
                    for json_item in source:
                        insert_string.append(source[json_item])
                insert_query = '", "'.join(str(x) for x in insert_string)
                db.execute(query.format(insert_query))
                db.commit()
                print insert_query
                i += 1
except Exception as ex:
       print ex.args[0]