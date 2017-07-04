# -*- coding: utf-8 -*-
import sys
import datetime

from xml.dom.minidom import parseString
import xml.etree.ElementTree as xml_tree
from bs4 import BeautifulSoup
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
    ref = '<a href="{0}.html">{1}</a>'
    ref_c = '<a class="{0}" href="{1}.html">{2}</a>'
    heading = '<h{0}>{1}</h{0}>'
    paragraph = '<p>{0}</p>'
    paragraph_c = '<p class="{0}">{1}</p>'
    div_tag = '<div id="{0}" class="{1}">{2}</div>'
    pageTemplateBegin = """<!DOCTYPE HTML>
    <htmll>
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
    selectFatherNodes = """SELECT children.father_id, COUNT(node.node_id) FROM node
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
    dashline = '---------------------------------------------------------'


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
