from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from .models import Event
from . import db
import json
from datetime import datetime

views = Blueprint('views', __name__)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    all_events = Event.query.order_by(Event.date.desc()).all()                          
    return render_template("home.html", user=current_user, all_events=all_events) 


@views.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST': 
        event = request.form.get('event') 
        price = request.form.get('price')
        day = request.form.get('day')
        time = request.form.get('time')
        place = request.form.get('place')
        link = request.form.get('link')
        name = request.form.get('name')
        background_image = request.form.get('background_image')
        qr_code_image = request.form.get('qr_code_image')

        # Check if the post request has the file part
        # if 'background_image' in request.files:
        #     background_image = request.files['background_image']
        #     if background_image and allowed_file(background_image.filename):
        #         filename = secure_filename(background_image.filename)
        #         background_image.save(os.path.join(UPLOAD_FOLDER, filename))
        #         background_image_path = os.path.join('images', filename)
        #     else:
        #         flash('Invalid background image file!', category='error')
        #         return redirect(request.url)

        # if 'qr_code_image' in request.files:
        #     qr_code_image = request.files['qr_code_image']
        #     if qr_code_image and allowed_file(qr_code_image.filename):
        #         filename = secure_filename(qr_code_image.filename)
        #         qr_code_image.save(os.path.join(UPLOAD_FOLDER, filename))
        #         qr_code_image_path = os.path.join('images', filename)
        #     else:
        #         flash('Invalid QR code image file!', category='error')
        #         return redirect(request.url)

        if not name or len(name) < 2:
            flash('Event name is too short!', category='error')   
        else:
            new_event = Event(data=event, user_id=current_user.id,
                              price=price, day=day, time=time, place=place, 
                              link=link, name=name, background_image_filename=background_image, qr_code_image_filename=qr_code_image)
            db.session.add(new_event)
            db.session.commit()
            flash('Event added!', category='success')
            return redirect(url_for('views.home'))

    return render_template("create.html", user=current_user)

@views.route('/my-events', methods=['GET', 'POST'])
@login_required
def my_events():
    return render_template("my_events.html", user=current_user)    

@views.route('/delete-event', methods=['POST'])
def delete_event():  
    event = json.loads(request.data)
    eventId = event['eventId']
    event = Event.query.get(eventId)
    if event:
        if event.user_id == current_user.id:
            db.session.delete(event)
            db.session.commit()
            flash('Event Deleted!', category='success')

    return jsonify({})
