from flask import * 
import uuid
import hashlib
import sqlite3
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "ae6dasasdsddd6514fa8d4a5ccc16a6574601db6dca/@*axmsao129n29330231j2091n3s9e313fs92s901292192012js9j102js019"
#DB 

class Storage:
    def __init__(self, datastorage_file):
        self.datastorage_file = datastorage_file
   
    def load_data(self):
        pass
    def save_data(self, datausr_package):
        pass 

    def update_data(self, datausr_package):
        pass
    def consult_data(self, datausr_package):
        pass
    
    def update_profile_pic(self,image):
        pass
class SQLite3(Storage):
    def conexion(self):
        return sqlite3.connect(self.datastorage_file)

    def start_tables(self):
        conn = self.conexion()
        cursor = conn.cursor()
        cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS users(
                    id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    mail TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                    )
                '''

        )

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS profile_pic(
                id_image TEXT PRIMARY KEY,
                image_profile TEXT NOT NULL,
                id_user TEXT,
                FOREIGN KEY (id_user) REFERENCES users(id)


             )   
            '''
        )
        conn.commit()
        cursor.close()
        conn.close()
    def save_data(self, datausr_package):
        conn = self.conexion()
        cursor = conn.cursor()
        cursor.execute(
                '''
                INSERT INTO users(id, username, mail, password) VALUES (?,?,?,?)
                ''', (
                    datausr_package["id"],
                    datausr_package["name"],
                    datausr_package["mail"],
                    datausr_package["password"]
                    )

        )

        conn.commit()
        cursor.close()
        conn.close()
    def consult_data(self, datausr_package):

        conn = self.conexion()
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT * FROM users WHERE (username = ? OR mail = ?) AND password = ?
            ''',(
                datausr_package["userToken"],
                datausr_package["userToken"],
                datausr_package["password"]
            )
        )

        verificacion = cursor.fetchone()

        

        conn.commit()
        cursor.close()
        conn.close()

        if verificacion:


            return{
                "id":verificacion[0],
                "username": verificacion[1],
                "mail": verificacion[2],
                "password":verificacion[3]
            }
        else:
            return False
    def update_data(self, datausr_package):
        conn = self.conexion()
        cursor = conn.cursor()
        
        fields_tochange = []
        values = []

        if datausr_package['username']:
            fields_tochange.append("username = ?")
            values.append(datausr_package['username'])
        
        if datausr_package['password']:
            fields_tochange.append("password = ?")
            values.append(datausr_package['password'])
        
        if datausr_package['user_mail']:
            fields_tochange.append("mail = ?")
            values.append(datausr_package['user_mail'])

        
        query = f"""
        UPDATE users
        SET {', '.join(fields_tochange)}
        WHERE id = ?
        """

        values.append(session.get('user_id'))
        cursor.execute(query, values)



           

        conn.commit()
        cursor.close()
        conn.close()
    def update_profile_pic(self, image):
        conn = self.conexion()
        cursor = conn.cursor()

        image_id=str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO profile_pic(id_image, image_profile ,id_user) VALUES (?,?,?)
            """,(
                image_id,
                image,
                session['user_id']
            )
        )

       
            
            
        image_upload = cursor.fetchone()



        conn.commit()
        cursor.close()
        conn.close()
        return {
        "id_image": image_id,
        "image_profile": image,
        "id_user": session['user_id']
    }
class Storage_Service:
    def __init__(self, storage:Storage):
        self.storage = storage

    def save_data_service(self,datausr_package):
        return self.storage.save_data(datausr_package)
    def consult_data_service(self, datausr_package):
        return self.storage.consult_data(datausr_package)
    def update_data_service(self, datausr_package):
        return self.storage.update_data(datausr_package)
    def update_profile_pic_service(self, image):
        return self.storage.update_profile_pic(image)
#Users
class User:
    def create_account(self, name, mail, password):

        hashPass = hashlib.sha512(password.encode())
        password = hashPass.hexdigest()

        user_package={
                "id": str(uuid.uuid4()),
                "name":name,
                "mail":mail,
                "password": password
                }
         
        sql3 = SQLite3("kitTest.db")
        sql3.start_tables()

        serviceStorage = Storage_Service(sql3)
        serviceStorage.save_data_service(user_package)

    def sing_in(self, loginUser, password):
        hashPass = hashlib.sha512(password.encode())
        hashedPass = hashPass.hexdigest()

        userData_package ={
            "userToken":loginUser,
            "password":hashedPass
        }
       

        sql3 = SQLite3("kitTest.db")
        sql3.start_tables()
        serviceStorage = Storage_Service(sql3)
        return serviceStorage.consult_data_service(userData_package)
    def update(self, changes):
        passwordHashing = hashlib.sha512(changes['password'].encode())
        passwordUpdate = passwordHashing.hexdigest()

        user_package_tochange ={
            "username":changes['username'],
            "user_mail":changes['mail'],
            "password":passwordUpdate

        }

        sqlite3 = SQLite3("kitTest.db")
        sqlite3.start_tables()
        serviceStorage = Storage_Service(sqlite3)
        serviceStorage.update_data_service(user_package_tochange)
    @staticmethod
    def messenger_images(image):
        sqlite3 = SQLite3("kitTest.db")
        sqlite3.start_tables()
        storageService = Storage_Service(sqlite3)
        return storageService.update_profile_pic_service(image)

#context_procesor
@app.context_processor
def inject_user_data():
    userpic = None

    if session.get('user_id'):
            conn = SQLite3("kitTest.db").conexion()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT image_profile FROM profile_pic WHERE id_user = ? ORDER BY id_image DESC LIMIT 1",
                (session['user_id'],)
            )

            row = cursor.fetchone()

            if row:
                userpic = url_for('uploads_filename', filename=row[0])

            cursor.close()
            conn.close()


    return {
        'username':session.get('username'),
        'mail':session.get('user_mail'),
        'is_logged_in':'user_id' in session,
        'userpic':userpic

    }

#Flask



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for("login"))
    return render_template("home.html")
@app.route('/create-account', methods=["GET", "POST"])
def register():
    session.clear()
    username = request.form.get("username")
    mail = request.form.get("mail")
    password = request.form.get("password")
    
    action = request.form.get("action")
    if request.method == "POST":
        if action == "Confirm":
            createUser = User().create_account(username, mail, password)
            return redirect(url_for("home", username=username))
    
    return render_template("create-account.html")

@app.route('/sign-in', methods=["GET", "POST"])
def login():
    session.clear()
    userToken = request.form.get('loginUser')
    password = request.form.get('password')
    action = request.form.get('action')

    if request.method == "POST" and action == "login":
        
        verification = User().sing_in(userToken, password)

        if verification:
            
            session['user_id'] = verification['id']
            session['username'] = verification['username']
            session['user_mail'] = verification['mail']
            session['password'] = verification['password']
           

    
            return redirect(url_for("home"))
        else:
            return render_template("sign-in.html", verification = verification)
    return render_template("sign-in.html")


@app.route('/my-profile', methods=["GET","POST"])
def user_profile():

    print("METHOD", request.method)
    print("FILES:", request.files)
    if 'user_id' not in session:
        return redirect(url_for("login"))

    username = request.form.get("username")
    mail = request.form.get("mail")
    password = request.form.get("password")
    action = request.form.get("action")
    

    
    if request.method == "POST" and action == "update":
        file = request.files["changeImage"]
        if file and file.filename:
            valid_extension = ['png', 'jpg', 'jpeg', 'webp']
            extension = file.filename.rsplit('.', 1)[1].lower()
            print(request.files)
            print(request.files.keys())
            if extension in valid_extension:
                filename = f"{str(uuid.uuid4())}.{extension}"
                print(os.getcwd())
                print(os.path.abspath("uploads"))
                print(os.path.exists("uploads"))
                file.save(f"uploads/{filename}")
                updateImg = User().messenger_images(filename)


                

            
        changes = {
            "username": username if username else session.get("username"),
            "mail": mail if mail else session.get("user_mail"),
            "password": password if password else session.get("password")

        }
    
        update_user = User()
        update_user.update(changes)
        session['username'] = changes['username']
        session['user_mail'] = changes["mail"]
        session['password'] = changes['password']
       
    return render_template('user-profile.html')
@app.route('/uploads/<filename>')
def uploads_filename(filename):
    return send_from_directory('uploads', filename)

@app.route('/my-projects', methods=["GET","POST"])

def my_projects():
    return render_template("my-projects.html")

@app.route('/productivity-tools', methods=["GET","POST"])

def productivity_tools():
    return render_template("productivity.html")

if __name__ == "__main__":
    
    app.run(debug=True)

