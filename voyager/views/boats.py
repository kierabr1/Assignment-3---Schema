
from collections import namedtuple

from flask import render_template
from flask import request
from flask import escape

from voyager.db import get_db, execute

def boats(conn):
    return execute(conn, "SELECT b.bid, b.name, b.color FROM Boats AS b")

def popularity(conn):
    return execute(conn, f"SELECT b.name, COUNT(*) AS total_reservations FROM Boats AS b, Voyages WHERE b.bid=Voyages.bid GROUP BY Voyages.bid ORDER BY count(*) DESC")


def views(bp):
    @bp.route("/boats")
    def _boats():
        with get_db() as conn:
            rows = boats(conn)
        return render_template("table.html", name="boats", rows=rows)

    @bp.route("/boats/by-popularity", methods = ["GET", "POST"])
    def _boats_popularity():
        with get_db() as conn:
            rows = popularity(conn)
        return render_template("table.html", name="boats", rows=rows)


  