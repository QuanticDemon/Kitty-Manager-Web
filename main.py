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
    def add_project(self, datapkg):
        pass
    def add_file(self, datapkg):
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
        cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS projects(
                    id_project TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    password TEXT,
                    id_user TEXT,
                    FOREIGN KEY (id_user) REFERENCES users(id)
                    )
                '''
                )

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS files(
                id_file INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                project_id TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id_project)

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

        if datausr_package['username'] and datausr_package['username'].strip():
            fields_tochange.append("username = ?")
            values.append(datausr_package['username'].strip())
        
        if datausr_package['password'] and datausr_package['password'].strip():
            fields_tochange.append("password = ?") 
            values.append(datausr_package['password'].strip())
        
        if datausr_package['user_mail'] and datausr_package['user_mail'].strip():
            fields_tochange.append("mail = ?")
            values.append(datausr_package['user_mail'].strip())

        if not fields_tochange:
            conn.close()
            return

        query = f"""
        UPDATE users
        SET {', '.join(fields_tochange)}
        WHERE id = ?
        """

        user_id = session.get('user_id')
        if not user_id:
            conn.close()
            



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

    def add_project(self, datapkg):
       
        conn = self.conexion()
        cursor = conn.cursor()
        project_id = str(uuid.uuid4())
        os.makedirs(
                f"projects/{project_id}",
                exist_ok=True
                )
        cursor.execute(
            """
            INSERT INTO projects(id_project, name, password,id_user) VALUES (?,?,?,?)
            """, (
                project_id,
                datapkg["project_name"],
                datapkg["password_project"],
                session.get('user_id')
                )
        )

        conn.commit()
        cursor.close()
        conn.close()
    def add_file(self, datapkg):
        conn = self.conexion()
        cursor = conn.cursor()
        
        cursor.execute(
            """
            INSERT INTO files (name, type, project_id) VALUES (?,?,?)
            """,(
                datapkg['name'],
                datapkg['type'],
                datapkg['project_id']

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
    def consult_data_service(self, datausr_package):
        return self.storage.consult_data(datausr_package)
    def update_data_service(self, datausr_package):
        return self.storage.update_data(datausr_package)
    def update_profile_pic_service(self, image):
        return self.storage.update_profile_pic(image)
    def add_project_service(self, datapkg):
        return self.storage.add_project(datapkg)
    def add_file_service(self,datapkg):
        return self.storage.add_file(datapkg)

#files
class Files:
    def __init__(self, filename, extension, project_id):
        self.filename = filename
        self.extension = extension
        self.project_id = project_id

    def create_file(self):
        data_package={
            "name":self.filename,
            "type":self.extension,
            "project_id":self.project_id
        }

        sql3 = SQLite3("kitTest.db")
        sql3.start_tables()
        storage_service = Storage_Service(sql3)
        storage_service.add_file_service(data_package)

    





#projects
class Project:
    def create_project(self, name, password):
        print("Esto funciona")
        if password:

            hashing = hashlib.sha512(password.encode())
            passHashed = hashing.hexdigest()
            
        else:
            passHashed = None
        
        datapkg_project ={
                    "project_name":name,
                    "password_project":passHashed
                    }
        sql3 = SQLite3("kitTest.db")
        sql3.start_tables()
        serviceStorage=Storage_Service(sql3)
        serviceStorage.add_project_service(datapkg_project)
        print("Se han enviado los datos")
    


#Users

class User:
    def create_account(self, name, mail, password):

        name = name.strip()
        mail = mail.strip()
        password=password.strip()


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
        loginUser = loginUser.strip()
        password = password.strip()

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
        
        user_package_tochange ={
            "username":None,
            "user_mail":None,
            "password":None

        }
        if changes.get('password'):

            passwordHashing = hashlib.sha512(changes['password'].encode())
            user_package_tochange["password"]= passwordHashing.hexdigest()
        if changes.get('username'):
            user_package_tochange['username'] = changes['username']
        if changes.get('user_mail'):
            user_package_tochange['user_mail'] = changes['user_mail']
        

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
    projects = []
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


    if session.get('user_id'):
        conn= SQLite3("kitTest.db").conexion()

        cursor=conn.cursor()
        cursor.execute(
            "SELECT id_project,name, password FROM projects WHERE id_user = ? ORDER BY id_project DESC",(session['user_id'],)
        )

        rows= cursor.fetchall()
        projects = [{ "id":r[0] ,"name":r[1], "has_password":bool(r[2])} for r in rows]
        cursor.close()
        conn.close()

    return {
        'username':session.get('username'),
        'mail':session.get('user_mail'),
        'is_logged_in':'user_id' in session,
        'userpic':userpic,
        'projects':projects

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
                



        changes = {}

        if username:changes['username'] = username
        if mail: changes['user_mail'] = mail

        if password:
            hashPass = hashlib.sha512(password.encode())
            changes['password'] = hashPass.hexdigest()
        else:
            changes['password'] = None
            
        

        
    
        update_user = User()
        update_user.update(changes)

        if 'username' in changes: session['username'] = changes['username']
        if 'user_mail' in changes: session['user_mail'] = changes['user_mail']
        if 'password' in changes: session['password'] = changes['password']
       
    return render_template('user-profile.html')
@app.route('/uploads/<filename>')
def uploads_filename(filename):
    return send_from_directory('uploads', filename)

@app.route('/projects/<project_id>')
def projects(project_id):
    conn = SQLite3("kitTest.db").conexion()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, password FROM projects WHERE id_project = ?
        """,(
            project_id,
        )
    )
    project = cursor.fetchone()
    cursor.execute(
        """
        SELECT * FROM files WHERE project_id=?
        """,(
            project_id,
        )
    )
   
    files = cursor.fetchall()
    cursor.close()
    conn.close()

    if not project:
        return "Proyecto no existe", 404
    return render_template('project.html', project=project, files=files, project_id=project_id)

@app.route('/my-projects', methods=["GET","POST"])

def my_projects():
    if request.method == "POST":
        if request.is_json:
            data = request.get_json()
            name = data['name']
            password = data['pass']
            create_project=Project()
            create_project.create_project(name, password)
            return jsonify({"success":True})

        else:
            project_name = request.form.get("name-project")
            password_project = request.form.get("pass_project")
            create_projecto=Project()
            create_projecto.create_project(project_name, password_project)

            return redirect(url_for('my_projects'))
        

    return render_template("my-projects.html")

@app.route('/productivity-tools', methods=["GET","POST"])

def productivity_tools():
    return render_template("productivity.html")


@app.route('/projects/<project_id>/delete', methods=["DELETE"])
def deleter_projects(project_id):
    conn = SQLite3("kitTest.db").conexion()
    cursor = conn.cursor()
    user_id = session.get('user_id')

    cursor.execute(
        """
        DELETE FROM projects WHERE id_project = ? AND id_user = ?
        """,(
            project_id,
            user_id
        )
    )
    
    conn.commit()
    cursor.close()
    conn.close()

    return {"success": True}

@app.route('/projects/<project_id>/private/delete', methods=["GET", "POST"])
def deleter_private_project(project_id):
    conn = SQLite3("kitTest.db").conexion()
    cursor = conn.cursor()
    
    pass_priv_data = request.get_json()
    pass_privHash = hashlib.sha512(pass_priv_data["password"].encode())
    pass_priv = pass_privHash.hexdigest()


    cursor.execute(
        """
        SELECT password FROM projects WHERE id_project = ?
        """,(
            project_id,
        )
    )
    row = cursor.fetchone()
    if pass_priv != row[0]:
        cursor.close()
        conn.close()
    
        return  {"success":False}, 404
    
    cursor.close()
    conn.close()
    return {"success":True}, 200

@app.route('/projects/<project_id>/access', methods=["GET", "POST"])
def access_private(project_id):
    conn = SQLite3("kitTest.db").conexion()
    cursor = conn.cursor()
    id_user = session.get('user_id')
    get_pass = request.get_json()
    hashing = hashlib.sha512(get_pass["password"].encode())
    pass_priv = hashing.hexdigest()
    cursor.execute(
            """
            SELECT password FROM projects WHERE id_project=? AND id_user=?
            """,(
                project_id,
                id_user
                )
            )
    row = cursor.fetchone()
    if pass_priv != row[0]:
        cursor.close()
        conn.close()
        return{"success": False}, 404
    cursor.close()
    conn.close()
    return {"success":True},200

@app.route('/projects/<project_id>/files/creation', methods=["POST"])
def files_creation(project_id):
    extension={
        "html":".html",
        "css":".css",
        
    }
    data= request.get_json()
    filename = data['filename']
    type_file = data['type']
    filenameFull = filename+extension[type_file]
    save_file_transport = Files(filenameFull, extension[type_file], project_id)
    save_file_transport.create_file()

    if save_file_transport == False:
        return {"success":False}, 404


    path_file = f"projects/{project_id}"

    os.makedirs(path_file, exist_ok=True)
    
    filename_path = os.path.join(path_file, filenameFull)

    with open(filename_path,"w", encoding="utf-8") as f:
        if type_file == "html":
            f.write(
            f"<!DOCTYPE html>\n"
            f" <html lang=\"en\">\n"
            f"<head>\n"
            f"<meta charset=\"UTF-8\">\n"
            f"<meta name=\"viewport\" \n"
            f"content=\"width=device-width, initial-scale=1.0\">\n" 
            f"<title>{filename}</title>\n"
            f"</head>\n"
            f"<body>\n"
            f"</body>\n"
            f"</html>\n")





    return {"success":True,
            "filename": filenameFull,
            "project_id":project_id
            }

@app.route('/projects/<project_id>/<filename>/open', methods=["GET",'POST'])
def open_file(project_id, filename):

    filepath = os.path.join(
        "projects", project_id, filename
    )
    with open (filepath, "r", encoding="utf-8") as f:
        content = f.read()

    return render_template( 
        "file.html",
        project_id=project_id,
        filename= filename,
        content=content
    )




@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/settings', methods=["GET", "POST"])
def settings():
    
    return render_template("settings.html")

if __name__ == "__main__":
    db = SQLite3("kitTest.db")
    db.start_tables()
    app.run(debug=True)

