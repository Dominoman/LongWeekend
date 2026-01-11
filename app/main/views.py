import os

from flask import render_template
from sqlalchemy import text, func

from common.apininja import Ninja
from config import Config
from . import main
from .. import db
from ..models import Search


@main.route('/')
def index():
    return 'Sabai sabai'

@main.route('/longweekend')
def test():
    logos = {}
    apininja=Ninja(Config.APININJASKEY,Config.LOGOS)
    with open("sql/monthly_5_cheapest.sql") as f:
        sql = text(f.read())
    result=db.session.execute(sql).mappings().all()
    for row in result:
        l=apininja.get_logo(row['firstairline'])
        logos[row['firstairline']]=os.path.basename(l['logo_url'])
    latest_ts = db.session.query(
        func.max(Search.timestamp)
    ).scalar()
    return render_template('index.html',itineraries=result,logos=logos, latest_ts=latest_ts)