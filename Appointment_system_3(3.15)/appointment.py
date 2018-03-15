# -*- coding:utf-8 -*- ＃  
import web
import model
import datetime
import calendar
import json

web.config.debug = False 
#web.config.session_parameters['timeout'] = 86400

urls = (
    '/', 'Login',
    '/login','Login',
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
    '/teacher_payment_in','Teacher_payment_in',
    '/teacher_payment_out','Teacher_payment_out',
    '/json_get_tlist/(.+)','JsonList',
    '/json_get_tlist_out/(.+)','JsonList_out',
    '/json_get_project','JsonProject',
    '/file_xlsx_payment_in','XlsxPayment_in',
    '/file_xlsx_payment_out','XlsxPayment_out',
    '/file_xlsx_daopan','XlsxDaopan',
    '/file_xlsx_daopan_out','XlsxDaopan_out',
)


app = web.application(urls, globals())
#设置session的存储方式为磁盘.initializer 指定session的初始化值
session = web.session.Session(app, web.session.DiskStore('sessions'),initializer={'login':0,'privilege':0,'uid':0,})

alltable = {'user':['user',['uid','usertype','username','password','full_name','utime']],
    'teacher':['teacher',['tid','tname','company','salary','title','bank_name','bank_number','ttime']],
    'teacher_out':['teacher_out',['tid','tname','sex','id','salary','title','bank_name','bank_number','ttime']],
     'student':['student',['sid','sname','studenttime']],
     'classroom':['classroom',['crid','place','classroom','number','crtime']],
     'project':['project',['pid','oid','pname','budget','snumber','ptime']],
     'class':['class',['cid','pid','tid','mid','crid','cname','begindate','begintime','enddate','endtime','approve','ctime']],
     'payment_history':['payment_history',['hid','tid','bank_num','project_name','hour_count','payment','ptime']]
     }

talbe_c_name ={'user':'用户','password':'密码','teacher':'局内教师','teacher_out':'局外教师','bank_name':'开户银行','username':'登录用户名','full_name':'用户姓名','usertype':'用户类型','utime':'最近修改','tname':'教师姓名','studenttime':'最近修改',
    'tname':'姓名','sname':'姓名','bank_number':'账号','classroom':'场地','crtime':'最近修改','student':'学员','ttime':'最近修改','place':'位置','number':'人数','salary':'师资系数','title':'职称','company':'单位','sex':'性别','id':'身份证号'}


def logged():

    if session.login == 1:
        return True
    else:
        return False

 
def create_render(privilege): 

    if privilege==0:
        render = web.template.render('templates', base='base')
    elif privilege==1:  
        render = web.template.render('templates/admin', base='base')
    elif privilege==2:          
        render = web.template.render('templates/manager', base='base',globals={'date': datetime.datetime.now().strftime('%Y-%m')})
    elif privilege==3:  
        render = web.template.render('templates/organizer', base='base')
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
        if logged():            
            #uid = session.uid
            #user = model.get_item(alltable['user'],uid)
            
            render = create_render(session.privilege)
            #return render.index(user,datetime.datetime.now().strftime('%Y-%m'))
            return render.index(datetime.datetime.now().strftime('%Y-%m'))
        else:
            raise web.seeother('/')

class Index_item:
    
    def GET(self,tablename):
        if logged():            
            table=alltable[tablename]
            items = model.get_items(table)
            render = create_render(session.privilege)
            return render.index_item(table,talbe_c_name,items)
        else:
            raise web.seeother('/')

class New_item:

    def GET(self,tablename):
        if logged():            
            table = alltable[tablename]
            render = create_render(session.privilege)
            return render.new_item(table,talbe_c_name)
        else:
            raise web.seeother('/')

    def POST(self,tablename):
        if logged():
            table = alltable[tablename]
            form = web.input()
            model.new_item(table,form)
            raise web.seeother('/index_item/'+table[0])
        else:
            raise web.seeother('/')

class Delete_item:

    def POST(self,tablename,itemid):
        if logged():
            try:
                table = alltable[tablename]
                model.del_item(table,int(itemid))
                raise web.seeother('/index_item/'+table[0])
            except:
                render = create_render(0)
                return render.error('已被细项包含，无法删除!')
        else:
            raise web.seeother('/')

class Edit_item:

    def GET(self,tablename,itemid):
        if logged():
            table = alltable[tablename]
            item = model.get_item(table,int(itemid))
            render = create_render(session.privilege)
            return render.edit_item(table,talbe_c_name,item)
        else:
            raise web.seeother('/')

    def POST(self,tablename,tid):
        if logged():
            table = alltable[tablename]
            form = web.input()
            model.update_item(table,int(tid),form)
            raise web.seeother('/index_item/'+table[0])
        else:
            raise web.seeother('/')
            

class Index_project:
    
    def GET(self):
        if logged():
            if session.privilege==2:
                wh = ''
            elif session.privilege==3:
                wh = ' and uid='+str(session.uid)
            projects = model.get_projects(wh)
            render = create_render(session.privilege)
            return render.index_project(projects)
        else:
            raise web.seeother('/')
            
class New_project:

    def GET(self):
        if logged():
            render = create_render(session.privilege)
            return render.new_project()
        else:
            raise web.seeother('/')

    def POST(self):
        if logged():
            table = alltable['project']
            form = web.input()
            form['oid'] = session.uid
            model.new_item(table,form)
            raise web.seeother('/index_project')
        else:
            raise web.seeother('/')
            

class Delete_project:

    def POST(self,pid):
        if logged():
            classes_project = list(model.get_classes('where class.pid='+str(pid)))
            if len(classes_project) != 0:
                approval = [a['approve'] for a in classes_project]
                if approval == [u'未审批']*len(approval):
                    for c in classes_project:
                        model.del_item(alltable['class'],int(c['cid']))
                    model.del_item(alltable['project'],int(pid))
                    raise web.seeother('/index_project')
                else:
                    render = create_render(0)
                    return render.error('细项已审批，不能删除!')
            else:
                model.del_item(alltable['project'],int(pid))
                raise web.seeother('/index_project')
        else:
            raise web.seeother('/')

class Edit_project:

    def GET(self,pid):
        if logged():
            table = alltable['project']
            project = model.get_item(table,int(pid))
            render = create_render(session.privilege)
            return render.edit_project(project)
        else:
            raise web.seeother('/')
        

    def POST(self,pid):
        if logged():
            table = alltable['project']
            form = web.input()
            model.update_item(table,int(pid),form)
            raise web.seeother('/index_project')
        else:
            raise web.seeother('/')


class Index_class:
    
    def GET(self,term):
        if logged():
            if session.privilege==3:
                user = 'where u2.uid='+str(session.uid)
                if term=='':
                    classes = list(model.get_classes(user+' order by ctime DESC'))
                elif term=='unapprove':
                    classes = list(model.get_classes(user+' and approve=\'未审批\' order by ctime DESC'))
                elif term=='pass':
                    classes = list(model.get_classes(user+' and approve=\'通过\' order by ctime DESC'))
                elif term=='notpass':
                    classes = list(model.get_classes(user+' and approve=\'不通过\' order by ctime DESC'))
                for c in classes:
                    conflict_class = model.get_conflict_class(c)
                    if len(conflict_class)==1:
                        c['conflict'] = 0
                    else:
                        c['conflict'] = 1    
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
        else:
            raise web.seeother('/')


class Index_class_project:
    
    def GET(self,pid):
        if logged():
            classes = list(model.get_classes('where class.pid='+str(pid)+' order by ctime DESC'))
            if session.privilege==3:
                for c in classes:
                    conflict_class = model.get_conflict_class(c)
                    if len(conflict_class)==1:
                        c['conflict'] = 0
                    else:
                        c['conflict'] = 1
            render = create_render(session.privilege)
            return render.index_class_project(classes,pid,datetime.datetime.now().strftime('%Y-%m'))
        else:
            raise web.seeother('/')

class New_class:

    def GET(self,pid):
        if logged():
            teachers = model.get_items(alltable['teacher'])
            classrooms = model.get_items(alltable['classroom'])
            render = create_render(session.privilege)
            return render.new_class(pid,teachers,classrooms)
        else:
            raise web.seeother('/')

    def POST(self,pid):
        if logged():
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
        else:
            raise web.seeother('/')


class Delete_class:

    def POST(self,cid,pid):
        if logged():
            c = model.get_item(alltable['class'],int(cid))
            if c['approve'] == u'未审批':
                model.del_item(alltable['class'],int(cid))
                if pid=='':
                    raise web.seeother('/index_class/')
                else:
                    raise web.seeother('/index_class_project/'+pid)
            else:
                render = create_render(0)
                return render.error('细项已审批，不能删除！')
        else:
            raise web.seeother('/')


class Edit_class:

    def GET(self,cid,pid):
        if logged():
            teachers = model.get_items(alltable['teacher'])
            classrooms = list(model.get_items(alltable['classroom']))
            item = model.get_item(alltable['class'],int(cid))
            render = create_render(session.privilege)
            return render.edit_class(teachers,item,pid,classrooms)
        else:
            raise web.seeother('/')

    def POST(self,cid,pid):
        if logged():
            form = web.input()
            model.update_item(alltable['class'],int(cid),form)
            if pid=='':
                raise web.seeother('/index_class/')
            else:
                raise web.seeother('/index_class_project/'+pid)
        else:
            raise web.seeother('/')


class Copy_class:

    def GET(self,cid,pid):
        if logged():
            teachers = model.get_items(alltable['teacher'])
            classrooms = list(model.get_items(alltable['classroom']))
            table=alltable['class']
            item = model.get_item(table,int(cid))
            render = create_render(session.privilege)
            return render.copy_class(teachers,item,pid,classrooms)
        else:
            raise web.seeother('/')

    def POST(self,cid,pid):
        if logged():
            table = alltable['class']
            form = web.input()
            model.new_item(table,form)
            if pid=='':
                raise web.seeother('/index_class/')
            else:
                raise web.seeother('/index_class_project/'+pid)
        else:
            raise web.seeother('/')
    
    
class View_class:

    def GET(self,cid):
        if logged():
            classes = model.get_classes('where cid='+str(cid))[0]
            render = create_render(session.privilege)
            return render.view_class(classes)
        else:
            raise web.seeother('/')
        
    
class Approve:
    
    def GET(self,cid):
        if logged():
            cname = model.get_item(alltable['class'],int(cid))['cname']
            render = create_render(session.privilege)
            return render.approve(cid,cname)
        else:
            raise web.seeother('/')

    def POST(self,cid):
        if logged():
            form = web.input()
            form['mid'] = session.uid
            model.update_class_approve(form['cid'],form['mid'],form['approve'])
            date = model.get_item(alltable['class'],int(cid))['begindate']
            raise web.seeother('/approve_class/'+date.strftime('%Y-%m'))
        else:
            raise web.seeother('/')
    

class Approve_class:
    
    def GET(self,date):
        if logged():
            '''
            wh = 'where (approve!=\''+'不通过'.decode('utf-8')+'\' or approve ISNULL)'\
            +' and ((strftime(\'%Y\',begindate)=\''+date[0:4]+'\' and strftime(\'%m\',begindate)=\''+date[5:7]+'\') or begindate ISNULL)'\
            +' order by ctime DESC'
            '''
            wh = 'where approve!=\''+'不通过'.decode('utf-8')+'\''\
            +' and strftime(\'%Y\',begindate)=\''+date[0:4]+'\' and strftime(\'%m\',begindate)=\''+date[5:7]\
            +'\' order by begindate'
            classes = list(model.get_classes(wh))
            days = calendar.monthrange(int(date[0:4]),int(date[5:7]))[1]
            render = create_render(session.privilege)
            return render.approve_class(classes,date,days)
        else:
            raise web.seeother('/')
    
    def POST(self,date):
        if logged():
            date = web.input()['date']
            raise web.seeother('/approve_class/'+date)
        else:
            raise web.seeother('/')

    
class Conflict_class:
    
    def GET(self,cid):
        if logged():
            c = model.get_classes('where cid='+cid)[0]
            classes = model.get_conflict_class(c)
            date = c['begindate'].strftime('%Y-%m')
            render = create_render(session.privilege)
            return render.conflict_class(classes,date,cid)
        else:
            raise web.seeother('/')
        
    
class Monthly_summary:
    
    def GET(self,date):
        if logged():
            wh = 'where approve=\''+'通过'.decode('utf-8')+'\''\
            +' and strftime(\'%Y\',begindate)=\''+date[0:4]+'\' and strftime(\'%m\',begindate)=\''+date[5:7]\
            +'\' order by begindate'
            classes = list(model.get_classes(wh))
            days = calendar.monthrange(int(date[0:4]),int(date[5:7]))[1]
            render = create_render(session.privilege)
            return render.monthly_summary(classes,date,days)
        else:
            raise web.seeother('/')
    
    def POST(self,date):
        if logged():
            date = web.input()['date']
            raise web.seeother('/monthly_summary/'+date)
        else:
            raise web.seeother('/')
 
class Teacher_payment_in:    
    def GET(self):
        if logged():
            render = create_render(session.privilege)
            return render.teacher_payment_in()
        else:
            raise web.seeother('/')
    
    def POST(self,date):
        if logged():
            raise web.seeother('/teacher_payment_in/')
        else:
            raise web.seeother('/')

 
class Teacher_payment_out: 
    def GET(self):
        if logged():
            render = create_render(session.privilege)
            return render.teacher_payment_out()
        else:
            raise web.seeother('/')
    
    def POST(self,date):
        if logged():
            raise web.seeother('/teacher_payment_out/')
        else:
            raise web.seeother('/')


###########以下为json查询字段
class JsonList:
    def GET(self,tname):
        if logged():
            web.header('content-type','text/json')
            teacherlist=list(model.get_teacher_by_name(tname))
            return json.dumps(teacherlist)
        else:
            return [];

class JsonList_out:
    def GET(self,tname):
        if logged():
            web.header('content-type','text/json')
            teacherlist=list(model.get_teacher_out_by_name(tname))
            return json.dumps(teacherlist)
        else:
            return [];

class JsonProject:
    def GET(self):
        if logged():
            web.header('content-type','text/json')
            if session.privilege==2:
                wh = ''
            elif session.privilege==3:
                wh = ' and uid='+str(session.uid)
            projectslist = list(model.get_projects(wh))            
            return json.dumps(projectslist)    
        else:
            return [];

class XlsxPayment_in:
    def GET(self):
        raise web.seeother('/')
    def POST(self):
        data=web.input()        
        xlsxData=json.loads(data['jsonstr'])      
        ptime=data['ptime']  
        pname=data['pname']  
        web.header('Content-type','application/vnd.ms-excel')  #指定返回的类型
        web.header('Transfer-Encoding','chunked')
        web.header('Content-Disposition','attachment;filename="download.xlsx"') #设定用户浏览器显示的保存文件名
        return model.get_xlsx_payment_in(xlsxData,ptime,pname)

class XlsxPayment_out:
    def GET(self):
        raise web.seeother('/')
    def POST(self):
        data=web.input()        
        xlsxData=json.loads(data['jsonstr'])      
        ptime=data['ptime']  
        pname=data['pname']  
        web.header('Content-type','application/vnd.ms-excel')  #指定返回的类型
        web.header('Transfer-Encoding','chunked')
        web.header('Content-Disposition','attachment;filename="download.xlsx"') #设定用户浏览器显示的保存文件名
        return model.get_xlsx_payment_out(xlsxData,ptime,pname)

class XlsxDaopan:
    def GET(self):
        raise web.seeother('/')
    def POST(self):
        data=web.input()        
        xlsxData=json.loads(data['jsonstr'])      
        
        web.header('Content-type','application/vnd.ms-excel')  #指定返回的类型
        web.header('Transfer-Encoding','chunked')
        web.header('Content-Disposition','attachment;filename="download.xlsx"') #设定用户浏览器显示的保存文件名
        return model.get_xlsx_daopan(xlsxData)

class XlsxDaopan_out:
    def GET(self):
        raise web.seeother('/')
    def POST(self):
        data=web.input()        
        xlsxData=json.loads(data['jsonstr'])      
        
        web.header('Content-type','application/vnd.ms-excel')  #指定返回的类型
        web.header('Transfer-Encoding','chunked')
        web.header('Content-Disposition','attachment;filename="download.xlsx"') #设定用户浏览器显示的保存文件名
        return model.get_xlsx_daopan_out(xlsxData)

if __name__ == '__main__':
    
    app.run()
