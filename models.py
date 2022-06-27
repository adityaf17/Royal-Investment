
from mainApp import db
from sqlalchemy.sql import func



class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    email = db.Column(db.String(30),unique_key=True)
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    contact = db.Column(db.Integer,nullable=False)

# class Courses(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     course_name = db.Column(db.String(30),nullable=False)
#     tagline = db.Column(db.String(100),nullable=False)
#     content=db.Column(db.String(200),nullable=False)

class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(80),nullable=False)
    slug=db.Column(db.String(20),nullable=False)
    content=db.Column(db.String(1000),nullable=False)
    tagline=db.Column(db.String(120),nullable=False)
    img_file=db.Column(db.String(18),nullable=True)
