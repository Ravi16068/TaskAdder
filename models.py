from app import db

#import flask_sqlalchemy import SQLalchemy

#db= SQLalchemy()

#class User(db.Model):

   #  __tablename__="users"
    #id = db.Column(db.Integer,primary_key=True)
  #  username =db.Column(db.String(25),unique=True,nullable=False)
 #   password =db.Column(db.String(),nullable=False)

#    db.create_all()





class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f'{self.title}'

