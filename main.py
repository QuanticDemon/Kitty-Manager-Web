from flask import * 
import uuid
import hashlib
import sqlite3
app = Flask(__name__)
app.secret_key = "ae6d651fa84a5ccc16a6574601db6dca/@*axmsao129n29330231j2091n39192s901292192012js9j102js019"
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
class Storage_Service:
    def __init__(self, storage:Storage):
        self.storage = storage

    def save_data_service(self,datausr_package):
        return self.storage.save_data(datausr_package)
    def consult_data_service(self, datausr_package):
        return self.storage.consult_data(datausr_package)
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
        password = hashPass.hexdigest()

        userData_package ={
            "userToken":loginUser,
            "password":password
        }

        sql3 = SQLite3("kitTest.db")
        sql3.start_tables()
        serviceStorage = Storage_Service(sql3)
        return serviceStorage.consult_data_service(userData_package)


#context_procesor
@app.context_processor
def inject_user_data():
    return {
        'username':session.get('username'),
        'mail':session.get('user_mail'),
        'is_logged_in':'user_id' in session
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
    userToken = request.form.get('loginUser')
    password = request.form.get('password')
    action = request.form.get('action')

    if request.method == "POST" and action == "login":
        
        verification = User().sing_in(userToken, password)

        if verification:
            
            session['user_id'] = verification['id']
            session['username'] = verification['username']
            session['user_mail'] = verification['mail']
            return redirect(url_for("home"))
        else:
            return render_template("sign-in.html", verification = verification)
    return render_template("sign-in.html")


@app.route('/my-profile', methods=["GET","POST"])
def user_profile():
    if 'user_id' not in session:
        return redirect(url_for("login"))

    return render_template('user-profile.html')

@app.route('/my-projects', methods=["GET","POST"])

def my_projects():
    return render_template("my-projects.html")


if __name__ == "__main__":
    app.run(debug=True)
