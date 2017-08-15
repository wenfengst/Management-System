# -*- coding:utf-8 -*- ＃  
import web
import datetime

db = web.database(dbn='mysql', db='exam', user='root', pw='123456')

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
    
def update_class_approve(approve_cid,unapprove_cid,mid):
    db.update('class',where='cid=$approve_cid',vars=locals(),mid=mid,approve='通过',ctime=datetime.datetime.now())
    db.update('class',where='cid=$unapprove_cid',vars=locals(),mid=mid,approve='不通过',ctime=datetime.datetime.now())
    
def get_projects():
    return db.query('select * from project left join organizer on project.oid=organizer.oid order by ptime DESC')
    
def get_classes(wh):
    return db.query('select cid,cname,begindate,begintime,enddate,endtime,classroom.place,classroom.classroom,\
    project.pname,teacher.tname,approve,manager.mname,ctime \
    from class inner join project on class.pid=project.pid inner join teacher on class.tid=teacher.tid \
    inner join classroom on class.crid=classroom.crid left join manager on class.mid=manager.mid '+wh+' order by ctime DESC')

