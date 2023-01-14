from flask import Flask, render_template, request, redirect, session
from flask_session import Session
import flask_login
from database import *
from datetime import date
from flask_login import login_user
from passlib.hash import sha256_crypt
from flask import Markup
import markdown


# Creating instances
app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.static_folder = 'static'

# User accesible routes
# Home
@app.route('/')
def welcome():
    Database.cursor.execute("SELECT * FROM blog_articles LIMIT 4")
    all_posts = Database.cursor.fetchall()
    lst_items = []
    for item in all_posts:
        lst_items.append(list(item))

    for item in lst_items:
        item[2] = Markup(item[2])

    return render_template("index.html", data=lst_items)


# View a single post
@app.route("/posts/view/<int:id>")
def post_view(id):
    Database.cursor.execute(f"SELECT * FROM blog_articles WHERE id='{id}'")
    single_post = list(Database.cursor.fetchone())
    
    single_post[2] = Markup(single_post[2])

    return render_template("view_post.html", data=single_post)


@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/resume.html")
def resume():
    return render_template("resume.html")

@app.route("/portfolio.html")
def portfolio():
    return render_template("portfolio.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")


@app.route("/portfolio-Discord-notifyer.html")
def portfolio_dn():
    return render_template("portfolio-Discord-notifyer.html")

@app.route("/portfolio-handbuildcomputers.html")
def portfolio_handbuildcomputers():
    return render_template("portfolio-handbuildcomputers.html")

@app.route("/portfolio-python-game.html")
def portfolio_python_game():
    return render_template("portfolio-python-game.html")

@app.route("/portfolio-weerbot.html")
def portfolio__weather_bot():
    return render_template("portfolio-weerbot.html")


# ADMIN 
@app.route("/login", methods=["POST", "GET"])
def admin_login():
     # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']


        # Check if account exists using MySQL
        Database.cursor.execute(f"SELECT * FROM users WHERE username='{username}'")
        account = Database.cursor.fetchone()

        if sha256_crypt.verify(password, account[3]) == True:

            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['username'] = account[1]
            # Redirect to home page
            return redirect("/dashboard")
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'            
            return msg

    return render_template("/admin/login.html")


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if not 'loggedin' in session:
        return redirect('/login')
        
    if request.method == 'POST':

        post_title = request.form['title']
        post_content = request.form['editor']
        post_author = request.form['author']

        Database.cursor.execute(f"INSERT INTO blog_articles (title, content, posted_by, posted_on) VALUES ('{post_title}', '{post_content}', '{post_author}', '{date.today()}')")
        Database.db.commit()

        return redirect('/posts')
    else:
        return render_template('/admin/new_post.html')


@app.route('/posts',  methods=['GET', 'POST'])
def posts():
    if not 'loggedin' in session:
        return redirect('/login')

    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['editor']
        post_author = request.form['author']

        Database.cursor.execute(f"INSERT INTO blog_articles (title, content, posted_by, posted_on) VALUES ('{post_title}', '{post_content}', '{post_author}', '{date.today()}')")
        Database.db.commit()

        return redirect('/posts')

    else:
        Database.cursor.execute("SELECT * FROM blog_articles ORDER BY posted_on DESC")
        all_posts = Database.cursor.fetchall()
        lst_items = []
        for item in all_posts:
            lst_items.append(list(item))

        for item in lst_items:
            item[2] = Markup(item[2])
            
        return render_template('/admin/posts.html', posts=lst_items)


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if not 'loggedin' in session:
        return redirect('/login')

    Database.cursor.execute(f"SELECT * FROM blog_articles WHERE id={id}")
    to_edit = Database.cursor.fetchone()

    if request.method == 'POST':
        to_edit_title = request.form['title']
        to_edit_author = request.form['author']
        to_edit_content = request.form['editor']
        Database.cursor.execute(f"UPDATE blog_articles SET title = '{to_edit_title}', content = '{to_edit_content}', posted_by = '{to_edit_author}' WHERE id='{id}'")
        Database.db.commit()

        return redirect('/posts')
        

    else:
        return render_template('/admin/edit.html', post=to_edit)


@app.route('/posts/delete/<int:id>')
def delete(id):
    if not 'loggedin' in session:
        return redirect('/login')

    Database.cursor.execute(f"DELETE FROM blog_articles WHERE id={id}")
    Database.db.commit()
    return redirect('/posts')


@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect("login")


# Test admin page
@app.route("/dashboard", methods=["GET"])
def admin_dash():
    if 'loggedin' in session:
        return render_template('/admin/dashboard.html')
    else:
        return redirect("/login")





if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")    