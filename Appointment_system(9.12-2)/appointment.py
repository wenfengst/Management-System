# -*- coding:utf-8 -*- ＃  
import web
import model
import datetime
import calendar
web.config.debug = False 


urls = (
    '/', 'Login',
    '/logout', 'Logout',
    '/index', 'Index',
    '/index_item/(.+)', 'Index_item',
    '/new_item/(.+)', 'New_item',
    '/delete_item/(.+)/(\d+)', 'Delete_item',
    '/edit_item/(.+)/(\d+)', 'Edit_item',
    '/index_project', 'Index_project',
    '/new_project', 'New_project',
    '/delete_project/(\d+)', 'Delete_project',
    '/edit_project/(\d+)', 'Edit_project',
    '/index_class/(.*)', 'Index_class',
    '/index_class_project/(\d+)', 'Index_class_project',
    '/new_class/(\d+)', 'New_class',
    '/delete_class/(\d+)/(\d*)', 'Delete_class',
    '/edit_class/(\d+)/(\d*)', 'Edit_class',
    '/copy_class/(\d+)/(\d*)', 'Copy_class',
    '/view_class/(\d+)','View_class',
    '/approve_class/(.+)', 'Approve_class',
    '/approve/(\d+)','Approve',
    '/conflict_class/(\d+)', 'Conflict_class',
    '/monthly_summary/(.+)','Monthly_summary',
)


app = web.application(urls, globals())
#设置session的存储方式为磁盘.initializer 指定session的初始化值
session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'login':0,'privilege':0,'uid':0,})

alltable = {'user':['user',['uid','username','password','usertype','utime']],
    'teacher':['teacher',['tid','tname','bank_number','ttime']],
     'student':['student',['sid','sname','studenttime']],
     'classroom':['classroom',['crid','place','classroom','crtime']],
     'project':['project',['pid','oid','pname','budget','snumber','ptime']],
     'class':['class',['cid','pid','tid','mid','crid','cname','begindate','begintime','enddate','endtime','approve','ctime']],
     }


def logged():
    if session.login == 1:
        return True
    else:
        return False

 
def create_render(privilege): 
    if privilege==0:
        render = web.template.render('templates', base='base')
    elif privilege==1:  
        render = web.template.render('templates/admin', base='../base')
    elif privilege==2:  
        render = web.template.render('templates/manager', base='../base')
    elif privilege==3:  
        render = web.template.render('templates/organizer', base='../base')
    return render


class Login:

    def GET(self):
        if logged():
            raise web.seeother('/logout')
        else:  
            render = create_render(session.privilege)
            return render.login()
    
    def POST(self):
        form = web.input()
        users = list(model.login(form['username'], form['password'], form['usertype']))
        if len(users)==1:
            session.login = 1
            session.uid = users[0]['uid']
            usertype = users[0]['usertype']
            if usertype=='administrator':
                session.privilege = 1
            elif usertype=='manager':
                session.privilege = 2
            elif usertype=='organizer':
                session.privilege = 3
            raise web.seeother('/index')
        else:
            render = create_render(0)
            return render.error('登录验证失败，请检查帐号和密码是否正确')
    
    
class Logout:
    def GET(self):
        session.login = 0
        session.uid = 0
        session.privilege = 0
        session.kill()  
        raise web.seeother('/')
        

class Index:
    def GET(self):
        uid = session.uid
        user = model.get_item(alltable['user'],uid)
        render = create_render(session.privilege)
        return render.index(user,datetime.datetime.now().strftime('%Y-%m'))


class Index_item:
    
    def GET(self,tablename):
        table=alltable[tablename]
        items = model.get_items(table)
        render = create_render(session.privilege)
        return render.index_item(table,items)


class New_item:

    def GET(self,tablename):
        table = alltable[tablename]
        render = create_render(session.privilege)
        return render.new_item(table)

    def POST(self,tablename):
        table = alltable[tablename]
        form = web.input()
        model.new_item(table,form)
        raise web.seeother('/index_item/'+table[0])


class Delete_item:

    def POST(self,tablename,itemid):
        table = alltable[tablename]
        model.del_item(table,int(itemid))
        raise web.seeother('/index_item/'+table[0])


class Edit_item:

    def GET(self,tablename,itemid):
        table = alltable[tablename]
        item = model.get_item(table,int(itemid))
        render = create_render(session.privilege)
        return render.edit_item(table,item)

    def POST(self,tablename,tid):
        table = alltable[tablename]
        form = web.input()
        model.update_item(table,int(tid),form)
        raise web.seeother('/index_item/'+table[0])


class Index_project:
    
    def GET(self):
        if session.privilege==2:
            wh = ''
        elif session.privilege==3:
            wh = ' and uid='+str(session.uid)
        projects = model.get_projects(wh)
        render = create_render(session.privilege)
        return render.index_project(projects)


class New_project:

    def GET(self):
        render = create_render(session.privilege)
        return render.new_project()

    def POST(self):
        table = alltable['project']
        form = web.input()
        form['oid'] = session.uid
        model.new_item(table,form)
        raise web.seeother('/index_project')


class Delete_project:

    def POST(self,pid):
        table = alltable['project']
        model.del_item(table,int(pid))
        raise web.seeother('/index_project')


class Edit_project:

    def GET(self,pid):
        table = alltable['project']
        project = model.get_item(table,int(pid))
        render = create_render(session.privilege)
        return render.edit_project(project)

    def POST(self,pid):
        table = alltable['project']
        form = web.input()
        model.update_item(table,int(pid),form)
        raise web.seeother('/index_project')


class Index_class:
    
    def GET(self,term):
        if session.privilege==3:
            user = 'where u2.uid='+str(session.uid)
            if term=='':
                classes = model.get_classes(user+' order by ctime DESC')
            elif term=='unapprove':
                classes = model.get_classes(user+' and approve=\'未审批\' order by ctime DESC')
            elif term=='pass':
                classes = model.get_classes(user+' and approve=\'通过\' order by ctime DESC')
            elif term=='notpass':
                classes = model.get_classes(user+' and approve=\'不通过\' order by ctime DESC')
        elif session.privilege==2:
            if term=='':
                classes = model.get_classes('order by ctime DESC')
            elif term=='unapprove':
                classes = model.get_classes('where approve=\'未审批\' order by ctime DESC')
            elif term=='pass':
                classes = model.get_classes('where approve=\'通过\' order by ctime DESC')
            elif term=='notpass':
                classes = model.get_classes('where approve=\'不通过\' order by ctime DESC')
        render = create_render(session.privilege)
        return render.index_class(classes,datetime.datetime.now().strftime('%Y-%m'))


class Index_class_project:
    
    def GET(self,pid):
        classes = list(model.get_classes('where class.pid='+str(pid)+' order by ctime DESC'))
        for c in classes:
            conflict_class = model.get_conflict_class(c)
            if len(conflict_class)==1:
                c['conflict'] = 0
            else:
                c['conflict'] = 1
        render = create_render(session.privilege)
        return render.index_class_project(classes,pid,datetime.datetime.now().strftime('%Y-%m'))


class New_class:

    def GET(self,pid):
        teachers = model.get_items(alltable['teacher'])
        classrooms = model.get_items(alltable['classroom'])
        render = create_render(session.privilege)
        return render.new_class(pid,teachers,classrooms)

    def POST(self,pid):
        table = alltable['class']
        form = web.input()
        bdate = form['begindate']
        edate = form['enddate']
        byear = int(form['begindate'][0:4])
        bmonth = int(form['begindate'][5:7])
        btime = int(form['begintime'])
        eyear = int(form['enddate'][0:4])
        emonth = int(form['enddate'][5:7])
        etime = int(form['endtime'])
        render = create_render(0)
        if bdate<edate or (bdate==edate and btime<=etime):
            if byear==eyear and bmonth==emonth:
                try:
                    model.new_item(table,form)
                except:
                    return render.error('请选择教师和地点！')
                raise web.seeother('/index_class_project/'+pid)
            elif byear==eyear and emonth-bmonth==1:
                enddate = form['enddate']
                endtime = form['endtime']
                form['enddate'] = datetime.date(year = byear, month = bmonth, day = calendar.monthrange(byear, bmonth)[1])
                form['endtime'] = 1
                model.new_item(table,form)
                form['begindate'] = datetime.date(year = eyear, month = emonth, day = 1)
                form['begintime'] = 0
                form['enddate'] = enddate
                form['endtime'] = endtime
                model.new_item(table,form)
                raise web.seeother('/index_class_project/'+pid)
            else:
                return render.error('时间输入错误！')
        else:
                return render.error('时间输入错误！')


class Delete_class:

    def POST(self,cid,pid):
        model.del_item(alltable['class'],int(cid))
        if pid=='':
            raise web.seeother('/index_class/')
        else:
            raise web.seeother('/index_class_project/'+pid)


class Edit_class:

    def GET(self,cid,pid):
        teachers = model.get_items(alltable['teacher'])
        classrooms = list(model.get_items(alltable['classroom']))
        item = model.get_item(alltable['class'],int(cid))
        render = create_render(session.privilege)
        return render.edit_class(teachers,item,pid,classrooms)

    def POST(self,cid,pid):
        form = web.input()
        model.update_item(alltable['class'],int(cid),form)
        if pid=='':
            raise web.seeother('/index_class/')
        else:
            raise web.seeother('/index_class_project/'+pid)


class Copy_class:

    def GET(self,cid,pid):
        teachers = model.get_items(alltable['teacher'])
        classrooms = list(model.get_items(alltable['classroom']))
        table=alltable['class']
        item = model.get_item(table,int(cid))
        render = create_render(session.privilege)
        return render.copy_class(teachers,item,pid,classrooms)

    def POST(self,cid,pid):
        table = alltable['class']
        form = web.input()
        model.new_item(table,form)
        if pid=='':
            raise web.seeother('/index_class/')
        else:
            raise web.seeother('/index_class_project/'+pid)
    
    
class View_class:

    def GET(self,cid):
        classes = model.get_classes('where cid='+str(cid))[0]
        render = create_render(session.privilege)
        return render.view_class(classes)
    
    
class Approve:
    
    def GET(self,cid):
        cname = model.get_item(alltable['class'],int(cid))['cname']
        render = create_render(session.privilege)
        return render.approve(cid,cname)

    def POST(self,cid):
        form = web.input()
        form['mid'] = session.uid
        model.update_class_approve(form['cid'],form['mid'],form['approve'])
        date = model.get_item(alltable['class'],int(cid))['begindate']
        raise web.seeother('/approve_class/'+date.strftime('%Y-%m'))
    

class Approve_class:
    
    def GET(self,date):
        wh = 'where approve!=\''+'不通过'.decode('utf-8')+'\''\
        +' and YEAR(begindate)='+date[0:4]+' and MONTH(begindate)='+date[5:7]\
        +' order by begindate'
        classes = list(model.get_classes(wh))
        days = calendar.monthrange(int(date[0:4]),int(date[5:7]))[1]
        render = create_render(session.privilege)
        return render.approve_class(classes,date,days)
    
    def POST(self,date):
        date = web.input()['date']
        raise web.seeother('/approve_class/'+date)

    
class Conflict_class:
    
    def GET(self,cid):
        c = model.get_classes('where cid='+cid)[0]
        classes = model.get_conflict_class(c)
        date = classes[0]['begindate'].strftime('%Y-%m')
        render = create_render(session.privilege)
        return render.conflict_class(classes,date,cid)
    
    
class Monthly_summary:
    
    def GET(self,date):
        wh = 'where approve=\''+'通过'.decode('utf-8')+'\''\
        +' and YEAR(begindate)='+date[0:4]+' and MONTH(begindate)='+date[5:7]\
        +' order by begindate'
        classes = list(model.get_classes(wh))
        days = calendar.monthrange(int(date[0:4]),int(date[5:7]))[1]
        render = create_render(session.privilege)
        return render.monthly_summary(classes,date,days)
    
    def POST(self,date):
        date = web.input()['date']
        raise web.seeother('/monthly_summary/'+date)
    
    
if __name__ == '__main__':
    app.run()
