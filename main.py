from flask import * 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import uuid
import hashlib
import sqlite3
import os

from sqlalchemy import or_
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "ae6dasasdsddd6514fa8d4a5ccc16a6574601db6dca/@*axmsao129n29330231j2091n3s9e313fs92s901292192012js9j102js019"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///kitTest.db"

dbAlchemy = SQLAlchemy(app)

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
    
#photos
class Pictures(dbAlchemy.Model):
    id = dbAlchemy.Column(
         dbAlchemy.String(36),
         primary_key=True,
         default= lambda: str(uuid.uuid4())
    )

    name = dbAlchemy.Column(
            dbAlchemy.Text,
            nullable=False,
    )

    id_user = dbAlchemy.Column(
           dbAlchemy.String(36),
           dbAlchemy.ForeignKey('user.id'),
           nullable=False
    )
    @classmethod
    def upload_image(cls, image):
        image = cls(
            name = image,
            id_user = session.get("user_id")
        )
        dbAlchemy.session.add(image)
        dbAlchemy.session.commit()
        if image:
            return True



#Users

class User(dbAlchemy.Model):
    id = dbAlchemy.Column(
        dbAlchemy.String(36),
        primary_key = True,
        default = lambda:str(uuid.uuid4())
    )

    username = dbAlchemy.Column(
        dbAlchemy.String(25),
        nullable = False
    )

    mail = dbAlchemy.Column(
        dbAlchemy.String(120),
        nullable = False,
        unique = True
    )

    password = dbAlchemy.Column(
        dbAlchemy.String(100),
        nullable = False
    )
    @classmethod
    def create_user(cls, name, mail, password):
        hashing = hashlib.sha512(password.encode())
        pass_priv = hashing.hexdigest()
        users = cls(
            username=name,
            mail = mail,
            password = pass_priv
        )
        dbAlchemy.session.add(users)
        dbAlchemy.session.commit()
        
        

    @classmethod
    def sing_in(cls, loginUser, password):
        loginUser = loginUser.strip()
        password = password.strip()

        hashPass = hashlib.sha512(password.encode())
        hashedPass = hashPass.hexdigest()

        user = cls.query.filter(
            or_(
                cls.username == loginUser,
                cls.mail == loginUser
            ),
            cls.password == hashedPass
        ).first()

        if user:
            return bool(user), user
    @classmethod
    def update(cls, changes):
        
        user = cls.query.filter_by(id = session.get("user_id")).first()
        if not user:
            return False

        if changes.get("username") != None:
            user.username = changes.get("username")
            dbAlchemy.session.commit()
        if changes.get("user_mail") != None:
            user.mail = changes.get("user_mail")
            dbAlchemy.session.commit()
        if changes.get("password") != None:
            user.password = changes.get("password")
            dbAlchemy.session.commit()

        return True


#context_procesor
@app.context_processor
def inject_user_data():
    session_id = session.get("user_id")
    projects =[]
    

    if 'user_id' not in session:
        return {
                "user":None,
                "picture":None,
    
        }

    user = dbAlchemy.session.get(User, session_id)
    pictureRow= (Pictures.query.filter_by(id_user = session_id).order_by(Pictures.id.desc()).first())
    picture = url_for('uploads_filename', filename=pictureRow.name)
    return {
            "user":user,
            "picture":picture,
            "projects":projects
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
            User.create_user(username, mail, password)
            return redirect(url_for('home', username = username))
    
    return render_template("create-account.html")

@app.route('/sign-in', methods=["GET", "POST"])
def login():
    
    userToken = request.form.get('loginUser')
    password = request.form.get('password')
    action = request.form.get('action')

    if request.method == "POST" and action == "login":
        
        verification, userData = User.sing_in(userToken, password)

        if verification:
            
            session['user_id'] = userData.id
            session['username'] = userData.username
            session['user_mail'] = userData.mail
            session['password'] = userData.password
           

    
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

         
            if extension in valid_extension:
                filename = f"{str(uuid.uuid4())}.{extension}"
        
                file.save(f"uploads/{filename}")
                Pictures.upload_image(filename)
                



        changes = {}

        if username:changes['username'] = username
        if mail: changes['user_mail'] = mail

        if password:
            hashPass = hashlib.sha512(password.encode())
            changes['password'] = hashPass.hexdigest()
        else:
            changes['password'] = None
            
        User.update(changes)

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

    if get_pass["source"] == "terminal":
            hashing = hashlib.sha512(get_pass["password_project"].encode())
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
    else:



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

    if data["source"] == "terminal":
        filename = data['filename']
        type_file = data['type_filename']
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
    else:
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
    with app.app_context():
        dbAlchemy.create_all()
    app.run(debug=True)

