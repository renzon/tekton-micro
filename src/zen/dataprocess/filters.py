'''
Created on 02/07/2011

@author: Renzo Nuccitelli
'''
import datetime

def brfloat(value):
    if value is None:
        return ""
    return str(value).replace(".",",")

def brcurrency(value, removesignal=False):
    """ put a variable in pt_Br currency format """
    if value is None or value == "":
        return not removesignal and "R$ --" or "0,00"
    value = str(value)
    if len(value)==1:
        num="0,0"+value
    elif len(value)==2:
        num="0,"+value
    else:
        num = ","+value[-2:]
        value=value[:-2]
        while len(value)>3:
            num="."+value[-3:]+num
            value=value[:-3]
            num=value+num
    return (not removesignal and "R$ " or "") + num
    
def brphone(phone):
    if not phone:
        return u""
    return u"(" + phone[0:2] + u") " + phone[2:6] + u"-" + phone[6:10]

def none_to(value, replace=""):
    return value or replace

class _BR_tzinfo(datetime.tzinfo):
    """Implementation of the BR timezone."""
    def utcoffset(self, dt):
        return datetime.timedelta(hours= -3) + self.dst(dt)

    def _ThirdSunday(self, dt):
        """Third Sunday on or after dt."""
        return dt + datetime.timedelta(days=(6 - dt.weekday()))

    def dst(self, dt):
        # 2 am on the Third Sunday in October
        dst_start = self._ThirdSunday(datetime.datetime(dt.year, 10, 15, 2))
        # 1 am on the first Sunday in November
        dst_end = self._ThirdSunday(datetime.datetime(dt.year, 2, 14, 1))
        # 2 am on the T Sunday in March
        if (dst_start >= dt.replace(tzinfo=None) > dst_end):
            return datetime.timedelta(hours=0)
        else:
            return datetime.timedelta(hours=1)
        
    def tzname(self, dt):
        if self.dst(dt) == datetime.timedelta(hours=0):
            return "BST"
        else: return "BDT"
        
class _UTC(datetime.tzinfo):
    def utcoffset(self, dt):
        return self.dst(dt)

    def dst(self, dt):
        return datetime.timedelta(hours=0)
        
        
    def tzname(self, dt):
        return "UTC"


brtzinfo = _BR_tzinfo()
utc = _UTC()


def brdate(dt,strf="%d/%m/%y - %H:%M:%S"):
    if dt:
        if not isinstance(dt, datetime.datetime):
            dt=datetime.datetime(dt.year,dt.month,dt.day)
        ut = dt.replace(tzinfo=utc)
        dt = ut.astimezone(brtzinfo)
        return dt.strftime(strf)
        return ""
  
def cep(c):
    if (c is not None) and len(c) > 5:
        c = c[0:5] + u"-" + c[5:]
        return c 
    return c

def cpf(c):
    c=None if c is None else str(c) 
    if (c is not None) and len(str(c)) == 11:
        c = c[0:3] + u"." +c[3:6]+u"."+c[6:9] +u"-"+ c[9:]
        return c 
    return c

