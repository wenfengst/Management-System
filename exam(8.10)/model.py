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
    
def update_project_apply(pid,oid):
    db.update('project',where='pid=$pid',vars=locals(),oid=oid,apply='已申请')

def update_project_approve(cid,mid):
    db.update('class',where='cid=$cid',vars=locals(),mid=mid,approve='已审批')
    
def get_projects():
    #return db.select(['project', 'organizer'], where="project.oid = organizer.oid",order='ptime DESC')
    return db.query('select * from project left join organizer on project.oid=organizer.oid')
    
def get_classes(table,pid):
    return db.select(table[0],where='pid=$pid',vars=locals(),order=table[1][-1]+' DESC')
