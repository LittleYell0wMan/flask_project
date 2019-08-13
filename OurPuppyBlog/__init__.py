import os
from flask import Flask,render_template,request,Blueprint,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_dance.contrib.google import make_google_blueprint,google

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(client_id='755499121072-0i1adi7qar16pn6ctjnpvjk81gig912i.apps.googleusercontent.com',
                                  client_secret='TsfjWafpwnizOTExdHGsxBtL', offline=True, scope=['profile','email'])

db = SQLAlchemy(app)
Migrate(app,db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from OurPuppyBlog.core.views import core
from OurPuppyBlog.users.views import users
from OurPuppyBlog.blog_posts.views import blog_posts
from OurPuppyBlog.error_pages.handlers import error_pages

app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(blueprint, url_prefix='/login')


@app.route('/login/google')
def login():
    if not google.authorized:
        return render_template(url_for('google.login'))

    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']

    return render_template('welcome.html',email=email)

@app.route('/welcome')
def welcome():
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    email = resp.json()['email']

    return render_template('welcome.html', email=email)
