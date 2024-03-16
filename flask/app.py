import csv
from urllib import response
from flask import Flask, render_template,request,session,g,jsonify,send_from_directory
from flask_mail import Mail,Message
import mysql.connector

import cv2
import numpy as np
from PIL import Image,ImageTk
from datetime import datetime, timedelta,date

import time


import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'archanapv347@gmail.com'
app.config['MAIL_PASSWORD'] = 'kptr dzjj sybx tuye'

mail = Mail(app)


app.secret_key = 'pv'

# ======================= DB Functions ==============================

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'face',
}


def insert_record(query, data):
    cnx = mysql.connector.connect(**config)
    crsr = cnx.cursor()
    crsr.execute(query, data)

    cnx.commit()
    crsr.close()
    cnx.close()


def update_record(query, data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(query, data)
    cnx.commit()
    cursor.close()
    cnx.close()
    return True


def select_records(query):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    cnx.close()
    return rows


def count_records(query):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()
    cnx.close()
    return len(rows)

# ======================= Database Functions ==============================


# ======================= Common Functions ===============================

@app.route('/')
def index():
    return render_template('index.html')


# ----------- Student Register start -----------

@app.route('/register')
def register():
    return render_template('signup.html')


@app.route('/submitregister', methods=['POST'])
def submitregister():
    data = []
    fname = request.form['fname']
    data.append(fname)
    email = request.form['email']
    data.append(email)
    rollno = request.form['rollno']
    data.append(rollno)
    dob = request.form['dob']
    data.append(dob)
    course = request.form['course']
    data.append(course)
    semester = request.form['semester']
    data.append(semester)
    gender = request.form['gender']
    data.append(gender)
    phone = request.form['phone']
    data.append(phone)
    password = request.form['password']
    data.append(password)
    cpass = request.form['cpass']
    data.append(cpass)

    sql0 = "SELECT * from registration where email='"+email+"' "
    data0 = select_records(sql0)
    if len(data0) > 0:
        return ("Account already exists")

    else:

        if (password == cpass):

            sql = "INSERT INTO registration(fullname,email,rollno,dob,course,semester,gender,phone) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (fname, email, rollno, dob, course, semester, gender, phone)
            insert_record(sql, data)

            sql1 = "INSERT INTO login(email,password,usertype,userstatus) VALUES(%s,%s,%s,%s)"
            data1 = (email, password, 0, 0)
            insert_record(sql1, data1)
            sql4="select max(id) from registration"
            data4=select_records(sql4)

            stdid=str(data4[0][0])
            print("files saving started")
            face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

            def face_croped(img):
                # conver gary sacle
                gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray,1.3,5)
                #Scaling factor 1.3
                # Minimum naber 5
                for (x,y,w,h) in faces:
                    face_croped=img[y:y+h,x:x+w]
                    return face_croped
            cap=cv2.VideoCapture(0)
            img_id=0
            while True:
                ret,my_frame=cap.read()
                if face_croped(my_frame) is not None:
                    img_id+=1
                    face=cv2.resize(face_croped(my_frame),(200,200))
                    face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                    file_path="dataset/stdudent."+stdid+"."+str(img_id)+".jpg"
                    cv2.imwrite(file_path,face)
                    cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)       
                    cv2.imshow("Capture Images",face)

                if cv2.waitKey(1)==13 or int(img_id)==100:
                    break
            cap.release()
            cv2.destroyAllWindows()



            return '''
							<script>
							alert('User Registered Successful!');
							window.location.href = '/';
							</script>
		
		
								'''

        else:
            return jsonify("Password doesnot match")


# ======================Student Register end =====================

# ---------------------------Login---------------------------------


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/submitlogin', methods=["POST", "GET"])
def submitlogin():
    data = []
    email = request.form['email']
    data.append(email)
    password = request.form['password']
    data.append(password)

    sql2 = "SELECT * from login where email='" + \
        email + "' and password='" + password + "' "
    data2 = select_records(sql2)

    # print(type(data2[0][2]))

    if len(data2) > 0:
        usertype = data2[0][2]
        userstatus = data2[0][3]
        if usertype == 0:
            if userstatus == 1:
                session['email'] = email
                sql5 = "SELECT * from registration where email='"+email+"'"
                data5 = select_records(sql5)
                session['user'] = data5[0]

                return '''
							<script>
							alert('User Login Successful!');
							window.location.href = '/user/';
							</script>
			
            
                                
					'''
            
            else:
                return jsonify("unsuccessful login")
            
            

        elif usertype == 1:
            session['email'] = email
            sql3 = "SELECT * from login where email='"+email+"'"
            data3 = select_records(sql3)
            session['admin'] = data3[0]

            return '''
                    <script>
                    alert('Admin Login Successful!');
                    window.location.href = '/admin/';
							</script>
            '''

        else:
            return jsonify("unsuccessful login")
    else:
        return jsonify("invalid details")


# ===========================Login Ends==========================


# `````````````````````````` Admin functions ---------------------

@app.route('/admin/')
def admin():
    return render_template('admin/adminindex.html')

@app.route('/admin/base')
def adminbase():
    return render_template('admin/base.html')

@app.route('/active')
def active():
    sql4 = "SELECT fullname, rollno, email, dob, gender, phone, course, semester FROM `registration` WHERE email IN (SELECT email FROM login WHERE userstatus=1 AND usertype=0)"
    data4 = select_records(sql4)
    return render_template('admin/activestudents.html', sdata1=data4)


@app.route('/pending')
def pending():
    sql7 = "SELECT fullname, rollno, email, dob, gender, phone, course, semester, id FROM `registration` WHERE email IN (SELECT email FROM login WHERE userstatus=0 AND usertype=0)"
    data7 = select_records(sql7)

    data_dir = "dataset"
    path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]
    faces = []
    ids = []
    for image in path:
        img = Image.open(image).convert('L')  # convert in gray scale
        imageNp = np.array(img, 'uint8')
        id = int(os.path.split(image)[1].split('.')[1])
        faces.append(imageNp)
        ids.append(id)

    ids = np.array(ids)
    print(ids)
    print("hello")

    # Train Classifier
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.train(faces, ids)
    clf.write("clf.xml")

    return render_template('admin/pendingstudents.html', sdata2=data7)


@app.route('/get_image/<student_id>')
def get_image(student_id):
    image = f'stdudent.{student_id}.10.jpg'
    return send_from_directory('dataset', image)


@app.route('/suspended')
def suspended():
    sql8 = "SELECT fullname, rollno, email, dob, gender, phone, course, semester FROM `registration` WHERE email IN (SELECT email FROM login WHERE userstatus=-1 AND usertype=0)"
    data8 = select_records(sql8)
    session['sdata3'] = data8
    return render_template('admin/suspendedstudents.html', sdata3=data8)


@app.route('/rejected')
def rejected():
    sql9 = "SELECT fullname, rollno, email, dob, gender, phone, course, semester FROM `registration` WHERE email IN (SELECT email FROM login WHERE userstatus=-2 AND usertype=0)"
    data9 = select_records(sql9)
    session['sdata4'] = data9
    return render_template('admin/rejectedstudents.html', sdata4=data9)


@app.route('/approvestudents', methods=['GET'])
def approvestudents():
    id = request.args.get('id')
    sql11 = "UPDATE login SET userstatus=1 WHERE email=%s"
    data = (id,)  # Prepare data as a tuple
    data11 = update_record(sql11, data)  # Provide both SQL query and data
    if data11:
        student_email = id  
        msg = Message("Account Approved", sender="archanapv347@gmail.com", recipients=[student_email])
        msg.body = "Your account has been approved. You can now login to your account."
        mail.send(msg)
        return '''
                <script>
                alert('Approved a Student ');
                window.location.href = '/active';
                        </script>
        
            '''

    else:
        return '''
                <script>
                alert('Error Occured');
                window.location.href = '/pending';
                        </script>
        
                '''
    

@app.route('/rejectstudents', methods=['GET'])
def rejectstudents():
    id = request.args.get('id')
    sql16 = "UPDATE login SET userstatus=-2 WHERE email=%s"
    data = (id,)  
    data16 = update_record(sql16, data) 
    if data16:
        student_email = id  
        msg = Message("Account Rejected", sender="archanapv347@gmail.com", recipients=[student_email])
        msg.body = "Your account has been rejected."
        mail.send(msg)
        return '''
                <script>
                alert('Rejected a Student ');
                window.location.href = '/rejected';
                        </script>
        
            '''

    else:
        return '''
                <script>
                alert('Error Occured');
                window.location.href = '/pending';
                        </script>
        
                '''
    
@app.route('/suspendstudents', methods=['GET'])
def suspendstudents():
    id = request.args.get('id')
    sql17 = "UPDATE login SET userstatus=-1 WHERE email=%s"
    data = (id,)  
    data17 = update_record(sql17, data) 
    if data17:
        student_email = id  
        msg = Message("Account Suspended", sender="archanapv347@gmail.com", recipients=[student_email])
        msg.body = "Your account has been suspended. You can't login to your account until further notice."
        mail.send(msg)
        return '''
                <script>
                alert('Suspended a Student ');
                window.location.href = '/suspended';
                        </script>
        
            '''

    else:
        return '''
                <script>
                alert('Error Occured');
                window.location.href = '/active';
                        </script>
        
                '''

@app.route('/createsession', methods=['POST'])
def createsession():
    data= []
    topic = request.form['topic']
    data.append(topic)
    date = request.form['date']
    data.append(date)
    stime = request.form['stime']
    data.append(stime)
    etime = request.form['etime']
    data.append(etime)
    sql12="INSERT INTO session(topic,date,stime,etime)VALUES(%s,%s,%s,%s)"
    data=(topic,date,stime,etime)
    insert_record(sql12,data)
    

    return '''
							<script>
							alert('Session created successfully!');
							window.location.href = '/admin/';
							</script>
		
		
								'''

@app.route('/admin/activesession')
def adminviewsession():
    today = datetime.now().strftime('%Y-%m-%d')
    sql13 = "SELECT * FROM session WHERE stime <= NOW() AND etime >= NOW() AND date = '"+today+"' "
    data13 = select_records(sql13)
    return render_template('admin/activesession.html', sdata13=data13)


@app.route('/admin/upcomingsession')
def adminupcomingsession():
    today = date.today().strftime('%Y-%m-%d')  
    sql14= "SELECT * FROM session WHERE (stime > NOW() AND etime > NOW() AND date = '2024-03-09') or date>'2024-03-09' "
    print(sql14)
    data14 = select_records(sql14)
    return render_template('admin/upcomingsession.html', sdata14=data14)


@app.route('/admin/completedsession')
def admincompletedsession():
    today = datetime.now().strftime('%Y-%m-%d')
    sql15 = "SELECT * FROM session WHERE etime < NOW() AND date <= '" + today + "'"
    data15 = select_records(sql15)
    return render_template('admin/completedsession.html', sdata15=data15)

@app.route('/admin/liststudents')
def adminliststudents():
    today = datetime.now().strftime('%Y-%m-%d')
    sql15 = "SELECT * FROM session WHERE etime < NOW() AND date <= '" + today + "'"
    data15 = select_records(sql15)
    return render_template('admin/studentlist.html', sdata15=data15)

@app.route('/logout')
def logout():
    session.clear()
    return '''
                <script>
                alert('You have been logged out');
                window.location.href = '/';
                        </script>
        
                '''


# ==========================================================================


# ------------------------- user functions ------------------------

@app.route('/user/')
def user():
    return render_template('user/userindex.html')


@app.route('/profile')
def profile():
    email = session['email']
    sql6 = "SELECT * from registration where email='"+email+"'"
    data6 = select_records(sql6)
    session['profile'] = data6
    return render_template('user/profile.html', profile=session['profile'])


@app.route('/buttons')
def buttons():
    return render_template('user/buttons.html')


@app.route('/cards')
def cards():
    return render_template('user/cards.html')


@app.route("/detectface/")
def detectfaceindex():
	user=session['user']


	faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	clf=cv2.face.LBPHFaceRecognizer_create()
	clf.read("clf.xml")

	start_time = time.time()

	videoCap=cv2.VideoCapture(0)

	while True:
		ret,img=videoCap.read()
		data=recognize(img,clf,faceCascade)
		cv2.imshow("Face Detector",data[0])
		print(data[1])

		if cv2.waitKey(1) == 27:

			videoCap.release()
			cv2.destroyAllWindows()

			return '''
						<script>
						alert('Exited from attendance mode');
						window.location.href = '/admin/';
						</script>
						'''


# =============================================================
        



def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
	gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	featuers=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

	user=session['user']
	userid=user[0]

	flag=False


	coord=[]
	
	for (x,y,w,h) in featuers:
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)#croping the face
		id,predict=clf.predict(gray_image[y:y+h,x:x+w])

		confidence=int((100*(1-predict/300)))

		

		# print(id==userid)

		if confidence > 80:
			if userid==id:
				flag=True
		

		coord=[x,y,w,y]
	
	return flag

def recognize(img,clf,faceCascade):
	flag=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
	return (img,flag)


# ======================= Common Functions ends ===============================
if __name__ == '__main__':
    app.run(debug=True)
