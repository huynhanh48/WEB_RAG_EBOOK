from flask import Blueprint, render_template, request, redirect, url_for
from markupsafe import escape
from RAG.GemiAI import result

bp = Blueprint("pages", __name__)

@bp.route("/")
def home():
    return render_template("pages/home.html")

@bp.route("/about")
def about():
    return render_template("pages/about.html")

@bp.route("/submitForm", methods=["GET", "POST"])
def handleForm():
    username = request.args.get("username")
    if username:
        # Escape để đảm bảo an toàn trước khi truyền vào template
        username = escape(username)
        answer = result(username)
        #chung ta se chen mo hinh ngon ngu lon vao
        return render_template('pages/submitForm.html', username=answer)
    return render_template('pages/submitForm.html')

# @bp.route("/submitForm/display")
# def submitFormDisplay():
#     username = request.args.get("username")
#     return render_template('pages/submitForm.html', username=username)