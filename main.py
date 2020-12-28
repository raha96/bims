import qrcode
from flask import Flask, url_for, current_app, g, request
import sqlite3

from gencode import *

app = Flask(__name__)

# Header
def header():
    form  = '<!DOCTYPE html>\n<html lang="en">\n'
    form += '<head>\n'
    form += '<title>Qt QR</title>\n'
    form += '<script src="' + url_for('static', filename='jquery.js') + '"></script>\n'
    form += '<script src="' + url_for('static', filename='ajax.js') + '"></script>\n'
    form += '<link rel="stylesheet" href="' + url_for('static', filename='style.css') + '">'
    form += '</head>\n'
    form += '<body>\n'
    return form

def footer():
    form = '</body>\n</html>\n'
    return form

# Database
def open_db():
    conn = sqlite3.connect(url_for('static', filename='qrgendb.sqlite'))

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'static/qrgendb.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    print(g.db)
    return g.db

def query_db(query):
    cur = g.db.cursor()
    cur.execute(query)
    retval = cur.fetchall()
    return retval

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

paramnum = 5
paramid = ['tissue', 'donner', 'passage', 'production', 'location']
paramti = ['Tissue type: ', 'Donner code: ', 'Passage number: ', 'Production date: ', 'Storage location: ']
tissue_types = ['Fat', 'Blood', 'Epiderm', 'Sperm']

@app.route('/')
def homepage():
    get_db()
    
    form = header()
    
    form += '<div id="query">\n'
    form += '<form id="qrform" name="qrform" action="addvial">\n'
    form += '<table>\n'

    par = 0             #tissue
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += f'<td><select name="{paramid[par]}" id="{paramid[par]}">\n'
    for item in tissue_types: 
        form += f'   <option value="{item}">{item}</option>\n'
    form += '</select></td>\n</tr>\n'

    par = 1             #donner
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += f'<td><input type=text maxlength=2 size=2 name="{paramid[par]}" id="{paramid[par]}" /></td>\n'

    par = 2             #passage
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += f'<td>P<input type=text maxlength=1 size=1 name="{paramid[par]}" id="{paramid[par]}" /></td>\n'
    form += '</tr>\n'

    par = 3             #production
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += '<td><input type=text maxlength=2 size=2 name="date_yy" id="date_yy" /> / '
    form += '<input type=text maxlength=2 size=2 name="date_mm" id="date_mm" /> / '
    form += '<input type=text maxlength=2 size=2 name="date_dd" id="date_dd" /></td>\n'
    form += '</tr>\n'

    par = 4             #location
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += f'<td><input type=text name="{paramid[par]}" id="{paramid[par]}" /></td>\n'
    form += '</tr>\n'

    form += '<tr>\n<td><input type=button onclick="request_visual_code(\'visual_code\')" value="Generate Code" /></td>\n</tr>\n'

    form += '</table>\n'
    form += '</form>\n'
    form += '</div>\n'

    #form += f'{len(query_db())}'

    form += '<div id="visual_code"></div>\n'

    form += footer()

    return form

@app.route('/addvial', methods=['GET'])
def addvial():
    get_db()
    form = header()
    
    if (request.method == 'GET'):
        tissue = request.args['tissue']
        donner = request.args['donner']
        passage = request.args['passage']
        production = f'{request.args["date_yy"]}/{request.args["date_mm"]}/{request.args["date_dd"]}'
        location = request.args['location']

        generated = generate_visual_code(serial="ABCDE00",
                                         date_yy=request.args["date_yy"], date_mm=request.args["date_mm"], date_dd=request.args["date_dd"],
                                         tissue=tissue,
                                         donner=donner,
                                         passage=passage,
                                         res1="0",
                                         res2="X")
        form += '<div class="visual_container">\n'
        for i in range(3):
            form += f'<p class="line{i}">{generated[i]}</p>\n'
        form += '</div>\n'
            
        query = ''

    form += footer()
    
    return form
            

@app.route('/qrgen')
def qrgen():
    img = qrcode.make('data')
    img.save('static\currentqr.png')
    imgpath = url_for('static', filename='currentqr.png')
    return '<img src="' + imgpath + '" />'
