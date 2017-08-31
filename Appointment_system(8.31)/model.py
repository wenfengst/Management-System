# -*- coding:utf-8 -*- ＃  
import web
import datetime

db = web.database(dbn='mysql', db='appointment', user='root', pw='123456')

def login(username, password, usertype):
    '''登录验证'''
    users = db.select('user', where='username=$username AND password=$password AND usertype=$usertype', vars=locals())
    return users

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
    
def update_class_approve(cid,mid,approve):
    db.update('class',where='cid=$cid',vars=locals(),mid=mid,approve=approve,ctime=datetime.datetime.now())
    
def get_projects(uid):
    return db.query('select project.*,user.username from project,user where project.oid=user.uid and uid=$uid order by ptime DESC',vars=locals())
    
def get_classes(wh):
    return db.query('select cid,cname,begindate,begintime,enddate,endtime,classroom.place,classroom.classroom,\
    project.pname,project.snumber,teacher.tname,approve,u1.username manager,u2.username organizer,ctime \
    from class inner join project on class.pid=project.pid inner join teacher on class.tid=teacher.tid \
    inner join classroom on class.crid=classroom.crid left join user u1 on class.mid=u1.uid inner join user u2 on project.oid=u2.uid '+wh)

