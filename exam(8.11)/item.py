# -*- coding:utf-8 -*- ＃  
import web
import model

### Url mappings
urls = (
    '/', 'Main',
    '/index/(.+)', 'Index',
    '/view/(.+)/(\d+)', 'View',
    '/new/(.+)', 'New',
    '/delete/(.+)/(\d+)', 'Delete',
    '/edit/(.+)/(\d+)', 'Edit',
    '/index_project', 'Index_project',
    '/view_project/(\d+)', 'View_project',
    '/new_project', 'New_project',
    '/delete_project/(\d+)', 'Delete_project',
    '/edit_project/(\d+)', 'Edit_project',
    '/apply/(\d+)','Apply',
    '/approve/(\d+)/(\d*)','Approve',
    '/index_class/(\d*)', 'Index_class',
    '/view_class/(\d+)', 'View_class',
    '/new_class/(\d+)', 'New_class',
    '/delete_class/(\d+)/(\d*)', 'Delete_class',
    '/edit_class/(\d+)/(\d*)', 'Edit_class',
    '/copy_class/(\d+)/(\d*)', 'Copy_class',
)

### Templates
t_globals = {
    'datestr': web.datestr
}
render = web.template.render('E:\\Python27\\templates\\exam', base='base', globals=t_globals)


alltable={'teacher':['teacher',['tid','tname','bank_number','ttime']],
     'student':['student',['sid','sname','studenttime']],
     'manager':['manager',['mid','mname','mtime']],
     'organizer':['organizer',['oid','oname','otime']],
     'classroom':['classroom',['crid','place','classroom','crtime']],
     'project':['project',['pid','oid','pname','budget','apply','ptime']],
     'class':['class',['cid','pid','tid','mid','crid','cname','begindate','begintime','enddate','endtime','approve','ctime']],
     }


class Main:

    def GET(self):
        return render.main()
    

class Index:
    
    def GET(self,tablename):
        table=alltable[tablename]
        """ Show page """
        items = model.get_items(table)
        return render.index(table,items)


class View:
    
    def GET(self,tablename,itemid):
        table=alltable[tablename]
        """ View single item """
        item = model.get_item(table,int(itemid))
        return render.view(table,item)


class New:

    def GET(self,tablename):
        table=alltable[tablename]
        return render.new(table)

    def POST(self,tablename):
        table=alltable[tablename]
        form=web.input()
        model.new_item(table,form)
        raise web.seeother('/index/'+table[0])


class Delete:

    def POST(self,tablename,itemid):
        table=alltable[tablename]
        model.del_item(table,int(itemid))
        raise web.seeother('/index/'+table[0])


class Edit:

    def GET(self,tablename,itemid):
        table=alltable[tablename]
        item = model.get_item(table,int(itemid))
        return render.edit(table,item)


    def POST(self,tablename,tid):
        table=alltable[tablename]
        form=web.input()
        model.update_item(table,int(tid),form)
        raise web.seeother('/index/'+table[0])


class Index_project:
    
    def GET(self):
        table=alltable['project']
        items = model.get_projects()
        return render.index_project(table,items)


class View_project:
    
    def GET(self,pid):
        table=alltable['project']
        item = model.get_item(table,int(pid))
        return render.view_project(table,item)


class New_project:

    def GET(self):
        table=alltable['project']
        return render.new_project(table)

    def POST(self):
        table=alltable['project']
        form=web.input()
        model.new_item(table,form)
        raise web.seeother('/index_project')


class Delete_project:

    def POST(self,pid):
        table=alltable['project']
        model.del_item(table,int(pid))
        raise web.seeother('/index_project')


class Edit_project:

    def GET(self,pid):
        table=alltable['project']
        item = model.get_item(table,int(pid))
        return render.edit_project(table,item)


    def POST(self,pid):
        table=alltable['project']
        form=web.input()
        model.update_item(table,int(pid),form)
        raise web.seeother('/index_project')

    
class Apply:
    
    def GET(self,pid):
        organizers = model.get_items(alltable['organizer'])
        project = model.get_item(alltable['project'],int(pid))
        pname=project['pname']
        return render.apply(organizers,pid,pname)


    def POST(self,pid):
        form=web.input()
        model.update_project_apply(form['pid'],form['oid'])
        raise web.seeother('/index_project')


class Approve:
    
    def GET(self,cid,pid):
        managers = model.get_items(alltable['manager'])
        cname=model.get_item(alltable['class'],int(cid))['cname']
        return render.approve(managers,cid,cname,pid)


    def POST(self,cid,pid):
        form=web.input()
        model.update_project_approve(form['cid'],form['mid'])
        raise web.seeother('/index_class/'+pid)


class Index_class:
    
    def GET(self,pid):
        if pid=='':
            classes = model.get_classes()
        else:
            classes = model.get_pclasses(pid)
        return render.index_class(classes,pid)


class View_class:
    
    def GET(self,cid):
        table=alltable['class']
        item = model.get_item(table,int(cid))
        return render.view_class(table,item)


class New_class:

    def GET(self,pid):
        teachers = model.get_items(alltable['teacher'])
        classrooms = model.get_items(alltable['classroom'])
        table=alltable['class']
        return render.new_class(table,pid,teachers,classrooms)

    def POST(self,pid):
        table=alltable['class']
        form=web.input()
        model.new_item(table,form)
        raise web.seeother('/index_class/'+pid)


class Delete_class:

    def POST(self,cid,pid):
        table=alltable['class']
        model.del_item(table,int(cid))
        raise web.seeother('/index_class/'+pid)


class Edit_class:

    def GET(self,cid,pid):
        teachers = model.get_items(alltable['teacher'])
        classrooms = list(model.get_items(alltable['classroom']))
        table=alltable['class']
        item = model.get_item(table,int(cid))
        return render.edit_class(table,teachers,item,pid,classrooms)


    def POST(self,cid,pid):
        table=alltable['class']
        form=web.input()
        model.update_item(table,int(cid),form)
        raise web.seeother('/index_class/'+pid)


class Copy_class:

    def GET(self,cid,pid):
        teachers = model.get_items(alltable['teacher'])
        classrooms = list(model.get_items(alltable['classroom']))
        table=alltable['class']
        item = model.get_item(table,int(cid))
        return render.copy_class(table,teachers,item,pid,classrooms)


    def POST(self,cid,pid):
        table=alltable['class']
        form=web.input()
        model.new_item(table,form)
        raise web.seeother('/index_class/'+pid)

if __name__ == '__main__':
    app = web.application(urls, globals())
    app.run()
