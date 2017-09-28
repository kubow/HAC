# -*- coding: utf-8 -*-
import sys
import xml.etree.ElementTree as xml_tree
# sys.setdefaultencoding('utf-8')


class HTML(object):
    """Some important structure templates, currently:
    + ref - for htmll refs (_c for classed ref)
    + heading - header universal
    + paragraph - paragraph styled (_c for classed)
    + div_tag
    + pageTemplateBegin - as document header (up to menu)
    + pageTemplateMiddle - as middle part of document
    + pageTemplateEnd - as ending part of document"""
    skelet = """<!DOCTYPE html> 
    <html lang="en">
    <head>{0}
    </head>
    <body>{1}
    </body>
    </html>"""
    skelet_meta = skelet.format('\n<meta {0}>{1}', '{2}')
    skelet_meta_charset = skelet_meta.format('charset="UTF-8"', '{0}', '{1}')
    skelet_titled = skelet_meta_charset.format('\n<title>{0}</title>', '{1}')
    ref = '<a href="{0}.html">{1}</a>'
    ref_c = '<a class="{0}" href="{1}.html">{2}</a>'
    heading = '<h{0}>{1}</h{0}>'
    paragraph = '<p>{0}</p>'
    paragraph_c = '<p class="{0}">{1}</p>'
    div_tag_simple = '<div {0}>{1}</div>'
    div_tag_id = div_tag_simple.format('id="{0}"', '{1}')
    div_tag_class = div_tag_simple.format('class="{0}"', '{1}')
    div_tag = '<div id="{0}" class="{1}">{2}</div>'
    pageTemplateBegin = """<!DOCTYPE HTML>
    <html lang="cs">
    <head>
    <meta charset="utf-8">
    <title>{0}</title>
    <link rel="stylesheet" type="text/css" href="../Web/Design/css/ENC.css">
    </head>
    <body>
    <div id="Cube">
      <div id="l1d1" class="Kula">
        <div class="cat_main"><a href="400.html" target="_self">Priroda</a></div>
        <div class="cat_sub"><a href="410.html" target="_self">Život, Biologie</a></div>
        <div class="cat_sub"><a href="420.html" target="_self">Voda, Hydrologie</a></div>
        <div class="cat_sub"><a href="430.html" target="_self">Vzduch, Ekologie</a></div>
        <div class="cat_sub"><a href="440.html" target="_self">Země, Geologie</a></div>
      </div>
      <div id="l2d1" class="Kula">
        <div class="l1"><a href="123.html" target="_self">Hvězdná encyklopedie</a></div>
        <div class="l2">(toolkit){1}</div>
      </div>
      <div id="l2d1x" class="Kula">"""
    pageTemplateMiddle = """</div>
      <div id="l3d1" class="Kula">
        <div class="cat_main"><a href="500.html" target="_self">Clovek</a></div>
        <div class="cat_sub"><a href="510.html" target="_self">Jídlo a zdravení</a></div>
        <div class="cat_sub"><a href="520.html" target="_self">Pohyb a kondice</a></div>
        <div class="cat_sub"><a href="530.html" target="_self">Kultura</a></div>
        <div class="cat_sub"><a href="540.html" target="_self">Administrativa</a></div>
        <div class="cat_sub"><a href="505.html" target="_self">Magie</a></div>
      </div>
      <div id="l1d2" class="Kula">
        <div class="cat_main"><a href="600.html" target="_self">Vedy</a></div>
        <div class="cat_sub"><a href="610.html" target="_self">Matematika</a></div>
        <div class="cat_sub"><a href="620.html" target="_self">Fyzika</a></div>
        <div class="cat_sub"><a href="630.html" target="_self">Chemie</a></div>
        <div class="cat_sub"><a href="640.html" target="_self">Astronomie</a></div>
        <div class="cat_sub"><a href="650.html" target="_self">Filosofie</a></div>
        <div class="cat_sub"><a href="660.html" target="_self">Kvantova</a></div>
      </div>
      <div id="l2d2" class="Kula">"""
    pageTemplateEnd = """
      </div>
      <div id="l3d2" class="Kula">
        <div class="cat_main"><a href="700.html" target="_self">Technika</a></div>
        <div class="cat_sub"><a href="710.html" target="_self">Materiály</a></div>
        <div class="cat_sub"><a href="720.html" target="_self">Nástroje</a></div>
        <div class="cat_sub"><a href="730.html" target="_self">Energetika</a></div>
        <div class="cat_sub"><a href="740.html" target="_self">Software</a></div>
        <div class="cat_sub"><a href="750.html" target="_self">Stavby</a></div>
      </div>
      <div id="l1d3" class="Kula">
        <div class="cat_main"><a href="800.html" target="_self">Mista</a></div>
      </div>
      <div id="l2d3" class="Kula"><a href="520.html" target="_self">{0}</a></div>
      <div id="l3d3" class="Kula">
        <div class="cat_main"><a href="520.html" target="_self">Znami</a></div>
      </div>
    </div>
    </body>
    </htmll>
    """


class SQL(object):
    """ First H808 queries / device controller"""
    
    table_ddl = 'CREATE TABLE {0} ({1});'
    table_ddl_dir = """ ID int,
        reg_name text,
        file_dir int, --boolean
        last_change text, --date
        size int
        """
    table_ddl_log = ("`ID`	INTEGER PRIMARY KEY AUTOINCREMENT,\n"
                     "	`Connection`	VARCHAR(255) DEFAULT NULL,\n"
                     "	`LogDate`	DATETIME DEFAULT NULL,\n"
                     "	`User`	VARCHAR(255) DEFAULT NULL,\n"
                     "	`Succesful`	BOOLEAN DEFAULT 0,\n"
                     "	`Tag`	VARCHAR(255) DEFAULT NULL,\n"
                     "	`CPName`	VARCHAR(255) DEFAULT NULL,\n"
                     "	`Report`	TEXT,\n"
                     "	`Domain`	VARCHAR(255) DEFAULT NULL,\n"
                     "	`Ping`	BOOLEAN DEFAULT 0")
    table_create = table_ddl.format('dirlist', table_ddl_dir)

    select = 'SELECT {0} FROM {1};'
    select_where = 'SELECT {0} FROM {1} WHERE {2};'

    select_node_text = select_where.format('txt', '"enc_nodes"', 'code = {0}')
    select_tables_in_db = select_where.format('tbl_name, type', '"sqlite_master"', 'type = "table"')

    exist = """SELECT EXISTS(
                SELECT 1 FROM {0}
                WHERE {1}
            );"""
    table_exist = exist.format('sqlite_master', 'type="table" AND name = "{0}"')
    table_structure = select_where.format('sql', 'sqlite_master', 'tbl_name = "{0}" and name = "{1}"')

    select_father_nodes = """SELECT children.father_id, COUNT(node.node_id) FROM node
    INNER JOIN children ON node.node_id = children.node_id
    GROUP BY father_id"""
    selectRootNodes = """SELECT children.father_id, node.level, node.name,
    node.txt, node.node_id, children.sequence, enc.code FROM children
    INNER JOIN node ON children.node_id = node.node_id
    INNER JOIN enc ON enc.node_id = node.node_id
    WHERE (children.father_id = 0 )
    ORDER BY children.sequence"""
    selectSubRootNodes = """SELECT node.node_id, node.name, node.txt,
    children.sequence, enc.code
    FROM children
    INNER JOIN node ON children.node_id = node.node_id
    INNER JOIN enc ON children.node_id = enc.node_id
    WHERE children.father_id =:father
    ORDER BY children.sequence"""

    insert = 'INSERT INTO {0} VALUES ({1});'
    
    ins_val = '"{0}", "{1}", "{2}", "{3}", {4}'
    dashline = '---------------------------------------------------------'

    get_settings = """SELECT drivertype, driverloc 
    FROM driver 
    WHERE device = (
        SELECT ID from device where devicename = '{0}'
    );"""

    column_select = 'SELECT {0} FROM {1};'
    column_select_where = column_select.format('{0}', '{1} WHERE {2}')
    column_group_select = column_select.format('{0}', '{1} GROUP BY {2}')
    column_group_select = column_select.format('{0}', '{1} GROUP BY {2}')

    get_structure = column_select.format('*', 'structure')
    get_table_name = column_select.format('table_name', 'setting')

    get_device_name_list = column_select.format('MachineName', 'Stations')
    get_device_os_list = column_select.format('OpSystem', 'Stations')

    get_driver_loc = column_select_where.format('ComAddress, ComAddLast', 'Stations', 'Machinename = "{0}"')
    get_driver_br = column_select_where.format('BaudeRate', 'Stations', 'Machinename = "{0}"')
    get_driver_dummy_loc = column_select_where.format('ComAddress, ComAddLast', 'Stations',
                                                      'Machinename LIKE "%cp%" AND OpSysType LIKE "%{0}%"')
    get_driver_dummy_br = column_select_where.format('BaudeRate', 'Stations',
                                                      'Machinename LIKE "%cp%" AND OpSysType LIKE "%{0}%"')

    measured_column_count = column_group_select.format('length({0}) AS {1}', 'measured', '{2}')
    
    value_select = column_select_where.format('{0}', '{1}', 'timestamp = "{2}"')
    value_exist = column_select_where.format('timestamp', '{0}', 'timestamp = "{1}"')

    value_insert = 'INSERT INTO {0} VALUES ({1});'
    value_update = 'UPDATE {0} SET {1} WHERE timestamp = "{2}";'


def construct(node, fathers, conn, level, mf, href, mainhref):
    """ function to write child nodes of root nodes, arguments:
    node - the main node id, which has node children
    fathers - pass array of nodes which have children
    conn - pass the original connection to sqlite database
    level - hierarchy tree position (starting with 1)
    mf - htmll file which is being written (main file)
    href - refernece to rootnode in htmll markup
    mainhref - main rootnode reference to keep bond"""
    rows = conn.execute(c.selectSubRootNodes, {"father": str(node)})  # .fetchall()
    level += 1
    # for all fetched children rows (compare with sql c.selectSubRootNodes)
    for node_id, node_namen, node_textn, node_sqn, code_he in rows:
        node_name = node_namen.encode('utf8')
        node_text = node_textn.encode('utf8')
        code_last = int(str(code_he).split(".")[0][-1])
        # print(
        # '--' * level + node_name + ' node / id ' + str(node_id) + ' / sqn ' + str(node_sqn) + ' level ' + str(level))
        mf.write(c.ref_c.format('l' + str(level), code_he, node_name))
        # level = 2 and 3 equivalent - appending all of them
        ref_prep = c.paragraph_c.format('l' + str(level), c.ref.format(str(code_he), node_name))
        if level < 4:
            href += ref_prep
            mainhref += ref_prep
            prev_code = code_last
        # level = 3 equivalent - appending different to each href
        else:
            href += ref_prep
        fo = open(directory + '/' + str(code_he) + '.html', 'w+')
        fo.write(c.pageTemplateBegin.format(node_name, node_name) + mainhref)
        # append next level refs and proceed new ones
        if node_id in fathers:
            sf = fo
            construct(node_id, fathers, conn, level, sf, href, mainhref)
        fo.write(c.pageTemplateMiddle)
        # begin to parse text
        e = xml_tree.fromstring(node_text)
        for element in e._children:
            if None <> element.text:
                for par_text in element.text.encode('utf8').split('\n'):
                    fo.write(c.paragraph.format(par_text))
            else:
                fo.write(c.paragraph.format('... no content yet ...'))
        fo.write(c.pageTemplateEnd.format(time_stamp))
        fo.close()
