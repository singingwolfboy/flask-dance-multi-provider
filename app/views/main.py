from flask import Blueprint, render_template

blueprint = Blueprint("main", __name__)


@blueprint.route("/")
def index():
    return render_template("home.j2")
