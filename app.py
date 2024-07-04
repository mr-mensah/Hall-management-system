from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, or_
from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
# from itsdangerous import SignatureExpired
from flask_mail import Mail,Message
from flask_login.utils import login_user
from werkzeug.utils import redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_manager, login_user, LoginManager, login_required, logout_user, current_user
from datetime import datetime
import os
# import sys
# import logging
# import click
# from flask.cli import with_appcontext

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir,'ugelhall.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']= 465
app.config['MAIL_USERNAME']= 'hubertdeveloped@gmail.com'
app.config['MAIL_PASSWORD']= '*******'
app.config['MAIL_DEFAULT_SENDER']= 'hubertdeveloped@gmail.com'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'hubertdeveloped@gmail.com'
app.config['MAIL_PASSWORD'] = 'asare1234567'

mail = Mail(app)

serial=Serializer(app.config['SECRET_KEY'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# @click.command(name='create_tables')
# @with_appcontext
# def create_tables():
#     db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#===============================================================Database Tables============================================================
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True, nullable=False)
    surname = db.Column(db.String(30), nullable=False)
    othernames = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    room_number = db.Column(db.String(5), nullable=False)
    contact = db.Column(db.String(20), unique=True, nullable=False)
    course = db.Column(db.String(150), nullable=False)
    level = db.Column(db.String(3), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    hall = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String(30), nullable=False)
    othernames = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    contact = db.Column(db.String(18), unique=True, nullable=False)
    portfolio = db.Column(db.String(30), nullable=False)
    hall = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.String(6), nullable=False)

    def get_reset_token(self, expires_sec=600):
        serial = Serializer(app.config['SECRET_KEY'], expires_sec)
        return serial.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        serial = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = serial.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return '<User %r>' % self.id

class Complaints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    std_fullname = db.Column(db.String(150), nullable=False)
    room_number = db.Column(db.String(5), nullable=False)
    hall = db.Column(db.String(30), nullable=False)
    issue_type = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120), nullable=False)
    event_type = db.Column(db.String(25), nullable=False)
    event_desc = db.Column(db.String)
    event_date = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

class Activities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doer = db.Column(db.String(200), nullable=False)
    event = db.Column(db.String(200), nullable=False)
    date_of_event = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id

class Keylog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(5), nullable=False)
    loggers_name = db.Column(db.String(150), nullable=False)
    time_in = db.Column(db.DateTime, default=datetime.utcnow)
    collectors_name = db.Column(db.String(150))
    time_out = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.id

class Visitors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visitors_name = db.Column(db.String(150), nullable=False)
    id_type = db.Column(db.String(20), nullable=False)
    id_number = db.Column(db.String(30), nullable=False)
    hostname = db.Column(db.String(150), nullable=False)
    hall = db.Column(db.String(30), nullable=False)
    room_number = db.Column(db.String(5), nullable=False)
    contact = db.Column(db.String(18), nullable=False)
    time_in = db.Column(db.DateTime, default=datetime.utcnow)
    time_out = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % self.id

class Passcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    newpasscode = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

class CheckedIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True, nullable=False)
    fullname = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(8), nullable=False)
    hall = db.Column(db.String(30), nullable=False)
    room_number = db.Column(db.String(5), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(18), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

class Account_Ugel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, unique=True, nullable=False)
    room_number = db.Column(db.String(5), nullable=False)
    transaction_nbr = db.Column(db.String(200), unique=True, nullable=False)
    payment_mode = db.Column(db.String(10), nullable=False)
    fees_paid = db.Column(db.REAL, nullable=False)
    level = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

with app.app_context():
    db.create_all()
#==============================================================CheckIn Students========================================================
@app.route('/checkIn', methods=['POST','GET'])
def checkIn():
    if request.method == "POST":     
            payment_mode = request.form['payment_mode']
            student_id = request.form['student_id']
            transaction_nbr = request.form['transaction_nbr'].upper()
            account = Account_Ugel.query.filter(Account_Ugel.transaction_nbr==transaction_nbr and Account_Ugel.payment_mode==payment_mode).first()
            if(account):
                student = Student.query.filter(Student.student_id == student_id).first()
                checkid = account.student_id==student_id
                if (checkid):
                    info = CheckedIn(
                        student_id = student_id,
                        fullname = student.surname+" "+student.othernames,
                        gender = student.gender,
                        room_number = student.room_number,
                        hall = student.hall,
                        level = student.hall,
                        course = student.course,
                        contact = student.contact)
                try:
                    db.session.add(info)
                    db.session.commit()  
                    message = "You have successfully Checked In To Room, "+ student.room_number +". Return to the Lodge for your Souvernirs!"
                    return successhandler(message)
                except:
                    # replace with nicer experience
                    error_statement = "Error: Transaction_ID Does Not Match Its Paid Student ID!"
                    return errorhandler(error_statement)
            else:
                error_statement = "To check in to your room, your hall fees must be paid!"
                return errorhandler(error_statement)
    else:
        return render_template('checkIn.html')


#==================================================================Home Page===============================================================
@app.route('/')
def index():
    return render_template('home.html')

#==================================================================Login Page==============================================================
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username').title()
        password = request.form.get('password')
        session['user'] = username
        user = User.query.filter_by(username=username).first()
        if not user or not check_password_hash(user.password,password):
            error_statement = "Please Enter Your Correct Login Credentials!"
            return errorhandler(error_statement)
        else:
            login_user(user)
            return redirect(url_for('dashboard'))
    else:
        return render_template("login.html")

#==============================================================Reset Password After ForgetPassword==============================================================
def send_mail(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",recipients = [user.email])
    msg.body=f'''To reset your password please follow the link below:
    {url_for('resetWithToken',token=token, _external=True)}
    If you did not send a password reset request, then ignore this message.'''

    mail.send(msg)

@app.route('/forgotpassword', methods=['POST','GET'])
def forgotpassword():
    if request.method == 'POST':
        email=request.form.get('email').lower()
        user=User.query.filter(User.email==email).first()
        message = 'check your mail for a confirmation link!'
        if user:
            try:
                send_mail(user)
                flash (message)
            except:
                # message ='This email is not recognized!'
                flash(message)
    return render_template('forgotpassword.html')

@app.route('/forgotpassword/<token>', methods=['POST', 'GET'])
def resetWithToken(token):
    user = User.verify_reset_token(token)
    if user is None:
        error_message= "The token Expired!"
        errorhandler(error_message)
        return redirect(url_for('forgotpassword'))
    elif request.method == 'POST':
        newpassword = generate_password_hash(request.form['password'])
        try:
            user.password = newpassword
            db.session.commit()
            success = "Password Changed Successfully. Please Login!"
            successhandler(success)
            return redirect(url_for('login'))
        except:
            error="An error occured whiles changing password!"
            errorhandler(error)
    return render_template ('resetpassword.html')


#==================================================================Signup Page=============================================================
@app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method == "POST":     
        recievedpasscode = request.form['passcode']
        currentpasscode= Passcode.query.order_by(desc(Passcode.id)).first()
        if recievedpasscode == currentpasscode.newpasscode:
                    username = request.form['username'].title()
                    surname = request.form['surname'].title()
                    othernames = request.form['othernames'].title()
                    portfolio = request.form['staff-type']
                    gender = request.form['gender'].title()
                    email = request.form['email'].lower()
                    password = generate_password_hash(request.form['password'])
                    contact = request.form['contact']
                    hall = request.form['hall'].title()
                    
                    TutorsCount= User.query.filter(User.hall==hall and User.portfolio=="Hall Tutor").count()
                    if (portfolio == "Hall Tutor" and TutorsCount<1):
                        user_info = User(
                            username = username,
                            surname = surname,
                            othernames = othernames,
                            portfolio = portfolio,
                            gender = gender,
                            email = email,
                            password = password,
                            contact = contact,
                            hall = hall,
                        )
                    elif (portfolio != "Hall Tutor"):
                        user_info = User(
                            username = username,
                            surname = surname,
                            othernames = othernames,
                            portfolio = portfolio,
                            gender = gender,
                            email = email,
                            password = password,
                            contact = contact,
                            hall = hall,
                        )
                    try:
                        db.session.add(user_info)
                        db.session.commit()  
                        # Add new data to db
                        return redirect(url_for("login"))
                    except:
                        # replace with nicer experience
                        error_statement = "Error: Username already exists or You can't be the Hall Tutor!"
                        return errorhandler(error_statement)
        else:
            error_statement = "Passcode provided is invalid, visit your Admin for a Passcode"
            return errorhandler(error_statement)
        
    else:
        return render_template('signup.html')

#============================================================Reset Passcode=============================================================
@app.route('/resetpasscode', methods=['POST', 'GET'])
@login_required
def resetpasscode():
    if request.method == "POST":
        new = request.form['new']
        old = request.form['old']
        recentpasscode= Passcode.query.order_by(desc(Passcode.id)).first()
        if (old == recentpasscode.newpasscode):
            data = Passcode(
                newpasscode= new
                )

        else:
            error_message= "Incorrect Old Passcode Entered!"
            return errorhandler(error_message),400
        try:
                db.session.add(data)
                db.session.commit()
                message="Passcode changed successfully!"
                return successhandler(message)
        except:
                error_message = "Changing Passcode Was Unsuccessful"
                return errorhandler(error_message),400
    else:
        return render_template('resetpasscode.html')

#============================================================Change UserPassword=============================================================
@app.route('/changepassword/<int:id>', methods=['POST', 'GET'])
@login_required
def changepassword(id):
    if request.method == "POST":
                new = request.form['new']
                old = request.form['old']
                currentuser = User.query.filter(User.id==id).first()
                if (check_password_hash(currentuser.password,old)):
                    currentuser.password = generate_password_hash(new)
                    try:
                            db.session.commit()
                            message="Password changed successfully!"
                            return successhandler(message)
                    except:
                            error_message = "Changing Password Was Unsuccessful"
                            return errorhandler(error_message),400
                else:
                    error_message= "Entered Old Password Is Incorrect!"
                    return errorhandler(error_message),400
    else:
        return render_template('changepassword.html')
        
#==============================================================SuccessHandling Page===========================================================
@app.route('/successhandling', methods=['POST','GET'])
def successhandler(success_message):
    return render_template('successhandler.html',success_message=success_message)

#==============================================================Errorhandling Page===========================================================
@app.route('/errorhandling', methods=['POST','GET'])
def errorhandler(error_message):
    return render_template('errorhandling.html',error_message=error_message)

#==============================================================Dashboad Page===============================================================
@app.route('/dashboard', methods=['POST','GET'])
@login_required
def dashboard():
    Male = Student.query.filter(Student.gender == "Male").count()
    Female = Student.query.filter(Student.gender == "Female").count()
    Activity = Activities.query.order_by(desc(Activities.date_of_event)).limit(4).all()
    PostedEvents = Events.query.order_by(desc(Events.event_date)).limit(4).all()
    return render_template('dashboard.html',Activity=Activity,Male=Male,Female=Female,PostedEvents=PostedEvents)

# -------------------------------Search Page---------------------------
@app.route('/search', methods=['POST','GET'])
@login_required
def search():
    currentpage = request.url_rule
    session['rule']= str(currentpage)
    if request.method == 'POST':
        searchQuery = request.form.get("searchQuery")
        try:
            results = Student.query.filter(or_(Student.student_id == searchQuery,
                                                Student.surname.op('regexp')(r'\b{}\b'.format(searchQuery.title())),
                                                Student.othernames.op('regexp')(r'\b{}\b'.format(searchQuery.title())),
                                                Student.room_number.op('regexp')(r'\b{}\b'.format(searchQuery.title()))
                                                    )).all()
            return render_template('searchpage.html', results=results)
        except:
            error_message = "Problem Encountered Searching For Student!"
            return errorhandler(error_message)
    else:
            return render_template('searchpage.html')

# -------------------------------Events Page------------------------------
@app.route('/events', methods=['POST','GET'])
@login_required
def events():
    if request.method == 'POST':
        event_name = request.form['event_name'].title()
        type_of_event = request.form['event_type'].title()
        event_date = request.form['event_date']
        description = request.form['description'].title()

        eventpassed = Events(
            event_name=event_name,
            event_type =type_of_event,
            event_desc =description,
            event_date = event_date
        )
        activity = Activities(
        doer =session['user'],
        event ="Added a new event coming on " + eventpassed.event_date)
        try:
            db.session.add(eventpassed)
            db.session.add(activity)
            db.session.commit()
            return redirect(url_for("events"))
        except:
            error_message = "Error occured adding Event!"
            return errorhandler(error_message)
    else:
        PostedEvents = Events.query.order_by(desc(Events.event_date)).all()
        return render_template('events.html',PostedEvents=PostedEvents)

#============================================================Addstudents Page=============================================================
@app.route('/addstudent', methods=['POST', 'GET'])
@login_required
def addStudent():
    if request.method == "POST":
        surname = request.form['surname'].title()
        othernames = request.form['othernames'].title()
        student_id = request.form['student_id']
        gender = request.form['gender'].title()
        hall = current_user.hall
        level = request.form['level']
        room_number = request.form['room_number'].capitalize()
        contact = request.form['contact']
        course = request.form['course'].title()
        email = request.form['email'].lower()

        checkRoom = Student.query.filter(Student.room_number == room_number).count()
        if checkRoom <= 3:
            data = Student(
                surname=surname,
                othernames=othernames,
                student_id=student_id,
                gender=gender,
                hall=hall,
                level=level,
                room_number=room_number,
                contact=contact,
                course=course,
                email= email)

            activity = Activities(
            doer =session['user'],
            event ="Added a new student with ID: " + str(data.student_id))
        else:
            error_message= "This Room is Full!"
            return errorhandler(error_message),400
        try:
                db.session.add(data)
                db.session.add(activity)
                db.session.commit()
                return redirect(url_for("database"))
        except:
                error_message = "Student ID, Email And Phone Must Be Unique!"
                return errorhandler(error_message),400
    else:
        return render_template('addstudent.html')

#=============================================================Database Page==============================================================
@app.route('/database', methods=['POST','GET'])
@login_required
def database():
    currentpage = request.url_rule
    session['rule'] = str(currentpage)
    Students = Student.query.order_by(Student.surname).all()
    return render_template('database.html',Students=Students)

# -----------------------Update Students----------------------------
@app.route('/update/<int:id>', methods=['POST','GET'])
@login_required
def update(id):
    updateStudent = Student.query.get_or_404(id)
    activity = Activities(
        doer =session['user'],
        event ="Updated details of student with ID: " + str(updateStudent.student_id))

    if request.method == 'POST':
# UpdateHere just can't update student ID
        updateStudent.surname = request.form['surname'].title()
        updateStudent.lastname = request.form['othernames'].title()
        updateStudent.room_number = request.form['room_number'].capitalize()
        updateStudent.contact = request.form['contact']
        updateStudent.course = request.form['course'].title()
        updateStudent.email = request.form['email'].lower()

        try:
            db.session.add(activity)
            db.session.commit()
            return redirect(url_for("database"))
        except:
                error_statement = "Make Sure All Required Details Are Not Empty!"
                return errorhandler(error_statement),400
    else:
        return render_template('updateStudent.html', updateStudent=updateStudent)

# ----------------------Delete Student---------------------------
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    student_to_delete = Student.query.get_or_404(id)

    activity = Activities(
        doer = session['user'],
        event = "Deleted student with ID: " + str(student_to_delete.student_id))
    try:
        db.session.add(activity)
        db.session.delete(student_to_delete)
        db.session.commit()
        return redirect(url_for('database'))
    except:
        error_statement = "There Was a Problem Deleting This Student"
        return errorhandler(error_statement),400

#===========================================================Porterslodge Page============================================================
@app.route('/porterslodge', methods=['POST','GET'])
@login_required
def porterslodge():
    return render_template('porterslodge.html')

#================LogKey under Porterslodge=================
@app.route('/logkey', methods=['POST','GET'])
@login_required
def logkey():
    if request.method=="POST":
        room_number=request.form['room_number'].capitalize()
        studentid=request.form['studentid']
        checkStudent = Student.query.filter(Student.student_id==studentid).first()
        
        if (checkStudent and checkStudent.room_number==room_number):

            surname = checkStudent.surname
            othernames = checkStudent.othernames
            loggers_name= surname + " " + othernames

            alog = Keylog(
                room_number=room_number,
                loggers_name=loggers_name)
        else:
            error_message= "You must be a room member to log its key!"
            return errorhandler(error_message),400
        activity = Activities(
        doer =session['user'],
        event ="Logged key of Room: " + room_number)
        try:
            db.session.add(alog)
            db.session.add(activity)
            db.session.commit()
            return redirect(url_for("logkey"))
        except:
            error_message = "Problem Encountered While Logging Room Key!"
            return errorhandler(error_message)
    Logs = Keylog.query.order_by(Keylog.time_in).all()
    return render_template('logkey.html',Logs=Logs)

# ------------------Sign Out Keylog--------------------
@app.route('/signoutLogger/<int:id>', methods=['POST','GET'])
@login_required
def updateLoggers(id):
    updateLog = Keylog.query.get_or_404(id)
    activity = Activities(
        doer =session['user'],
        event ="Signed Out Key of Room: " + updateLog.room_number)
    checkSigned = updateLog.collectors_name

    if request.method == 'POST':
        collectorsid = request.form['collectors_id']
        checkCollector = Student.query.filter(Student.student_id==collectorsid).first()
        if (checkCollector and updateLog.room_number==checkCollector.room_number and not checkSigned):
                updateLog.collectors_name = checkCollector.surname + " " + checkCollector.othernames
                updateLog.time_out = datetime.now()
        
                try:
                    db.session.add(activity)
                    db.session.commit()
                    return redirect(url_for('logkey'))
                except:
                        error_statement = "Make Sure All Required Details Are Not Empty!"
                        return errorhandler(error_statement)
        else:
            error_statement = "Error: You must be a room member OR key already signed out!"
            return errorhandler(error_statement),400
    else:
        Logs = Keylog.query.order_by(Keylog.time_in).all()
        return render_template('signOutKeylog.html', Logs=Logs,updateLog=updateLog)

#==============Vistorsbook under Porterslodge================
@app.route('/visitorsbook', methods=['POST','GET'])
@login_required
def visitorsbook():
    if request.method=="POST":
        visitors_name=request.form['visitors_name'].title()
        id_type=request.form['id_type'].title()
        id_number=request.form['id_number']
        hostid=request.form['hostid'].title()
        room_number=request.form['room_number'].capitalize()
        visitors_contact=request.form['visitors_contact']
        checkHost=Student.query.filter(Student.student_id==hostid).first()
        if (checkHost and checkHost.room_number == room_number):
            Visits = Visitors(
                visitors_name=visitors_name,
                id_type=id_type,
                id_number=id_number,
                hostname=checkHost.surname+ " " + checkHost.othernames,
                hall=checkHost.hall,
                room_number=checkHost.room_number,
                contact=visitors_contact
            )
            activity = Activities(
            doer =session['user'],
            event ="Logged a visitor of Room: " + room_number)
            try:
                db.session.add(Visits)
                db.session.add(activity)
                db.session.commit()
            except:
                error_message = "Problem Encountered While Logging Visitor!"
                return errorhandler(error_message),400
        else:
            error_message="No Such Host Exist OR Wrong Room Number!"
            return errorhandler(error_message)
    Visits = Visitors.query.order_by(Visitors.time_in).all()
    return render_template('visitorsbook.html',Visits=Visits)

# ------------------Sign Out Visitors--------------------
@app.route('/signoutVisitor/<int:id>', methods=['POST','GET'])
@login_required
def updateVisitors(id):
    SignOutVisits = Visitors.query.get_or_404(id)
    activity = Activities(
        doer =session['user'],
        event ="Signed Out Visitor of Room: " + SignOutVisits.room_number)
    checkSigned = SignOutVisits.time_out

    if request.method == 'POST' and not checkSigned:
        SignOutVisits.time_out = datetime.now()

        try:
            db.session.add(activity)
            db.session.commit()
            return redirect(url_for('visitorsbook'))
        except:
                error_statement = "System Encountered Error Signing Visitor Out!"
                return errorhandler(error_statement)
    else:
        Visits = Visitors.query.order_by(Visitors.time_in).all()
        return render_template('signOutVisitor.html',Visits=Visits,SignOutVisits=SignOutVisits)

#===========================View Complaints====================
@app.route('/complaints', methods=['POST','GET'])
@login_required
def complaints():
    Issues = Complaints.query.order_by(desc(Complaints.date_submitted)).all()
    return render_template('complaints.html',Issues=Issues)

#==============================================================SystemLogs Page==============================================================
@app.route('/systemtickets', methods=['POST','GET'])
@login_required
def systemtickets():
    Activity = Activities.query.order_by(desc(Activities.date_of_event)).all()
    return render_template('systemtickets.html',Activity=Activity)


#=====================================================Compliants Submission Page===========================================================
@app.route('/complaintsSubmission', methods=['POST','GET'])
def complaintsSubmission():
    if request.method == "POST":
        room_number = request.form['room_number'].capitalize()
        hall = request.form['hall']
        student_id = request.form['student_id']
        issue_type = request.form['issue_type']
        other_specify = request.form['other_specify']
        description = request.form['description'].capitalize()

        check_Id = Student.query.filter_by(student_id=student_id).first()
        if check_Id:    
            if issue_type == "Other":
                issue_type = other_specify
        else:
            error_message= "You're not a Resident of the Hall. You can't submit a complaint"
            return errorhandler(error_message),400
        data = Complaints(
            room_number=room_number,
            std_fullname=check_Id.othernames + " " + check_Id.surname,
            student_id=student_id,
            hall=hall,
            issue_type=issue_type,
            description=description
        )
        try:
                db.session.add(data)
                db.session.commit()
                statement = "Complaint Submitted Successfully!"
                return successhandler(statement),200
        except:
                error_statement = "Complaint Submitted was Unsuccessful!"
                return errorhandler(error_statement)
    else:
        return render_template('complaintsSubmission.html')

#===========================================================Log Out===========================================================
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

#==============================================================Student Portal=============================================================
@app.route('/studentPortal', methods=['POST', 'GET'])
def studentPortal():
    return render_template('studentPortal.html')

#===============================================================Display CheckedIn Students===============================================================
@app.route('/checkedIn', methods=['POST','GET'])
@login_required
def checkedIn():
    students = CheckedIn.query.order_by(CheckedIn.room_number).all()
    return render_template('checkedIn.html',students=students)

#=============================================================About_us Page============================================================
@app.route('/about_us', methods=['POST','GET'])
def about_us():
    return render_template('about_us.html')

#=============================================================Contact_us Page===========================================================
@app.route('/contact_us', methods=['POST','GET'])
def contact_us():
    return render_template('contact_us.html')

#=======================================================================================================================================
if __name__ == "__main__":
    # app.logger.addHandler(logging.StreamHandler(sys.stdout))
    # app.logger.setLevel(logging.ERROR)
    app.run(debug=True)
