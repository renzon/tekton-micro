# -*- coding: utf-8 -*-
from zen.dataprocess import transform

INVALID_BR_DATE="invalidBrDate"
REQUIRED_MSG="requiredField"
INVALID_BOOLEAN="invalidBoolean"
INVALID_INT="invalidInt"
INVALID_FLOAT="invalidInt"
INVALID_PHONE="invalidPhone"
INVALID_CEP="invalidCep"
INVALID_LINK="invalidLink"
BR_ERROR_MSGS = {"invalidMail":u"Email inválido", REQUIRED_MSG:u"Campo Obrigatório",
               INVALID_LINK:u"Link Inválido", INVALID_PHONE:u"Telefone Inválido. Exemplo válido: (12) 1212-1212",
               INVALID_CEP:u"CEP Inválido",INVALID_BOOLEAN:u"Opção Inválida","invalidvalueCurrency":u"Moeda Inválida",
               INVALID_INT:u"Valor Inválido",INVALID_FLOAT:u"Valor Inválido","invalidChoice":u"Opção Inválida","invalidChoices":u"Opções Inválidas",\
               INVALID_BR_DATE:u"Data Inválida"}

def composition(*validators):
    def f(currentValidator,nextValidator):
        def k(value):
            result=currentValidator(value)
            if result is not None:
                return result
            return nextValidator(value)
        return k
    return reduce(f,validators,lambda value: None)

def float_validator(value):
    if value is None or value=="":
        return None
    value=value.replace(".","")
    value=value.replace(",",".")
    try:
        float(value)
    except:
        return BR_ERROR_MSGS[INVALID_FLOAT]


def boolean_validator(value):
    if value is None or value=="":
        return None
    value=str(value).upper()
    if value!="TRUE" and value!="FALSE":
        return BR_ERROR_MSGS[INVALID_BOOLEAN]
    return None

def int_validator(value):
    if value is None or value=="":
        return None
    try:
        int(value)
    except:
        return BR_ERROR_MSGS[INVALID_INT]

def required_str(value):
    if value=="" or value is None:
        return BR_ERROR_MSGS[REQUIRED_MSG]
    return None

def br_phone(value):
    if value is None or value=="":
        return None
    value=transform.brphone(value)
    if len(value) == 10:
        try:
            int(value)
            return None
        except Exception:
            pass
    return BR_ERROR_MSGS[INVALID_PHONE]

def cep(value):
    if value is None or value=="":
        return None
    value=transform.cep(value)
    if len(value) == 8:
        try:
            int(value)
            return None
        except Exception:
            pass
    return BR_ERROR_MSGS[INVALID_CEP]


def brcurrency(value):
    if value is None or value=="":
        return None
    value=str(value)
    value=value.replace("R$", "")
    return float_validator(value)




def brdate(value):
    if value is None or value=="":
        return None
    try:
        v=transform.brdate(value)
        f=v
    except: return BR_ERROR_MSGS[INVALID_BR_DATE]


