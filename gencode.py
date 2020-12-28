
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

def generate_visual_code(serial, date_yy, date_mm, date_dd, tissue, donner, passage, res1, res2):
    code = []

    code.append(f'{serial}')
    code.append(f'{date_yy}/{date_mm}/{date_dd}')
    code.append(f'{code_tissue(tissue)}-{code_donner(donner)}-{code_passage(passage)}-{code_res1(res1)}-{code_res2(res2)}')
    
    return code
