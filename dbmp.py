#TODO: 1. connect mysql db with the flask app:- Done
#2. ADD sign up functionality for students and teachers :- Done
#3. Add redirect to data and datas.html in profile and display the data from sql. :- Done
#4. collect data from subs.html and add that to mysql substable :- Done
#5. Add redirection to services page:- Done
#6. Add event registration form in the event page.:- Done
#7. collect data from event registration form and display it in profile page
#8. Understand how to collect the fetched data from sql in variable and print it on webpage.:- Done
#9. Work on coach profile page.:-  Done
#10. Add message for incorrect details
## The sql queries is returning an int object which isn't iterable.:- Done
## Also check the sql queries for syntax and proper working. :- Done





from flask import Flask,render_template,request,redirect, url_for, session
from flask_mysqldb import MySQL
import yaml
from datetime import datetime


app = Flask(__name__)
db=yaml.load(open('db.yaml'))


app.config['MYSQL_HOST']=db['mysql_host']
app.config['MYSQL_USER']=db['mysql_user']
app.config['MYSQL_PASSWORD']=db['mysql_password']
app.config['MYSQL_DB']=db['mysql_db']
app.secret_key= 'hello'

mysql=MySQL(app)


@app.route('/')
def home():
     return render_template('home.html')



@app.route('/contact')
def contact():
     return render_template('contact.html')

@app.route('/data')
def data():
     # session["Coach_Id"]=coid
     #      session["Phone_No"]=cpho
     if "Coach_Id" in session:
          coid=session["Coach_Id"]
          cphone=session["Phone_No"]
          cur2=mysql.connection.cursor()
          cdetails=cur2.execute("SELECT coach.coachID,coach.coachName, coach.coachph, eventr.eventName,eventr.studentID FROM coach INNER JOIN eventr ON coach.coachID = eventr.coachID WHERE coach.coachID=%s;",(coid,))
          if cdetails>0:
               CoachDetails=cur2.fetchall()
               return render_template('data.html', CD=CoachDetails)
          else:
               pass
               ## Add message about "No such event has been planned"
          cur2.close()
     return render_template('profile.html')

@app.route('/datas')
def datas():
     if "Student_Id" in session:
          sid=session["Student_Id"]
          spoid=session["Sports_Id"]
          cur=mysql.connection.cursor()
          sdetails=cur.execute("SELECT student.*,subscription.noofmonth,subscription.startdate FROM student INNER JOIN subscription ON student.sportsID=subscription.sportsID where student.studentID=%s GROUP BY student.sportsID",(sid,))
          if sdetails>0:
               studentDetails=cur.fetchall()
               return render_template('datas.html', studentDetails=studentDetails)
          else:
               render_template('regs.html')
               ##Add message "No such Record found/exist"
          # cur1=mysql.connection.cursor()
          # subsdetail=cur.execute("SELECT subscription.* FROM subscription WHERE studentID=%s and sportsID=%s;",(sid,spoid))
          # if subsdetail>0:
          #      subscriptionD=cur.fetchall()
          #      return render_template('example.html', subD=subscriptionD)
          # cur2=mysql.connection.cursor()
          # cdetails=cur2.execute("SELECT coach.coachName, coach.coachph, eventr.eventName FROM coach INNER JOIN eventr ON coach.coachID = eventr.coachID WHERE coach.sportsID=%s;",(spoid,))
          # if cdetails>0:
          #      coachD=cur.fetchall()
          #      for M in coachD:
          #           for i in M:
          #                print(i)
               #return render_template('example.html', CD=coachD)
          # for x in bx:
          #      print(x)
          # print("============")
          # for y in subsdetail:
          #      print(y)
          # print("============")
          # for z in cdetails:
          #      print(z)
          cur.close()
          cur1.close()
          #cur2.close()
     return render_template('profile.html')


@app.route('/services')
def services():
     return render_template('services.html')



@app.route('/reg', methods = ['GET','POST'])
def reg():
     if request.method=='POST':
          cname=request.form['cusername']
          cid=request.form['cid']
          cpho=request.form['cphno']
          cspo=request.form['csport']
          sid=request.form['spoid']
          cursor=mysql.connection.cursor()
          cursor.execute("INSERT INTO coach VALUES(%s, %s, %s, %s, %s);",(cid,cname,cpho,cspo,sid))
          mysql.connection.commit()
          cursor.close()
          return redirect(url_for('profile'))
     return render_template('tregistration.html')


@app.route('/regs', methods=['GET','POST'])
def regs():
     if request.method == 'POST':
          sname=request.form['studentName']
          stid=request.form['student_id']
          ph=request.form['phone']
          spid=request.form['sportID']
          address=request.form['addr']
          
          cur=mysql.connection.cursor()
          cur.execute("INSERT INTO student VALUES(%s , %s, %s, %s, %s);",(stid, sname, address, ph, spid))
          mysql.connection.commit()
          # cur.execute("SELECT phone FROM student WHERE studentName=%s;",[ss]) #use a list to send items in select query
          # sd=cur.fetchall()
          # for x in sd:
          #      for i in x:
          #           print(int(i))
          cur.close()
          return redirect(url_for('profile'))
     return render_template('sregistration.html')

@app.route('/subs', methods=['GET','POST'])
def subs():
     if request.method=='POST':
          subsid=request.form['subssid']
          stuid=request.form['subsstid']
          nom=request.form['subsMonth']
          date=request.form['sdate']
          datex=datetime.strptime(date,'%Y-%m-%d')
          cur=mysql.connection.cursor()
          # to pass date as an sql query input.....
          cur.execute("INSERT INTO subscription VALUES (%s, %s, %s, %s);",(subsid,stuid,nom,datex))
          mysql.connection.commit()
          cur.close()
          return redirect(url_for('profile'))


     return render_template('subs.html')



@app.route('/events',methods=['GET','POST'])
def events():
     return render_template('event.html')


@app.route('/eventr',methods=['GET','POST'])
def eventr():
     if request.method=='POST':
          eid=request.form['evid']
          ename=request.form['ename']
          sid=request.form['stid']
          spid=request.form['spid']
          coid=request.form['cid']
          cursor=mysql.connection.cursor()
          cursor.execute("INSERT INTO eventr VALUES(%s, %s, %s, %s, %s);",(eid,ename,spid,coid,sid))
          mysql.connection.commit()
          cursor.close()
          return redirect(url_for('profile'))
     return render_template('eventform.html')


@app.route('/profile',methods=['GET','POST'])
def profile():
     if request.method=='POST' and 'sid' in request.form and 'spid' in request.form:
          sid=request.form['sid']
          spid=request.form['spid']
          session["Student_Id"]=sid
          session["Sports_Id"]=spid
          return redirect(url_for('datas'))
     elif request.method =='POST' and 'cid' in request.form and 'cph' in request.form:

          coid=request.form['cid']
          cpho=request.form['cph']
          session["Coach_Id"]=coid
          session["Phone_No"]=cpho

          return redirect(url_for('data'))

     return render_template('profile.html')


@app.route('/subscription')
def subscription():
     return render_template('subscription.html')


if __name__ == '__main__':
     app.run(debug=True)

