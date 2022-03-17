import datetime
from datetime import date

from flask import Flask, render_template
from flask_login import login_user, LoginManager, logout_user, login_required
from werkzeug.utils import redirect

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.jobs import JobsForm
from forms.login import LoginForm
from forms.register import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
            modified_date=datetime.datetime.now())
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def jobs():
    jobs = JobsForm()
    if jobs.validate_on_submit():
        session = db_session.create_session()
        job = Jobs()
        job.team_leader = jobs.team_leader.data
        job.job = jobs.job.data
        job.work_size = jobs.work_size.data
        job.collaborators = jobs.collaborators.data
        job.start_date = date.today()
        job.end_date = date.today()
        job.is_finished = jobs.is_finished.data
        session.add(job)
        session.commit()
        return redirect('/')
    return render_template('jobs.html', form=jobs, title='addjob')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def index():
    session = db_session.create_session()
    job = session.query(Jobs).all()
    return render_template('journal.html', jobs=job)


db_session.global_init("db/blogs.db")
app.run()
