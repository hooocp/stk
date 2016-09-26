django learning


django-admin.py startproject demo 
(TIME_ZONE='Asia/Shanghai'
languige-code'zh-cn'
installed_app 'blog',)


url(r'^blog/index/$','blog.views.index')

django-admin.py startapp blog


from django.http import HttpResponse
def index(req):
    return HttpResponse('<h1>hello</h1>')

python manage.py runserver

=======================
mkdir blog/templates/

mv *  blog/templates/

from django.http import HttpResponse
from  django.template import loader, Context

def index(req):
    t = loader.get_template('index.html')
    c = Context({})

    return HttpResponse(t.render(c))


from django.shortcuts import render_to_response
def index(req):
    return render_to_response('index.html',{})

python manage.py runserver


=======================
模板变量{{title}} in index.html

from django.shortcuts import render_to_response
def index(req):
    user = {'name:':'lala', 'age':15, 'sex': 'male'}
    return render_to_response('index.html',{'title':'test var','user':user})

模板变量{{user.name1}} {{booklist.0}}  {{user.say,无参数}} in index.html  字典 对象属性 对象方法 list 
from django.shortcuts import render_to_response
class Perso(object):
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex
    def say(self):
        return self.name



user = Perso('tom',23,'male')
booklist = ['python','java']

def index(req):
    -- user = {'name:':'lala', 'age':15, 'sex': 'male'}
    return render_to_response('index.html',{'title':'test var','user':user,'booklist':booklist})



====第四== {%if%} tags的使用,直接调用。py文件的东西

<body>
    <body>

{% if user % manumal book}

{% else%}

{%endif%}


{%for book in books% }
<li>{{forloop.counter}}{{book}} <li>
{%endfor%}

=====第五===模板的使用

mkdir templates

url.py add url(r'^index/$','blog.views.index'),url(r'^index1/$','blog.views.index1'),url(r'^index2/$','blog.views.index2'),




----------------------



---------------------


from django.templates import loader ,Context,Template
from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(req):
    t=loader.get_template('index.html') #create index.html  manumal
    c= Context({'uname':'alen'})
    html=t.render(c)     #html 为字符串
    return HttpResponse(html)


def index1(req):
    t=Template('<h1>hello{{uname}}</h1>')
    c=Context({'uname':'csv'})
    return HttpResponse(t.render(c))
    
def index2(req):
    return render_to_response('index.html',{'uname':'csv01'})




====url.py 使用
url(r'^index/$'(正则表达式),'blog.views.index'（处理方法）)



from blog.views import index 
url(r'^index/$'(正则表达式),index（处理方法）)


urlpatterbs = patterns('blog.views',
        url(r'^index/$'(正则表达式),'index'（处理方法）)



 url(r'^index/(?P<id>\d{2})/$','index') 注意传递的参数(位置参数，关键字参数)
def index(req,id):


====数据库的使用1====

django-admin.py startproject csvdbtest

settings.py  add app 
DATABASE 'ENGINE':'django.db.backends.mysql'
         
models

from django.db import models

class Employee(object):
    """docstring for Employee"""
    name = models.CharField(max_length=20)

python manage.py syncdb


====数据库的使用2====
from django.db import models

class Employee(object):
    """docstring for Employee"""
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


ipython manage.py shell
from blog.models import Employee
emp = Employee() # or emp = Employee(name = 'hahaa')
emp.name = 'Hahah' 
emp.save()
emp = Employee(name = 'hahaa')
emp.save()

Employee.object.create(name = 'max')

emp = Employee.object.create(name = 'max')

emps = Employee.object.all()



from django.shortcuts import render_to_response
from blog.models import Employee

def index(req):
    emps = Employee.object.all()
    return render_to_response('index.html', {'emps':emps})

mkdir blog/templates/index.html



====数据库的使用3====



change models.py
from django.db import models

class Entry(object):
    """docstring for Entry"""
    name = models.CharField(max_length=30)
    def __unicode__():
        return self.name


class Blog(object):
    """docstring for Blog"""
    name = models.CharField(max_length=30)
    entry = models.ForeignKey(Entry)
     
     def __unicode__():
            return self.name



ipython manage.py shell 

from blog.models import Entry, Blog

entry1 = Entry.object.create(name = 'alen')
entry2 = Entry.object.create(name='hahaa')
entry3 = Entry.object.create(name='hi')


blog1 = Blog.object.create(name='alen_blog')
blog2 = Blog.object.create(name='hahaa_blog')
blog3 = Blog.object.create(name='hi_blog')


blog1.entry_id


entry1.blog_set.all()





====数据库的使用admin 使用====
settings.py change installed_app   反注释 django.contrib.admin (数据库 安装app 时区等) 


url.py  url(,include(admin.site,url)) 打开

from django.db import models

sex_choice = (('f','female'),('m','male'))
class User(models.Model):
    name = models.CharField(max_length=30)
    sex =models.CharField(max_length=1, choices=sex_choice)
    def __unicode__(self):
        return self.name
        


vi admin.py

from django.contrib import admin
from blog.models import User

admin.site.register(User)


=====many to many 模型====

from django.db import models

class Author(models.Model)
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

class  Book(models.Model):
    name = models.CharField(max_length=30)
    author = models.ManyToManyField(Author)
    def __unicode__(self):
        return self.name

ipython create Authors 
from blog.object import Author,Book 
Author.object.create(name='Alen')
b1=Book(b1.name='python books')
 
======views===

mkdir templates
vi views.py
from blog.models import Author,Book
from django.shortcuts import render_to_response
def show_author(req):
    author = Author.object.all()
    return render_to_response('show_author.html', {'author':authors})





====form=====

django-admin.py startproject csv07

django-admin.py startapp blog


vi settings.py
vi url.py


vi views

from django import forms
from django.http import HttpResponse
from django.shortcuts import render_to_response

class User_form(form.Form):
    """docstring for User_form"""
    name = form.CharField()

    def __init__(self, arg):
        super(User_form, self).__init__()
        self.arg = arg
        

def register(req):
    if req.method == 'POST':
        form = User_form(req.POST)
            if form.is_valid():
                print(form.cleaned_data)
                return HttpResponse('Ok')
    else :
        form = User_form()
    return render_to_response('register.html', {'form': form})

vi register.html
<form method='POST'>
{{form}}
<input type='submit' value='ok'/>
</form>



