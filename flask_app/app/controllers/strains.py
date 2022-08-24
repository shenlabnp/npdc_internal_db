#!/usr/bin/env python3

from flask import render_template, request, session, redirect, url_for
import sqlite3
import pandas as pd

# import global config
from ..config import conf
from ..session import check_logged_in

# set blueprint object
from flask import Blueprint
blueprint = Blueprint('strains', __name__)


@blueprint.route("/strains/view")
def page_strains():

    # check login
    if not check_logged_in():
        return redirect(url_for("login.page_login"))
        
    # page title
    page_title = "Strains Collection"
    page_subtitle = (
        ""
    )

    # render view
    return render_template(
        "strains/main.html.j2",
        page_title=page_title,
        page_subtitle=page_subtitle
    )


@blueprint.route("/api/strains/get_overview")
def get_overview():
    """ for strain overview tables """
    result = {}
    result["draw"] = request.args.get('draw', type=int)
    limit = request.args.get('length', type=int)
    offset = request.args.get('start', type=int)

    with sqlite3.connect(conf["db_path"]) as con:
        cur = con.cursor()

        # fetch total records
        result["recordsTotal"] = cur.execute((
            "select count(npdc_id)"
            " from strains"
        )).fetchall()[0][0]

        # fetch total records (filtered)
        result["recordsFiltered"] = cur.execute((
            "select count(npdc_id)"
            " from strains"
        )).fetchall()[0][0]


        result["data"] = []

        query_result = pd.read_sql_query((
            "select *"
            " from strains order by npdc_id"
            " limit {} offset {}"
        ).format(limit, offset), con)


        for idx, row in query_result.iterrows():
            result["data"].append([
                "NPDC{:06d}".format(row["npdc_id"]),
                "-",
                "-",
                "-" if row["collection_date"] == "" else row["collection_date"],
                "Unknown" if row["collection_country"] == "" else row["collection_country"],
                "-",
                "-",
            ])

    return result