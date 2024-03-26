import flask_session
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from sweater.models import UserInfo, SendDataProducts, Processors, Videocards
from sweater import login_manager, db, app, mail,  Message, ALLOWED_EXTENSIONS
from password_generator import PasswordGenerator
from werkzeug.utils import secure_filename
from show_in_database import show_processor, show_videocards, show_applications_database, show_test_data
import uuid, os

@login_manager.user_loader
def load_user(user_id):
    return UserInfo.query.get(int(user_id))


@app.route('/')
def home():
    return render_template("all_home_page.html")

@app.route('/projects')
def projects():
    show_projects = SendDataProducts.query.filter_by(status="3").all()
    print(show_projects)
    return render_template("projects.html", show_projects=show_projects)



@app.route('/projects/<id_project>/view', methods=['POST','GET'])
def view_projects_user(id_project):
    show_applications_data = SendDataProducts.query.filter_by(id=id_project, status="3").all()

    print(show_applications_data)


    return render_template('view_project.html', show_applications_data=show_applications_data)

@app.route('/projects/virtual_tour', methods=['POST','GET'])
def virtual_tour():

    return render_template('virtualtour.html')



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if UserInfo.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("You've already signed up with that email, log in instead")
            return redirect(url_for('login'))

        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = UserInfo(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password,
            status="Admin"
        )

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        status_login = UserInfo.query.filter_by(email=current_user.email, status="Admin").first()
        if status_login:
            return redirect(url_for('adminmenu'))
        else:
            return redirect(url_for('usermenu'))


    else:
        if request.method == "POST":
            email = request.form.get('email')
            password = request.form.get('password')

            # Find user by email entered
            user = UserInfo.query.filter_by(email=email).first()
            status = UserInfo.query.filter_by(status="Admin", email=email).first()

            # Email doesn't exist
            if not user:
                flash("Такого пользователя не существует!")
                return redirect(url_for('login'))
            # Password incorrect
            elif not check_password_hash(user.password, password):
                flash('Пароль не подходит!')

            else:
                if status:
                    login_user(user)
                    return redirect(url_for('adminmenu'))
                else:
                    login_user(user)
                    return redirect(url_for('usermenu'))


        return render_template("user_authorization.html", logged_in=current_user.is_authenticated)


@app.route('/adminmenu')
@login_required
def adminmenu():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="Admin").first()
    if status_login:
        show_projects = SendDataProducts.query.filter_by(status="1").count()
        print(show_projects)
        print(current_user.name)
        return render_template("adminmenu.html", name=current_user.name, logged_in=True, count=show_projects)
    else:
        return redirect(url_for('home'))


@app.route('/adminmenu/personal_account', methods=["GET", "POST"])
@login_required
def personal_account():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="Admin").first()
    if status_login:
        if request.method == "POST":
            pas_1 = request.form.get('password')
            pas_2 = request.form.get('old_password')
            pas_3 = request.form.get('old_password_two')
            user = UserInfo.query.filter_by(email=current_user.email).first()
            print(user)
            if user:
                if check_password_hash(user.password, pas_1):
                    if pas_2 == pas_3:
                        hash_and_salted_password = generate_password_hash(
                            pas_2,
                            method='pbkdf2:sha256',
                            salt_length=8
                        )

                        update_password = UserInfo.query.filter_by(email=current_user.email).first()
                        update_password.password = hash_and_salted_password
                        db.session.commit()
                        msg = Message(current_user.name, recipients=[current_user.email])
                        msg.html = "<h2>Ваш пароль был заменен!</h2>\n<p>Если вы не совершали замену пароля на вашем аккаунте то обратитесь к администратору.</p>"
                        mail.send(msg)
                        logout_user()
                        flash('Ваш пароль был изменен!')
                        return redirect(url_for('login'))


                    else:
                        flash('Новые пароли не совпадают!')

                else:
                    flash('Старый пароль не подходит!')







        return render_template("personal_account.html", name=current_user.name, logged_in=True)
    else:
        return redirect(url_for('home'))


@app.route('/usermenu/personal_account', methods=["GET", "POST"])
@login_required
def personal_user_account():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="User").first()
    if status_login:

        if request.method == "POST":
            pas_1 = request.form.get('password')
            pas_2 = request.form.get('old_password')
            pas_3 = request.form.get('old_password_two')
            user = UserInfo.query.filter_by(email=current_user.email).first()
            print(user)
            if user:
                if check_password_hash(user.password, pas_1):
                    if pas_2 == pas_3:
                        hash_and_salted_password = generate_password_hash(
                            pas_2,
                            method='pbkdf2:sha256',
                            salt_length=8
                        )

                        update_password = UserInfo.query.filter_by(email=current_user.email).first()
                        update_password.password = hash_and_salted_password
                        db.session.commit()
                        msg = Message(current_user.name, recipients=[current_user.email])
                        msg.html = "<h2>Ваш пароль был заменен!</h2>\n<p>Если вы не совершали замену пароля на вашем аккаунте то обратитесь к администратору.</p>"
                        mail.send(msg)
                        logout_user()
                        flash('Ваш пароль был изменен!')
                        return redirect(url_for('login'))


                    else:
                        flash('Новые пароли не совпадают!')

                else:
                    flash('Старый пароль не подходит!')

        return render_template("personal_user_account.html", name=current_user.name, logged_in=True)
    else:
        return redirect(url_for('home'))






@app.route('/adminmenu/show_applications', methods=["GET", "POST"])
@login_required
def show_applications():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="Admin").first()
    if status_login:
        show_data = show_applications_database()
        if request.method == 'POST':
            for key, val in request.form.items():
                if key.startswith("record"):
                    print(val)

                    return redirect(url_for('view_projects', id_project=val))


        return render_template("show.html", show_data=show_data)
    else:
        return redirect(url_for("home"))


@app.route('/adminmenu/show_users', methods=["GET", "POST"])
@login_required
def show_users():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="Admin").first()
    if status_login:
        users_data = UserInfo.query.filter_by(status="User").all()

        return render_template("show_users.html", show_data=users_data)
    else:
        return redirect(url_for("home"))

#test22
@app.route('/adminmenu/published_projects', methods=["GET", "POST"])
@login_required
def show_published_projects():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="Admin").first()
    if status_login:
        published_projects_data = SendDataProducts.query.filter_by(status="3").all()

        return render_template("published_projects.html", show_data=published_projects_data)
    else:
        return redirect(url_for("home"))


@app.route('/adminmenu/create_user', methods=["GET", "POST"])
@login_required
def create_user():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="Admin").first()
    if status_login:
        if request.method == "POST":
            email = request.form.get('email')
            email_two = request.form.get('email_two')
            usertype = request.form.get('usertype')
            if email == email_two:
                if UserInfo.query.filter_by(email=request.form.get('email')).first():
                    flash("alert-danger")
                    return redirect(url_for('create_user'))

                flash("alert-success")
                print('Сходится')
                guid = str(uuid.uuid4())
                os.makedirs('sweater/static/user_directory/{}'.format(guid), exist_ok=True)
                pwo = PasswordGenerator()
                passwrod = pwo.shuffle_password('qwertyuiopasdfghjklzxcvbnm1234567890', 5)
                hash_and_salted_password_for_registation = generate_password_hash(
                    passwrod,
                    method='pbkdf2:sha256',
                    salt_length=8
                )
                test = UserInfo(
                    email=email,
                    name="User",
                    password=hash_and_salted_password_for_registation,
                    status=usertype,
                    directory=guid,

                )
                db.session.add(test)
                db.session.commit()
                print(test.id)
                msg = Message("Subject", recipients=[email])
                msg.html = "<h2>Ваш пароль!</h2>\n<p>Пароль и логин от платформы phystech3d</p>\n<p>Пароль: </p>"+passwrod+"<p>Логин: </p>"+email
                mail.send(msg)
                return redirect(url_for("create_user"))

            else:
                print('Не сходится')
                flash("alert-danger")


        return render_template("create_user.html")

    else:
        return redirect(url_for("home"))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/download')
def download():
    return send_from_directory('static', filename="files/cheat_sheet.pdf")
@app.route('/usermenu')
@login_required
def usermenu():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="User").first()
    if status_login:
        print(current_user.name)
        return render_template("menu_second.html", name=current_user.name, logged_in=True)
    else:
        return redirect(url_for('home'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS




@app.route('/usermenu/submitting_an_application_from_the_user', methods=["GET", "POST"])
@login_required
def submitting_an_application():
    search_proc_info = show_processor()
    search_video_info = show_videocards()
    status_login = UserInfo.query.filter_by(email=current_user.email, status="User").first()
    if status_login:
        if request.method == "POST":
            project_name = request.form.get('name')
            vers = request.form.get('version')
            developer = request.form.get('autor')
            lang = request.form.get('lang')
            os_sys = request.form.get('os_system')
            arch = request.form.get('arch')
            processor = request.form.get('proc')
            ozu = request.form.get('ozu')
            videoadapter = request.form.get('video')
            disk = request.form.get('disk')
            if request.method == 'POST':
                file = request.files['slide_one']
                print(file)
                file_two = request.files['slide_two']
                file_three = request.files['slide_three']
                file_four = request.files['slide_four']
                data = UserInfo.query.filter_by(email=current_user.email).first()
                directory = data.directory
                file_list = [file, file_two, file_three, file_four]
                file_directory_list = []
                filename_list = []
                file_list_input_database = []
                for file_item in file_list:
                    if file_item and allowed_file(file_item.filename):
                        #filename = secure_filename(file_item.filename)
                        filename = file_item.filename
                        file_path = 'sweater/static/' + app.config['UPLOAD_FOLDER'] + "/" + directory
                        file_directory_list.append(file_path)
                        filename_list.append(filename)
                        file_full_path = 'sweater/static/' + file_path + '/' + filename
                        file_directory_name = app.config['UPLOAD_FOLDER'] + "/" + directory +'/'+ filename
                        file_list_input_database.append(file_directory_name)
                    else:
                        flash('Файл не подлежит нужному формату!')


                if len(file_directory_list) == 4 and len(filename_list) == 4:
                    counter = 0
                    for item in file_list:
                        item.save(os.path.join(file_directory_list[counter], filename_list[counter]))
                        counter+=1
                    insert_user_data = SendDataProducts(
                        project_name=project_name,
                        vers=vers,
                        developer=developer,
                        lang=lang,
                        os_sys=os_sys,
                        arch=arch,
                        processor=processor,
                        ozu=ozu,
                        status="1",
                        videoadapter=videoadapter,
                        disk=disk,
                        one_slide=file_list_input_database[0],
                        two_slide=file_list_input_database[1],
                        three_slide=file_list_input_database[2],
                        file=file_list_input_database[3],
                        user_email=current_user.email
                    )
                    db.session.add(insert_user_data)
                    db.session.commit()
                    flash("alert-warning", "Загрузка завершена!")
                    return redirect(url_for("submitting_an_application"))




                else:
                   print("Сохранения не будет")

        return render_template("submitting_an_application_from_the_user.html", search_proc_info=search_proc_info, search_video_info=search_video_info)
    else:
        return redirect(url_for("home"))

@app.route('/adminmenu/show_applications/test_show/<id_project>#',  methods=['POST','GET'])
@login_required
def view_projects(id_project):
    status_login = UserInfo.query.filter_by(email=current_user.email, status="Admin").first()
    if status_login:
        show_applications_data = SendDataProducts.query.filter_by(id=id_project).all()
        project_file_download = db.session.query(SendDataProducts.file). \
            filter_by(id=id_project). \
            scalar()
        id_project_list = []
        id_project_list.append(id_project)
        print(id_project_list)
        if request.method == 'POST':
            if 'button_upload' in request.form.keys():
                if request.form['button_upload'] in id_project_list:
                    update_status = SendDataProducts.query.filter_by(id=id_project).first()
                    update_status.status = '2'
                    db.session.commit()
                    return redirect(url_for('show_applications'))

            if 'button_delete' in request.form.keys():
                if request.form['button_delete'] in id_project_list:
                    update_status = SendDataProducts.query.filter_by(id=id_project).first()
                    update_status.status = '-1'
                    db.session.commit()
                    return redirect(url_for('show_applications'))

            if 'button_back' in request.form.keys():
                if request.form['button_back'] in id_project_list:
                    return redirect(url_for('show_applications'))
            #afd_filename = request.form.get('filename')
            #return send_file('static/' + project_file_download, as_attachment=True)
        return render_template('test.html', show_applications_data=show_applications_data)
    else:
        pass


@app.route('/usermenu/show_user_application',  methods=['POST','GET'])
@login_required
def user_application():
    status_login = UserInfo.query.filter_by(email=current_user.email, status="User").first()
    if status_login:
        show_applications_data = SendDataProducts.query.filter_by(user_email=current_user.email, status="2").all()
        id_user_project_list = []
        for id_project in show_applications_data:
            id_user_project_list.append(str(id_project.id))
        if request.method == 'POST':
            if 'delete_project' in request.form.keys():
                if request.form['delete_project'] in id_user_project_list:
                    button_id = request.form['delete_project']
                    update_status = SendDataProducts.query.filter_by(id=button_id).first()
                    update_status.status = '-2'
                    db.session.commit()
                    return redirect(url_for('user_application'))


            if 'add_project' in request.form.keys():
                if request.form['add_project'] in id_user_project_list:
                    button_id = request.form['add_project']
                    update_status = SendDataProducts.query.filter_by(id=button_id).first()
                    update_status.status = '3'
                    db.session.commit()
                    return redirect(url_for('user_application'))






        return render_template('show_user_applications.html', show_applications_data=show_applications_data)

    else:
        pass


@app.route('/game',  methods=['POST','GET'])
def game():
    return render_template('index.html')