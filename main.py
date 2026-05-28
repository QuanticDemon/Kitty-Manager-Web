from flask import * 
import uuid
import hashlib
import sqlite3
app = Flask(__name__)
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


class Storage_Service:
    def __init__(self, storage:Storage):
        self.storage = storage

    def save_data_service(self,datausr_package):
        return self.storage.save_data(datausr_package)

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



#Flask
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    username = request.args.get("username")
    return render_template("home.html", username = username)
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
if __name__ == "__main__":
    app.run(debug=True)
