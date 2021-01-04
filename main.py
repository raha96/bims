import qrcode
from flask import Flask, url_for, current_app, g, request
import sqlite3

from gencode import *
from serialfuncs import *

app = Flask(__name__)

# Header
def header():
    form  = '<!DOCTYPE html>\n<html lang="en">\n'
    form += '<head>\n'
    form += '<title>Qt QR</title>\n'
    form += '<script src="' + url_for('static', filename='jquery.js') + '"></script>\n'
    form += '<script src="' + url_for('static', filename='jquery.tablesorter.js') + '"></script>\n'
    form += '<script src="' + url_for('static', filename='jquery-ui.js') + '"></script>\n'
    form += '<script src="' + url_for('static', filename='ajax.js') + '"></script>\n'
    form += '<link rel="stylesheet" href="' + url_for('static', filename='theme.blue.css') + '">'
    form += '<link rel="stylesheet" href="' + url_for('static', filename='jquery-ui.css') + '">'
    form += '<link rel="stylesheet" href="' + url_for('static', filename='style.css') + '">'
    form += '</head>\n'
    form += '<body>\n'
    return form

def footer():
    form = '</body>\n</html>\n'
    return form

# Database
def open_db():
    conn = sqlite3.connect('db/qrgendb.sqlite')
    #conn = sqlite3.connect(url_for('static', filename='qrgendb.sqlite'))

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            'db/qrgendb.sqlite',
            #url_for('static', filename='qrgendb.sqlite'),
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    #print(g.db)
    return g.db

def query_db(query):
    cur = g.db.cursor()
    cur.execute(query)
    g.db.commit()
    retval = cur.fetchall()
    return retval

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

paramnum = 5
paramid = ['tissue', 'donner', 'vialnum', 'passage', 'production', 'location', 'number']
paramti = ['Tissue type: ', 'Donner code: ', 'Vial Number: ', 'Passage number: ', 'Production date: ', 'Storage location: ', 'Number of Vials: ']
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

    par = 2             #vialnum
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += f'<td>V<input type=text maxlength=2 size=2 name="{paramid[par]}" id="{paramid[par]}" /></td>\n'

    par = 3             #passage
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += f'<td>P<input type=text maxlength=1 size=1 name="{paramid[par]}" id="{paramid[par]}" /></td>\n'
    form += '</tr>\n'

    par = 4             #production
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += '<td><input type=text maxlength=2 size=2 name="date_yy" id="date_yy" /> / '
    form += '<input type=text maxlength=2 size=2 name="date_mm" id="date_mm" /> / '
    form += '<input type=text maxlength=2 size=2 name="date_dd" id="date_dd" /></td>\n'
    form += '</tr>\n'

    par = 5             #location
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += f'<td><input type=text name="{paramid[par]}" id="{paramid[par]}" /></td>\n'
    form += '</tr>\n'

    par = 6             #number
    form += '<tr>\n'
    form += f'<td>{paramti[par]}</td>\n'
    form += f'<td><input type=text name="{paramid[par]}" id="{paramid[par]}" /></td>\n'
    form += '</tr>\n'

    form += '<tr>\n<td><input type=button onclick="request_visual_code(\'visual_code\')" value="Generate Code" /></td>\n'
    form += '<td><input type=button onclick="fetch_visual_code(\'visual_code\')" value="Find Codes" /></td>\n</tr>\n'

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
        vialnum = int(request.args['vialnum'])
        passage = request.args['passage']
        production = f'{request.args["date_yy"]}/{request.args["date_mm"]}/{request.args["date_dd"]}'
        location = request.args['location']
        number_of_tags = int(request.args['number'])


        #TODO: finalize serial generation algorithm
        #      add serial defragmentation
        query = 'SELECT serial FROM vials ORDER BY serial DESC'
        similar_vials = query_db(query)

        new_serial = ''
        if (len(similar_vials) > 0):
            new_serial = similar_vials[0]['serial']

        form += '<div class="visual_container">\n'
        
        for i in range(number_of_tags):
            new_serial = inc(new_serial)

            outpair = generate_visual_code(serial=new_serial,
                                             date_yy=request.args["date_yy"], date_mm=request.args["date_mm"], date_dd=request.args["date_dd"],
                                             tissue=tissue,
                                             donner=donner,
                                             passage=passage,
                                             res1="0",
                                             res2="X",
                                             vial_num=vialnum)

            generated = outpair[0]
            genquery = outpair[1]
            
            vialnum += 1
      
            query  = f'INSERT INTO vials (serial, tissue, donner, vialnum, passage, date_yy, date_mm, date_dd, location) '
            query += f"VALUES ('{genquery['serial']}', '{genquery['tissue']}', '{genquery['donner']}', '{genquery['vialnum']}', "
            query += f"'{genquery['passage']}', {genquery['date_yy']}, {genquery['date_mm']}, {genquery['date_dd']}, '{location}') "
            query_db(query)
            
            form += '<div class="visual_sub_container">\n'
            form += f'<p class="line0"><b>{generated[0]}</b></p>\n'
            form += f'<p class="line1">{generated[1]}<b>{generated[2]}</b></p>\n'
            form += f'<p class="line2">{generated[3]}</p>\n'
            form += '</div>\n<br />\n'
        
        form += '</div>\n'

    form += footer()
    
    return form

@app.route('/findvial', methods=['GET'])
def findvial():
    get_db()
    form = header()

    query = 'SELECT * FROM vials '
    conditions = []
    

    if (request.method == 'GET'):
        if ('tissue' in request.args) and (len(request.args['tissue']) > 0):
            conditions.append(f"(tissue='{code_tissue(request.args['tissue'])}')")
            
        if ('donner' in request.args) and (len(request.args['donner']) > 0):
            conditions.append(f"(donner='{code_donner(request.args['donner'])}')")
            
        if ('vialnum' in request.args) and (len(request.args['vialnum']) > 0):
            conditions.append(f"(vialnum='{vnum(request.args['vialnum'])}')")
            
        if ('passage' in request.args) and (len(request.args['passage']) > 0):
            conditions.append(f"(passage='{code_passage(request.args['passage'])}')")
            
        if ('date_yy' in request.args) and (len(request.args['date_yy']) > 0):
            conditions.append(f"(date_yy='{request.args['date_yy']}')")
            
        if ('date_mm' in request.args) and (len(request.args['date_mm']) > 0):
            conditions.append(f"(date_mm='{request.args['date_mm']}')")
            
        if ('date_dd' in request.args) and (len(request.args['date_dd']) > 0):
            conditions.append(f"(date_dd='{request.args['date_dd']}')")
            
        if ('location' in request.args) and (len(request.args['location']) > 0):
            conditions.append(f"(location='{request.args['location']}')")
    
    if (len(conditions) > 0):
        query += 'WHERE '
        for cond in conditions:
            query += cond + ' AND '
        query = query[:len(query)-4]
    
    data = query_db(query)

    form += '<div class="visual_container">\n'

    form += '<table class="vial_query">\n'
    form += '   <thead>\n'
    form += '      <tr>\n'
    form += '      <th>Serial Number</th>\n'
    form += '      <th>Tissue Type</th>\n'
    form += '      <th>Donner Code</th>\n'
    form += '      <th>Passage</th>\n'
    form += '      <th>Vial Number</th>\n'
    form += '      <th>Production Date</th>\n'
    form += '      <th>Location</th>\n'
    form += '      <th></th>\n'
    form += '      </tr>\n'
    form += '   </thead>\n'
    form += '   <tbody>\n'
    
    for record in data:
        form += '      <tr>\n'
        form += f'      <td>{record["serial"]}</td>\n'
        form += f'      <td>{record["tissue"]}</td>\n'
        form += f'      <td>{record["donner"]}</td>\n'
        form += f'      <td>{record["passage"]}</td>\n'
        form += f'      <td>{record["vialnum"]}</td>\n'
        form += f'      <td>{record["date_yy"]}/{record["date_mm"]}/{record["date_dd"]}</td>\n'
        form += f'      <td>{record["location"]}</td>\n'
        form += f'      <td><a href="#" onclick="remove_vial_dialog(\'#remove_vial\', \'{record["serial"]}\')">Remove</a></td>\n'
        form += '      </tr>\n'

    #form += f'<p>{len(data)}</p>\n'
    #form += f'<p>{query}</p>\n'
        
    form += '   </tbody>\n'
    form += '</table>\n'

    # Remove vial from the bank
    form += '<div id="remove_vial" title="Remove the vial from the bank?">\n'
    form += '   <div id="message">lorum</div>\n'
    form += '</div>\n'
        
    form += '</div>\n'

    form += footer()
    
    return form


@app.route('/showvial', methods=['GET'])
def showvial():
    get_db()
    #form = header()
    form = ''
    
    if (request.method == 'GET'):
        
        serial = request.args['serial']
        query = f"SELECT * FROM vials WHERE serial='{serial}'"
        vial = query_db(query)

        if (len(vial) > 0):
            rec = vial[0]
            
            form += '<div class="visual_container">\n'            
            outpair = generate_visual_code_raw(serial=serial,
                                             date_yy=rec["date_yy"], date_mm=rec["date_mm"], date_dd=rec["date_dd"],
                                             tissue=rec["tissue"],
                                             donner=rec["donner"],
                                             passage=rec["passage"],
                                             res1="0",
                                             res2="X",
                                             vial_num=rec["vialnum"])

            generated = outpair[0]
            
            form += '<div class="visual_sub_container">\n'
            form += f'<p class="line0"><b>{generated[0]}</b></p>\n'
            form += f'<p class="line1">{generated[1]}<b>{generated[2]}</b></p>\n'
            form += f'<p class="line2">{generated[3]}</p>\n'
            form += '</div>\n<br />\n'
            
            form += '</div>\n'

    #form += footer()
    
    return form
    

@app.route('/qrgen')
def qrgen():
    img = qrcode.make('data')
    img.save('static\currentqr.png')
    imgpath = url_for('static', filename='currentqr.png')
    return '<img src="' + imgpath + '" />'
