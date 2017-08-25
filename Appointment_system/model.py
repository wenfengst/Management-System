# -*- coding:utf-8 -*- ＃  
import web
import hashlib
import datetime

db = web.database(dbn='mysql', db='appointment', user='root', pw='123456')

def login(username, password, usertype):
    '''登录验证'''
    pwdhash = hashlib.md5(password).hexdigest()
    users = db.select('user', where='username=$username AND password=$password AND usertype=$usertype', vars=locals())
    if users:
        user = users[0]
        return user
    else:
        return 0
    
def current_id():
    '''当前登录用户的id'''
    uid = 0
    try:
        uid = int(web.cookies().get('uid'))
    except Exception, e:
        print e
    else:
        # 刷新cookie
        web.setcookie('uid', str(uid), 3600)
    finally:
        return uid

def get_items(table):
    return db.select(table[0],order=table[1][-1]+' DESC')

def get_item(table,item_id):
    try:
        return db.select(table[0], where=table[1][0]+'=$item_id', vars=locals())[0]
    except IndexError:
        return None

def new_item(table,dic):
    a=dic.keys()
    s='db.insert(table[0]'
    for i in range(len(dic)):
        s=s+','+a[i]+'=dic[a['+str(i)+']]'
    exec(s+')')

def del_item(table,item_id):
    db.delete(table[0], where=table[1][0]+"=$item_id", vars=locals())

def update_item(table,item_id,dic):
    a=dic.keys()
    s='db.update(table[0], where=\''+table[1][0]+'=$item_id\', vars=locals()'
    for i in range(len(dic)):
        s=s+','+a[i]+'=dic[a['+str(i)+']]'
    exec(s+','+table[1][-1]+'=datetime.datetime.now())')
    
def update_class_approve(approve_cid,mid,approve):
    db.update('class',where='cid=$approve_cid',vars=locals(),mid=mid,approve=approve,ctime=datetime.datetime.now())
    
def get_projects():
    return db.query('select project.*,organizer.oname from project left join organizer on project.oid=organizer.oid order by ptime DESC')
    
def get_classes(wh):
    return db.query('select cid,cname,begindate,begintime,enddate,endtime,classroom.place,classroom.classroom,\
    project.pname,project.snumber,teacher.tname,approve,manager.mname,ctime \
    from class inner join project on class.pid=project.pid inner join teacher on class.tid=teacher.tid \
    inner join classroom on class.crid=classroom.crid left join manager on class.mid=manager.mid '+wh)

