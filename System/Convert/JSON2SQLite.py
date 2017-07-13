"""Usage JSON2SQLite.py #.json
parses JSON data to SQLite
kubw kubow 2017"""
import os
import sys
import sqlite3
import json

check_select='SELECT EXISTS(SELECT 1 FROM sqlite_master WHERE type="table" AND name = "{0}");'
insert_query = 'INSERT INTO {0} VALUES ("{1}");'

try:
    if len(sys.argv[1:])>0:
        file_names = sys.argv[1:]
    else:
        file_names = []
        for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
            if file.lower().endswith('.json'):
                print file
                file_names.append(file)
    for json_file in file_names:
        i = 0
        tab_name = json_file.lower().replace('.json', '').replace('.', '_')
        db = sqlite3.connect(tab_name+'.sqlite')
        # db.cursor().execute(check_select.format(tab_name))
        print '***********************'
        if db.cursor().execute(check_select.format(tab_name)).fetchone()[0]:
            db.execute('DROP TABLE '+tab_name+';')
        with open(json_file) as json_stream:
            print 'json opened...'
            source_item = []# for columns
            for line in json_stream:
                source = json.loads(line)
                insert_string = []
                # for j in range(len(source.items())+1):
                if i == 0:
                    for json_item in source:
                        source_item.append(json_item)
                        insert_string.append(str(source[json_item]).encode('utf8'))
                    columns = ', '.join(source_item)
                    print 'columns: '+columns
                    create_query = 'CREATE TABLE '+tab_name+' ('+' text , '.join(source_item)+' text);'
                    db.execute(create_query)
                else:
                    for json_item in source:
                        if str(source[json_item]).isdigit():
                            insert_string.append(str(source[json_item]))
                        else:
                            insert_string.append(str(source[json_item]).encode('utf8'))
                insert_items = '", "'.join(x for x in insert_string)
                db.execute(insert_query.format(tab_name, insert_items.encode('utf8')))
                db.commit()
                #print insert_items
                i += 1
except Exception as ex:
    print 'some exception occured'
    print ex.args
