
def code_tissue(tissue):
    tissues = {'Fat':'FAT', 'Blood':'BLD', 'Epiderm':'EPM', 'Sperm':'SPM'}
    return tissues[tissue]

def code_donner(donner):
    sanitized = ''
    try:
        donner = int(donner)
        if (donner > 0) and (donner <= 9):
            sanitized = f'0{donner}'
        elif (donner <= 99):
            sanitized = donner
        else:
            sanitized = '99'
    except:
        sanitized = '99'
    finally:
        return sanitized

def code_passage(passage):
    passage = int(passage)
    sanitized = ''
    if (passage >= 0) and (passage <= 9):
        sanitized = f'P{passage}'
    else:
        sanitized = 'PX'
    return sanitized

def code_res1(res):
    sanitized = res[0]
    return sanitized

def code_res2(res):
    sanitized = res[0]
    return sanitized

def vnum(vial_num):
    sanitized = f'V{vial_num}'
    return sanitized

def generate_visual_code_raw(serial, date_yy, date_mm, date_dd, tissue, donner, passage, res1, res2, vial_num):
    code = []

    code.append(f'{tissue}-{donner}-{passage}')
    code.append(f'{serial}-')
    code.append(vial_num)
    #code.append(f'{}---{code_res1(res1)}-{code_res2(res2)}')
    code.append(f'{date_yy}/{date_mm}/{date_dd}')

    qdic = {}
    qdic['serial'] = serial
    qdic['tissue'] = tissue
    qdic['donner'] = donner
    qdic['vialnum'] = vial_num
    qdic['passage'] = passage
    qdic['date_yy'] = date_yy
    qdic['date_mm'] = date_mm
    qdic['date_dd'] = date_dd
    
    return (code, qdic)

def generate_visual_code(serial, date_yy, date_mm, date_dd, tissue, donner, passage, res1, res2, vial_num):
    return generate_visual_code_raw(serial, date_yy, date_mm, date_dd, code_tissue(tissue),
                                    code_donner(donner), code_passage(passage), res1, res2, vnum(vial_num))
