from collections import namedtuple

from flask import g
from flask import escape
from flask import render_template
from flask import request
from flask import Flask,redirect

from voyager.db import get_db, execute
from voyager.validate import validate_field, render_errors
from voyager.validate import NAME_RE, INT_RE, DATE_RE

def sailors(conn):
    return execute(conn, "SELECT s.sid, s.name, s.age, s.experience FROM Sailors AS s")

def sailor_who(conn, boat_n):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages ON s.sid=Voyages.sid INNER JOIN Boats ON Boats.bid=Voyages.bid WHERE Boats.name='{boat_n}'")

def boats_who(conn, sailors_n):
    return execute(conn, f"SELECT b.bid, b.name FROM Boats AS b INNER JOIN Voyages ON b.bid=Voyages.bid INNER JOIN Sailors ON Sailors.sid=Voyages.sid WHERE Sailors.name='{sailors_n}'")

def dates_who(conn, s_date):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages ON s.sid=Voyages.sid WHERE Voyages.date_of_voyage='{s_date}'")

def colors_who(conn, s_color):
    return execute(conn, f"SELECT s.sid, s.name FROM Sailors AS s INNER JOIN Voyages ON s.sid=Voyages.sid INNER JOIN Boats ON Boats.bid=Voyages.bid WHERE Boats.color='{s_color}'")

def add_sailor(conn, add_s_name,add_s_age,add_s_exp):
    return execute(conn, f"INSERT INTO Sailors(name, age, experience) VALUES ('{add_s_name}','{add_s_age}','{add_s_exp}')")

def add_boat(conn, add_b_name,add_b_color):
    return execute(conn, f"INSERT INTO Boats(name, color) VALUES ('{add_b_name}','{add_b_color}')")

def add_voyage(conn, add_v_sid,add_v_bid, add_v_date):
    return execute(conn, f"INSERT INTO Voyages(sid, bid, date_of_voyage) VALUES ('{add_v_sid}','{add_v_bid}','{add_v_date}')")


def views(bp):
    @bp.route("/sailors/add", methods=["POST"])
    def _add_sailor():
        if request.method == "POST":
            add_s_name = request.form['add-sailor-name']
            add_s_age = request.form['add-sailor-age']
            add_s_exp = request.form['add-sailor-experience']
            with get_db() as conn:
                add_sailor(conn, add_s_name, add_s_age, add_s_exp)
            return redirect("/sailors")

    @bp.route("/boats/add", methods=["POST"])
    def _add_boat():
        if request.method == "POST":
            add_b_name = request.form['add-boat-name']
            add_b_color = request.form['add-boat-color']
            with get_db() as conn:
                add_boat(conn, add_b_name, add_b_color)
            return redirect("/boats")

    @bp.route("/voyages/add", methods=["POST"])
    def _add_voyage():
        if request.method == "POST":
            add_v_sid = request.form['add-voyage-sid']
            add_v_bid = request.form['add-voyage-bid']
            add_v_date = request.form['add-voyage-date']
            with get_db() as conn:
                add_voyage(conn, add_v_sid, add_v_bid, add_v_date)
            return redirect("/voyages")


    @bp.route("/sailors")
    def _get_all_sailors():
        with get_db() as conn:
            rows = sailors(conn)
        return render_template("table.html", name="sailors", rows=rows)


    @bp.route("/sailors/who-sailed", methods = ["POST"])
    def _who_sailed():
        if request.method == "POST":
            boat_n = request.form['boat-name']
            with get_db() as conn:
                rows = sailor_who(conn, boat_n)
            return render_template("table.html", rows=rows, name="Boats")


    @bp.route("/boats/sailed-by", methods = ["POST"])
    def _boats_sailed_by():
        if request.method == "POST":
            sailors_n = request.form['sailor-name']
            with get_db() as conn:
                rows = boats_who(conn, sailors_n)
            return render_template("table.html", rows=rows, name="Sailors")

    @bp.route("/sailors/who-sailed-on-date", methods = ["POST"])
    def _who_sailed_date():
        if request.method == "POST":
            s_date = request.form['date']
            with get_db() as conn:
                rows = dates_who(conn, s_date)
            return render_template("table.html", rows=rows, name="Sailors")


    @bp.route("/sailors/who-sailed-on-boat-of-color", methods = ["POST"])
    def _who_sailed_color():
        if request.method == "POST":
            s_color = request.form['color']
            with get_db() as conn:
                rows = colors_who(conn, s_color)
            return render_template("table.html", rows=rows, name="Sailors")

   