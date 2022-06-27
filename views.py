from datetime import date, datetime
from flask import Blueprint,request,render_template,redirect,session,Flask
from flask_mail import Mail
import json
from mainApp import db
from models import Contacts,Posts
import math



with open('config.json', 'r') as c:
    params = json.load(c)["params"]

views=Blueprint('views',__name__)

app = Flask(__name__)
app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = True,
    MAIL_USERNAME = params['gmail-user'],
    MAIL_PASSWORD=  params['gmail-password']
)
mail = Mail(app)



@views.route("/",methods=['GET' ])
def home():
    return render_template('index.html',params=params)



@views.route("/products",methods=['GET'])
def products():
    return render_template('products.html')



@views.route("/contact_us", methods=['POST','GET'])
def contact_us():
    if request.method == 'POST':
        name=request.form.get('name')
        email=request.form.get('email')
        contact=request.form.get('phone')

        contact_info = Contacts(name=name,email=email,date=datetime.now(),contact=contact)
        db.session.add(contact_info)
        db.session.commit()
        

        mail.send_message('New message from ' + name,
                          sender=email,
                          recipients = [params['gmail-user']],
                          body = contact
                          )

        return redirect('/')

    return render_template('contact.html',params=params)


@views.route("/about")
def about():
    return render_template('about.html')




@views.route("/blogs")
def post():
    blogs = Posts.query.filter_by().all()

    last = math.ceil(len(blogs)/int(params['no_of_posts']))

    page = request.args.get('page')
    if(not str(page).isnumeric()):
        page=1
    page = int(page)
    blogs = blogs[(page-1)*int(params['no_of_posts']):(page-1)*int(params['no_of_posts'])+int(params['no_of_posts'])]

    if (page==1):
        prev='#'
        next = "/?page="+str(page+1)
    elif (page==last):
        prev = "/?page=" + str(page-1)
        next = "#"
    else:
        prev = "/?page=" + str(page-1)
        next = "/?page=" + str(page+1)

    return render_template('blogs.html',blogs=blogs,params=params,prev=prev,next=next)



@views.route("/post/<string:blog_slug>")
def post_route(blog_slug):
    blog = Posts.query.filter_by(slug=blog_slug).first()

    return render_template('blog.html',blog=blog)



@views.route("/dashboard",methods=['POST','GET'])
def dashboard():
    if ("user" in session and session['user'] == params['admin_user']):

        blogs = Posts.query.all()

        return render_template('dashboard.html',blogs=blogs,params=params)

    if request.method == 'POST':

        username = request.form.get('uname')
        password = request.form.get('pass')

        if username == params['admin_user'] and password == params['admin_password']:
            session['user'] = username
            blogs = Posts.query.all()

            return render_template('dashboard.html',params=params,blog=blogs)

    return render_template('login.html',params=params)



@views.route("/edit/<string:id>",methods=['GET','POST'])
def edit(id):
    if 'user' in session and session['user'] == params['admin_user']:
        if request.method == 'POST':
            title = request.method.get('title')
            slug = request.method.get('slug')
            content = request.method.get('content')
            tagline = request.method.get('tagline')
            img_file = request.method.get('img')

            if id == "0":
                entry = Posts(title=title,slug=slug,content=content,tagline=tagline,img_file=img_file)
                db.session.add(entry)
                db.session.commit()

            else:
                blogs = Posts.query.filter_by(id=id).first()
                blogs.title = title
                blogs.slug = slug
                blogs.content = content
                blogs.tagline = tagline
                blogs.img_file = img_file

                db.session.commit()
                return redirect('/edit/'+ id )

    blog = Posts.query.filter_by(id=id).first()
    return render_template('edit.html',blog=blog,params=params,id=id)


@views.route('/delete/<string:id>',methods=['GET','POST'])
def delete(id):
    if 'user' in session and session['user'] == params['admin_user']:
        blog = Posts.query.filter_by(id=id).first()
        db.session.delete(blog)
        db.session.commit()
    return redirect('/dashboard')


@views.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')


