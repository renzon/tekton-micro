# -*- coding: utf-8 -*-
'''
Created on 12/07/2011

@author: Renzo Nuccitelli
'''
from google.appengine.ext import ndb
from zen.dataprocess import validation,transform as trans
from zen.dataprocess.gae import property as prop



REQUIRED_FIELD_ERROR_MSG=u"Campo Obrigatório"
INVALID_OPTION_MSG=u"Opção Inválida"
INVALID_MAIL=u"Email Inválido"
INVALID_FIELD=u"Campo Inválido"
MULTILINE_MSG=u"Campo não aceita que se pule linha"
STRING_TOO_LONG=u"Tamanho máximo de 500 carateres"

def choice_validator_generator(choices):
    def v(value):
        if value is not None and not (value in choices):
            return INVALID_OPTION_MSG
    return v

def _handle_db_propert_attrs(ppt,validator=lambda v: None):
    if ppt._required:
        validator= validation.composition(validation.required_str,\
                validator)
    if ppt._choices:
        validator= validation.composition(choice_validator_generator(ppt._choices),\
                validator)
    return validator

def boolean_validator_generator(ppt):
    return _handle_db_propert_attrs(ppt,validation.boolean_validator)
    
    
def int_validator_generator(ppt):
    return _handle_db_propert_attrs(ppt,validation.int_validator)

def float_validator_generator(ppt):
    return _handle_db_propert_attrs(ppt,validation.float_validator)

def date_validator_generator(ppt):
    return _handle_db_propert_attrs(ppt,validation.brdate)


def string_validator_generator(ppt):
    return _handle_db_propert_attrs(ppt)


DEFAULT_VALIDATORS={ndb.BooleanProperty:boolean_validator_generator,\
    ndb.IntegerProperty:int_validator_generator,\
    ndb.FloatProperty:float_validator_generator,\
    ndb.DateProperty:date_validator_generator,\
    ndb.DateTimeProperty:date_validator_generator,\
    ndb.StringProperty:string_validator_generator
    }

DEFAULT_TRANSFORMATIONS={ndb.BooleanProperty:trans.to_boolean,\
    ndb.FloatProperty:trans.to_float,\
    ndb.IntegerProperty:trans.to_int,\
    ndb.StringProperty:trans.to_none,\
    ndb.DateProperty:trans.brdate,\
    ndb.DateTimeProperty:trans.brdate,\
    prop.PasswordProperty:lambda k: prop.Password(pw=k)}

def _validate_generator(ppt):
    def validate(value):
        vld=getattr(ppt, "validation",lambda k:None)
        validator=_handle_db_propert_attrs(ppt,vld)
        error=validator(value)
        if error: return error
        try:
            if value is not None:
                ppt._validate(value)
            return None
        except Exception,e:
            msg=str(e)
            if msg.find("characters long")>=0:
                return STRING_TOO_LONG
            return INVALID_FIELD
    return validate

def default_validator(ppt):
    return DEFAULT_VALIDATORS.get(ppt.__class__,_validate_generator)(ppt)

def transform(ppt):
    return DEFAULT_TRANSFORMATIONS.get(ppt.__class__,trans.to_none)

formBase='''
          <div class="control-group{{' error' if errors.%(value)s is defined }}">
            <label class="control-label" for="%(value)s">%(value)s</label>
            <div class="controls">
              <input type="text" name="%(value)s"
                class="required{{' error' if errors.%(value)s is defined }}"
                value="{{ %(prefix)s.%(value)s|default('',true) }}" /> <span
                class="help-inline">{{errors.%(value)s|default('',true)}}</span>
            </div>    
            </div>
          ''' 

class Form():
    ''' Base class used to validate,
     transform and generate html based on model _processors
    '''
    def __init__(self,modelClass,exclude=(),requestValidator=None):
        props=modelClass._properties
        keys=[k for k in props.keys() if not k.startswith("_")]
        keys=set(keys)
        exclude=set(exclude)
        foundProps=keys.difference(exclude)
        self.transformations={}
        def f(result,key):
            result[key]=default_validator(props[key])
            self.transformations[key]=transform(props[key])
            return result
        self.validators=reduce(f,foundProps,{})
        self.requestValidator=requestValidator
        
    def validate(self,request):
        def f(errors,key):
            er=self.validators[key](request.get(key))
            if er is not None:
                errors[key]=er
            return errors
        allErrors=reduce(f,self.validators.keys(),{})
        if self.requestValidator:
            allErrors.update(self.requestValidator(request))
        return allErrors
    
    def transform(self,request):
        "Returns a transformed _processors dict"
        return {k:t(request.get(k)) for k,t in self.transformations.iteritems()}
    
    def fill(self,request,model_instace):
        ''' fill a model instance with transformed request _processors
        '''
        def f(m,key):
            val=self.transformations[key](request.get(key))
            setattr(m, key, val) 
            return m
        model=reduce(f,self.transformations.keys(),model_instace)
        return model

    
    def html(self,prefix=""):
        '''Return a horizontal html form based on Twitter Bootstrap CSS
        '''
        form='<form action="" method="post" class="well form-horizontal"><fieldset><legend>Formulário</legend>'
        d={"prefix":prefix}
        for p in self.validators.keys():
            d["value"]=p
            form+=formBase%d

        return form+'</fieldset><div class="form-actions"><input type="submit" value="Salvar" class="btn btn-primary" /></div></form>' 


    
    def request_dict(self, request):
        ''' Return a dict containing the _processors defined on form
        '''
        return {k:request.get(k) for k in self.transformations.keys()}
