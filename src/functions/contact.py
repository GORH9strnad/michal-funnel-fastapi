import re

def validate_name(name: str):
    if not len(name) > 0:
        raise ValueError('Jméno nesmí být prázdné!')
    if len(name) > 50:
        raise ValueError('Jméno nesmí být delší než 50 znaků!')
    if not re.match(r'^([A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽa-záčďéěíňóřšťúůýž]+(?: [A-ZÁČĎÉĚÍŇÓŘŠŤÚŮÝŽa-záčďéěíňóřšťúůýž]+)*)$', name):
        raise ValueError('Jméno musí obsahovat pouze písmena!')
    if not re.match(r'^\S+\s+\S+.*$', name):
        raise ValueError('Celé jméno musí obsahovat alespoň dvě slova!')
    [first_name, last_name] = name.split(' ')
    if not len(first_name) > 1:
        raise ValueError('Jméno musí obsahovat alespoň 2 znaky!')
    if not len(last_name) > 1:
        raise ValueError('Příjmení musí obsahovat alespoň 2 znaky!')

def validate_email(email: str):
    if not len(email) > 0:
        raise ValueError("E-mail nesmí být prázdný!")
    if len(email) > 100:
        raise ValueError("E-mail nesmí být delší než 100 znaků!")
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        raise ValueError("E-mail není ve správném formátu!")
    
def validate_phone(phone: str):
    if not len(phone) > 0:
        raise ValueError("Telefonní číslo nesmí být prázdné!")
    if len(phone) != 9:
        raise ValueError("Telefonní číslo musí mít 9 číslic!")
    if not re.match(r'^\d{9}$', phone):
        raise ValueError("Telefonní číslo musí obsahovat pouze číslice!")