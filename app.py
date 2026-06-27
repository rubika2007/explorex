from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_mail import Mail, Message
import os
app = Flask(__name__)

# ---------------- MAIL CONFIG ----------------





app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD']=os.getenv("MAIL_PASSWORD")
mail=Mail(app)
db=mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor=db.cursor()


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- PLACES PAGE ----------------

@app.route("/places")
def places():
    return render_template("packages.html")

# ---------------- TEMPLE PAGES ----------------

@app.route("/meenakshi")
def meenakshi():
    return render_template("meenakshi.html")


@app.route("/alagar")
def alagar():
    return render_template("alagar.html")


@app.route("/mariamman")
def mariamman():
    return render_template("mariamman.html")


@app.route("/pala")
def pala():
    return render_template("pala.html")

@app.route("/samanar")
def samanar():
    return render_template("samanar.html")

@app.route("/yanaimalai")
def yanaimalai():
    return render_template("yanaimalai.html")

@app.route("/nagamalai")
def nagamalai():
    return render_template("nagamalai.html") 

@app.route("/thirumalai")
def thirumalai():
    return render_template("thirumalai.html") 
@app.route("/gandhi")
def gandhi():
    return render_template("gandhi.html") 
@app.route("/keeladi")
def keeladi():
    return render_template("keeladi.html") 
@app.route("/mary")
def mary():
    return render_template("mary.html") 
@app.route("/mosque")
def mosque():
    return render_template("mosque.html")
@app.route("/konar")
def konar():
    return render_template("konar.html") 
@app.route("/murugan")
def murugan():
    return render_template("murugan.html")
@app.route("/amman")
def amman():
    return render_template("amman.html")
@app.route("/sabarees")
def sabarees():
    return render_template("sabarees.html")
# ---------------- ABOUT ----------------

@app.route("/about")
def about():
    return render_template("index.html")


# ---------------- CONTACT ----------------

@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/submit",methods=["POST"])
def submit():

    name=request.form['name']
    email=request.form['email']
    place=request.form['place']
    purpose=request.form['purpose']
    message=request.form['message']

    sql="""
    INSERT INTO contact
    (name,email,place,purpose,message)
    VALUES(%s,%s,%s,%s,%s)
    """

    values=(
        name,
        email,
        place,
        purpose,
        message
    )

    cursor.execute(sql,values)
    db.commit()

    return redirect(url_for("contact"))


# ---------------- LOGIN ----------------

@app.route("/login",methods=["GET","POST"])
def login():

    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        query="""
        SELECT * FROM admin
        WHERE email=%s
        AND password=%s
        """

        cursor.execute(query,(email,password))

        admin=cursor.fetchone()

        if admin:
            return redirect(url_for("admin"))

        return "Invalid Login"

    return render_template("login.html")


# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin")
def admin():

    cursor.execute("SELECT * FROM contact")
    data=cursor.fetchall()

    users=[]

    for row in data:

        users.append({

            "id":row[0],
            "name":row[1],
            "email":row[2],
            "place":row[3],
            "purpose":row[4],
            "message":row[5],
            "reply":row[6],
            "status":row[7]
        })


    cursor.execute("SELECT COUNT(*) FROM places")
    total_places=cursor.fetchone()[0]


    cursor.execute("SELECT COUNT(*) FROM contact")
    total_users=cursor.fetchone()[0]


    cursor.execute(
    "SELECT COUNT(*) FROM contact WHERE purpose='Feedback'"
    )

    feedback_count=cursor.fetchone()[0]


    cursor.execute(
    "SELECT COUNT(*) FROM contact WHERE purpose!='Feedback'"
    )

    query_count=cursor.fetchone()[0]


    cursor.execute("SELECT * FROM places")
    places=cursor.fetchall()


    return render_template(
        "admin.html",
        users=users,
        places=places,
        total_places=total_places,
        total_users=total_users,
        feedback_count=feedback_count,
        query_count=query_count
    )


# ---------------- ADD PLACE ----------------

@app.route("/add_place",methods=["POST"])
def add_place():

    place_name=request.form["place_name"]
    location=request.form["location"]
    timings=request.form["timings"]
    weather=request.form["weather"]
    description=request.form["description"]
    image=request.form["image"]
    map_link=request.form["map_link"]

    sql="""
    INSERT INTO places
    (place_name,location,timings,weather,
    description,image,map_link)

    VALUES(%s,%s,%s,%s,%s,%s,%s)
    """

    values=(
        place_name,
        location,
        timings,
        weather,
        description,
        image,
        map_link
    )

    cursor.execute(sql,values)

    db.commit()

    return redirect(url_for("admin"))

# ---------------- EDIT PLACE ----------------
@app.route("/edit_place", methods=["POST"])
def edit_place():

    id = request.form["id"]
    place_name = request.form["place_name"]
    location = request.form["location"]
    timings = request.form["timings"]
    weather = request.form["weather"]
    description = request.form["description"]
    image = request.form["image"]
    map_link = request.form["map_link"]

    cursor.execute("""
        UPDATE places
        SET place_name=%s,
            location=%s,
            timings=%s,
            weather=%s,
            description=%s,
            image=%s,
            map_link=%s
        WHERE id=%s
    """, (
        place_name, location, timings, weather,
        description, image, map_link, id
    ))

    db.commit()

    return redirect(url_for("admin"))


# ---------------- DELETE PLACE ----------------

@app.route("/delete_place/<int:id>", methods=["POST"])
def delete_place(id):

    cursor.execute(
    "DELETE FROM places WHERE id=%s",
    (id,)
    )

    db.commit()

    return redirect(url_for("admin"))


# ---------------- REPLY MAIL ----------------

@app.route("/reply/<int:id>",methods=["POST"])
def reply(id):

    reply_text=request.form["reply"]

    cursor.execute(
    """
    UPDATE contact
    SET reply=%s,
    status='Replied'
    WHERE id=%s
    """,
    (reply_text,id)
    )

    db.commit()

    cursor.execute(
    "SELECT email FROM contact WHERE id=%s",
    (id,)
    )

    user=cursor.fetchone()

    email=user[0]

    msg=Message(
        subject="Reply from ExploreX",
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
    )

    msg.body=reply_text

    mail.send(msg)

    return redirect(url_for("admin"))

@app.route("/place/<int:id>")
def place_details(id):

    cursor.execute(
    "SELECT * FROM places WHERE id=%s",
    (id,)
    )

    place=cursor.fetchone()

    return render_template(
    "place_details.html",
    place=place
    )
@app.route("/search_places")
def search_places():

    query = request.args.get("q","").lower()

    # Database search
    cursor.execute("""
        SELECT id, place_name
        FROM places
        WHERE place_name LIKE %s
        LIMIT 5
    """, ("%" + query + "%",))

    results = cursor.fetchall()

    data = []

    for r in results:
        data.append({
            "id": r[0],
            "name": r[1],
            "url": "/place/" + str(r[0])
        })

    # Manual places
    manual_places = [
        {"name":"Meenakshi Amman Temple","url":"/meenakshi"},
        {"name":"Alagar Kovil","url":"/alagar"},
        {"name":"Palamudhircholai Kovil","url":"/pala"},
        {"name":"Teppakulam Mariamman Kovil","url":"/mariamman"},
        {"name":"Samanar Hills","url":"/samanar"},
        {"name":"Yanaimalai Hills","url":"/yanaimalai"},
        {"name":"Nagamalai Hills","url":"/nagamalai"},
         {"name":"Thirumalai Nayakar Mahal","url":"/thirumalai"},
           {"name":"Gandhi Memorial Museum","url":"/gandhi"},
         {"name":"Keeladi Museum","url":"/keeladi"},
         {"name":"St Mary's Cathedral","url":"/mary"},
         {"name":"Goripalayam Dargah","url":"/mosque"},
         {"name":"Konar Kadai","url":"/konar"},
         {"name":"Murugan Idli Shop","url":"/murugan"},
         {"name":"Amman Mess","url":"/amman"},
         {"name":"Sree Sabarees Hotel","url":"/sabarees"}

    ]

    for place in manual_places:
        if query in place["name"].lower():
            data.append(place)

    return {"results": data}
if __name__=="__main__":
    app.run(debug=True)