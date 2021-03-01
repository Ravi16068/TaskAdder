from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required,UserManager,UserMixin,SQLAlchemyAdapter




app = Flask(__name__)
app.config['SECRET_KEY'] = '8u3rouhfkjdsfiluh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['CSRF_ENABLED']=True
app.config['USER_ENABLE_EMAIL']=False
app.config['Testing']=False

db = SQLAlchemy(app)


from routes import *

if __name__ == '__main__':
    app.run(debug=True)
    #host="192.168.43.239"








