from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

def get_stocks(strategies):
    return {}

@views.route('/portfolio', methods=['POST','GET'])
def portfolio():
    stocks = {}
    if request.method == 'POST':
        strategies = []
        amount = request.form.get('amount')
        for strategy in request.form:
            if request.form.get(strategy) == '1':
                strategies.append(strategy)
        
        print(amount ,strategies)

        stocks = get_stocks(strategies)


    return render_template("portfolio.html", user=current_user, stocks=stocks)