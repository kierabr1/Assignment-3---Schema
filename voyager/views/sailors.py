from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

def sailor_who(conn, boat_n):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages ON s.sid=Voyages.sid INNER JOIN Boats ON Boats.bid=Voyages.bid WHERE Boats.name='{boat_n}'")

def boats_who(conn, sailors_n):
    return execute(conn, f"SELECT b.bid, b.name FROM Boats AS b INNER JOIN Voyages ON b.bid=Voyages.bid INNER JOIN Sailors ON Sailors.sid=Voyages.sid WHERE Sailors.name='{sailors_n}'")

def views(bp):
    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="sailors", rows=rows)


    @bp.route("/sailors/who-sailed", methods = ["POST"])
    def _datainput1():
        if request.method == "POST":
            boat_n = request.form['boat-name']
            with get_db() as conn:
                rows = sailor_who(conn, boat_n)
            return render_template("table.html", rows=rows, name="Boats")


    @bp.route("/boats/sailed-by", methods = ["POST"])
    def _datainput2():
        if request.method == "POST":
            sailors_n = request.form['sailor-name']
            with get_db() as conn:
                rows = boats_who(conn, sailors_n)
            return render_template("table.html", rows=rows, name="Sailors")


