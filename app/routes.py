import os
from flask import Flask, flash, request, render_template, redirect, url_for, jsonify, send_from_directory
from models import User, Music, EmailGroup, SendEmail, VerificationEmail, PaymentReceived
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
from werkzeug.utils import secure_filename
from sqlalchemy import desc, and_, asc
from datetime import datetime


#from forms import ContactUsForm

def register_routes(app, db, bcrypt):
  
# Payment Recevied
    @app.route('/received_payment/', methods=['GET'])
    @login_required
    def received_payment():
        pass

    @login_required
    def payment_received():
        pass


    @app.route('/', methods=['GET', 'POST'])
    def index():
        '''
        if current_user.is_authenticated:
            return str(current_user.username)
        else:
            return 'No User is logged in'
        '''
        return render_template('index.html')
    
    def get_date():
        current_time = datetime.now()
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = str(request.form.get('username'))
            password = request.form.get('password')
            print(len(username))
            if len(username) > 150:
                flash('Username too long. Please choose another one.')
                return redirect(url_for('signup', message="Username Too Long"))
            elif len(password) > 200:
                flash('Password too long. Please choose another one.')
                return redirect(url_for('signup', message="Password Too Long"))
            
            hashed_password = bcrypt.generate_password_hash(password)

            inputter = 'system_generated'
            date_time = get_date()

            user = User(username=username, password=hashed_password, inputter=inputter, date_time=datetime.now())

            db.session.add(user)
            try:
                db.session.commit()
            except:
                db.session.rollback()  # Rollback the session if commit fails
                flash('Username taken. Please choose another one.')
                return redirect(url_for('signup', message="User Taken"))
            
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter(User.username == username).first()

            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('input_user'))
            else:
                return 'Failed'
            
    
    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        logout_user()
        return redirect(url_for('index'))
    

    @app.route('/secrets')
    @login_required
    def secrets():

        '''
        if current_user.role == 'admin':
            return 'My secret message!'
        else:
            return 'No Permission'
        '''
        return 'My secret message!'
    

    @app.route('/us_contact', methods=['GET'])
    def us_contact():
        return render_template('contact_us.html')


    @app.route('/get_confirmation', methods=['GET', 'POST'])
    def get_confirmation():
        if request.method == 'GET':
           email = request.args.get('email')
           type = request.args.get('type')
           mic = request.args.get('mic')
           print('mic mic mic mic: ', mic)
           print('type: ', type)
           return render_template('confirmation.html', email=email, mic=mic, type=type)
        
        elif request.method == 'POST':
            confirm = request.form.get('confirm')
            email = request.args.get('email')
            type = request.args.get('type')
            mic = request.args.get('mic')
            print('get_confirmation email: ', email)
            verification = VerificationEmail.query.filter(VerificationEmail.email == email).first()
            if int(confirm) == int(verification.verification_test):
                
                verification.verified = 1
                try:
                    db.session.commit()
                    if type == 'download':
                        return redirect(url_for('Download_music_payment', email=email, type=type, mic=mic))
                    else:
                        flash('Email Confirmed. Someone will contact you asap. Thank You')
                        return redirect(url_for('contact_us'))

                except Exception as e:
                    db.session.rollback()  # Rollback the session if commit fails
                    flash('An error occurred. Please try again.')
                    return redirect(url_for('contact_us'))
            else:
                flash('Incorrect number please retry. Thank You')
                return redirect(url_for('get_confirmation', email=email, type=type, mic=mic))
                


    @app.route('/contact_us', methods=['GET', 'POST'])
    def contact_us():
        #form = ContactUsForm()
       # if form.validate_on_submit():
        if request.method == 'GET':
            return redirect(url_for('us_contact'))
        elif request.method == 'POST':
            email = request.form.get('email')
            body = request.form.get('message')
            type = request.form.get('type')
            mic = request.form.get('mic')
            print('contact_us email: ', email)

            verify = VerificationEmail.query.filter(VerificationEmail.email == email).first()
            print('verify verify :', verify)
            if verify:
                if verify.verified == 1:
                    # Download email check
                    if type == 'download':
                        music = Music.query.filter(Music.mic==mic).order_by(Music.mic.desc()).first()
                        inputter = 'download'
                        body = 'Item Downloaded: ' + str(music.name)
                    else:
                        inputter = 'incoming'

                    email_db = SendEmail(email=email, body=body, inputter=inputter)

                    db.session.add(email_db)
                    try:
                        db.session.commit()
                        if type == 'download':
                            return redirect(url_for('Download_music_payment', email=email, type=type, mic=mic))
                        else:
                            flash('You will be contacted asap. Thank you.')
                            return redirect(url_for('contact_us'))
                        
                    
                    except Exception as e:
                        db.session.rollback()  # Rollback the session if commit fails
                        flash('An error occurred. Please try again.')
                        return redirect(url_for('contact_us'))

                if not verify.verification_test:
                    verify.verification_test = 0
                #
                #
                # Check the time for 10 minutes
                if verify.verification_test <= 1:
                    # Resend email with db_email.verification_test 

                    flash('Please see your email for resent confirmation Number if')
                    return redirect(url_for('get_confirmation', message="Confirm Email", sid=email, type=type, mic=mic))
                else:
                    # Generate 4 digit
                    y = 1234
                    # Send email to user

                    # Save to DB
                    if verify.inputter != 'incoming':
                        verify.inputter = 'incoming'

                    verify.verification_test=y

                    try:
                        db.session.commit()
                        flash('Please see your email for resent confirmation Number else')
                        return redirect(url_for('get_confirmation', message="Confirm Email", email=email, type=type, mic=mic))
                    
                    except Exception as e:
                        print('error: ', e)
                        db.session.rollback()  # Rollback the session if commit fails
                        flash('An error occurred1. Please try again.')
                        return redirect(url_for('contact_us'))
            else:
                # Generate 4 digit
                y = 1234
                # Send email to user

                # Save to DB
                if type == 'download':
                    music = Music.query.filter(Music.mic==mic).order_by(Music.mic.desc()).first()
                    inputter = 'download'
                    body = 'Item downloaded: ' + str(music.name)
                else :
                    inputter = 'incoming'

                verify =  VerificationEmail(email=email, verification_test=y, inputter=inputter)
                emails = SendEmail(email=email, body=body, inputter=inputter)

                db.session.add(verify)
                db.session.add(emails)
                try:
                    db.session.commit()
                    if type == 'download':

                        flash('Please see your email for confirmation Number')
                        return redirect(url_for('get_confirmation', message="Confirm Email", email=email, type=type, mic=mic))
                    else: 
                        flash('Please see your email for confirmation Number')
                        return redirect(url_for('get_confirmation', message="Confirm Email", email=email, type=type, mic=mic))
                    
                except Exception as e:
                    db.session.rollback()  # Rollback the session if commit fails
                    flash('An error occurred2. Please try again.')
                    return redirect(url_for('contact_us'))
                


               

    @app.route('/media')
    def media():
        user = current_user
        #user = User.query.filter_by(uid=user.uid).order_by(User.uid.desc()).first()
        
        music = Music.query.filter(Music.publish == 1).all()
        music_playlist = Music.query.filter(and_(Music.playlist != "", Music.publish == 1)).all()
        unique_playlists = set(music.playlist for music in music_playlist)
        
        most_downloaded = Music.query.filter(and_(Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_downloaded = Music.query.filter(and_(Music.downloaded > 0)).order_by(Music.downloaded.desc()).limit(10).all()
        most_played = Music.query.filter(and_(Music.played > 0)).order_by(Music.played.desc()).limit(10).all()
        #date calculation for 1 month or week. 
        latest_release_music = Music.query.filter().order_by(Music.played.desc()).limit(100).all()
        return render_template('media.html', 
                               latest_release_music=latest_release_music,
                               unique_playlists=unique_playlists,
                               music=music,  
                               user=user, 
                               most_downloaded=most_downloaded,
                               most_played=most_played)

                                                    
    @app.route('/search/', methods=['GET'])
    def search():
        if request.method == 'GET':
            pass
    

 # Emails ####

    @app.route('/asnd_email_sort_choice/', methods=['GET'])
    def asnd_email_sort_choice():
        user = current_user
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        print('asnd_email_sort_choice')
        sorted_music = EmailGroup.query.order_by(EmailGroup.email.asc()).all()
        asnd_dsnd = 'Asnd'
        my_sort_choice = 'Email'
        return render_template('music/sort_files/group_emails/emails_list.html', 
                    music=sorted_music,  
                    user=user, 
                    most_downloaded=most_downloaded,
                    most_played=most_played,
                    unpublished=unpublished,
                    order_by=asnd_dsnd,
                    sort_by=my_sort_choice)
    

    @app.route('/dsnd_email_sort_choice/', methods=['GET'])
    def dsnd_email_sort_choice():
        user = current_user
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        print('dsnd_email_sort_choice')
        sorted_music = EmailGroup.query.order_by(EmailGroup.email.desc()).all()
        asnd_dsnd = 'Dsnd'
        my_sort_choice = 'Email'
        return render_template('music/sort_files/group_emails/emails_list.html', 
                    music=sorted_music,  
                    user=user, 
                    most_downloaded=most_downloaded,
                    most_played=most_played,
                    unpublished=unpublished,
                    order_by=asnd_dsnd,
                    sort_by=my_sort_choice
                        )
    
    @app.route('/asnd_email_group_sort_choice/', methods=['GET'])
    @login_required
    def asnd_email_group_sort_choice():
        
        user = current_user
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        print('asnd_email_sort_choice')
        sorted_music = EmailGroup.query.order_by(EmailGroup.email_group.asc()).all()
        asnd_dsnd = 'Asnd'
        my_sort_choice = 'Group Emails'
        return render_template('music/sort_files/group_emails/emails_list.html', 
                    music=sorted_music,  
                    user=user, 
                    most_downloaded=most_downloaded,
                    most_played=most_played,
                    unpublished=unpublished,
                    order_by=asnd_dsnd,
                    sort_by=my_sort_choice)


    @app.route('/music_report_sort/', methods=['GET'])
    @login_required
    def music_report_sort():
        asnd_dsnd = request.args.get('asnd_dsnd')
        my_sort_choice = request.args.get('my_sort_choice')
        user = current_user
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        sorted_music = EmailGroup.query.order_by(EmailGroup.email_group.desc()).all()
        
        if asnd_dsnd == 'asnd' and my_sort_choice == 'name':
            sorted_music = Music.query.order_by(Music.name.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Name'

            
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'name':
            sorted_music = Music.query.order_by(Music.name.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Name'
            
        elif asnd_dsnd == 'asnd' and my_sort_choice == 'playlist':
            sorted_music = Music.query.order_by(Music.playlist.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Playlist'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'playlist':
            sorted_music = Music.query.order_by(Music.playlist.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Playlist'
            
        elif asnd_dsnd == 'asnd' and my_sort_choice == 'featured_artist':
            sorted_music = Music.query.order_by(Music.featuring_name.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Featured'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'featured_artist':
            sorted_music = Music.query.order_by(Music.featuring_name.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Featured'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'price':
            sorted_music = Music.query.order_by(Music.price.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Price'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'price':
            sorted_music = Music.query.order_by(Music.price.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Price'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'download':
            sorted_music = Music.query.order_by(Music.downloaded.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Downloads'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'download':
            sorted_music = Music.query.order_by(Music.downloaded.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Downloads'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'bpm':
            sorted_music = Music.query.order_by(Music.bpm.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'BPM'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'bpm':
            sorted_music = Music.query.order_by(Music.bpm.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'BPM'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'key':
            sorted_music = Music.query.order_by(Music.key.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Key'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'key':
            sorted_music = Music.query.order_by(Music.key.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Key'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'mood':
            sorted_music = Music.query.order_by(Music.mood.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Mood'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'mood':
            sorted_music = Music.query.order_by(Music.mood.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Mood'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'instrument':
            sorted_music = Music.query.order_by(Music.instrument.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Instruments'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'instrument':
            sorted_music = Music.query.order_by(Music.instrument.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Instruments'
        else:
            return 'Choice not found'
        
        return render_template('music/music_report.html', 
                        music=sorted_music,  
                        user=user, 
                        most_downloaded=most_downloaded,
                        most_played=most_played,
                        unpublished=unpublished,
                        order_by=asnd_dsnd,
                        sort_by=my_sort_choice
                            )
    

#end redirects

    @app.route('/sort_choice/', methods=['GET', 'POST'])
    @login_required
    def sort_choice():
        if request.method == 'POST':
            asnd_dsnd = request.form.get('asnd_dsnd')
            my_sort_choice = request.form.get('sort_choice')
            if not asnd_dsnd:
                asnd_dsnd = 'asnd'
            if not my_sort_choice:
                my_sort_choice = 'name'

            return redirect(url_for('music_report_sort', asnd_dsnd=asnd_dsnd, my_sort_choice=my_sort_choice))
          
        else:
            asnd_dsnd = request.form.get('asnd_dsnd')
            my_sort_choice = request.form.get('sort_choice')

            user = current_user
            most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
            most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
            unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
            

            sorted_music = Music.query.order_by(Music.name.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Name'
            return render_template('music/music_report.html', 
                        music=sorted_music,  
                        user=user, 
                        most_downloaded=most_downloaded,
                        most_played=most_played,
                        unpublished=unpublished,
                        order_by=asnd_dsnd,
                        sort_by=my_sort_choice
                            )
            
    
    @app.route('/def_email_sort_choice/', methods=['POST'])
    @login_required
    def def_email_sort_choice():
        asnd_dsnd = request.form.get('asnd_dsnd')
        sort_choice = request.form.get('sort_choice')
        print('asnd_dsnd', asnd_dsnd)
        print('sort_choice', sort_choice)
        if asnd_dsnd == 'asnd' and sort_choice == 'email':
            return redirect(url_for('asnd_email_sort_choice'))
        elif asnd_dsnd == 'dsnd' and sort_choice == 'email':
            return redirect(url_for('dsnd_email_sort_choice'))
        elif asnd_dsnd == 'asnd' and sort_choice == 'email_group':
            return redirect(url_for('asnd_email_group_sort_choice'))
        elif asnd_dsnd == 'dsnd' and sort_choice == 'email_group':
            return redirect(url_for('dsnd_email_group_sort_choice'))
        else:
            print(' else email_sort_choice ')
            return redirect(url_for('dsnd_playlist_sort_choice'))

    @app.route('/finance_report_sort/', methods=['GET'])
    @login_required
    def finance_report_sort():
        asnd_dsnd = request.args.get('asnd_dsnd')
        my_sort_choice = request.args.get('my_sort_choice')
        user = current_user
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        sorted_music = EmailGroup.query.order_by(EmailGroup.email_group.desc()).all()
        
        if asnd_dsnd == 'asnd' and my_sort_choice == 'name':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.name.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Name'

            
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'name':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.name.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Name'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'price':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.price.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Price'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'price':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.price.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Price'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'download':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.download_number.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Downloads'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'download':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.download_number.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Downloads'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'bpm':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.bpm.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'BPM'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'bpm':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.bpm.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'BPM'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'key':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.key.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Key'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'key':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.key.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Key'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'mood':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.mood.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Mood'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'mood':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.mood.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Mood'

        elif asnd_dsnd == 'asnd' and my_sort_choice == 'instrument':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.instrument.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Instruments'
        elif asnd_dsnd == 'dsnd' and my_sort_choice == 'instrument':
            sorted_music = PaymentReceived.query.order_by(PaymentReceived.instrument.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Instruments'
        else:
            return 'Choice not found'
        
        return render_template('finance/payment_received_report.html', 
                        music=sorted_music,  
                        user=user, 
                        most_downloaded=most_downloaded,
                        most_played=most_played,
                        unpublished=unpublished,
                        order_by=asnd_dsnd,
                        sort_by=my_sort_choice
                            )
    
    @app.route('/sort_choice_finance/', methods=['GET', 'POST'])
    @login_required
    def sort_choice_finance():
        if request.method == 'POST':
            asnd_dsnd = request.form.get('asnd_dsnd')
            my_sort_choice = request.form.get('sort_choice')
            if not asnd_dsnd:
                asnd_dsnd = 'asnd'
            if not my_sort_choice:
                my_sort_choice = 'name'

            return redirect(url_for('finance_report_sort', asnd_dsnd=asnd_dsnd, my_sort_choice=my_sort_choice))
          
        else:
            asnd_dsnd = request.form.get('asnd_dsnd')
            my_sort_choice = request.form.get('sort_choice')

            user = current_user
            most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
            most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
            unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
            

            sorted_music = Music.query.order_by(Music.name.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Name'
            return render_template('music/music_report.html', 
                        music=sorted_music,  
                        user=user, 
                        most_downloaded=most_downloaded,
                        most_played=most_played,
                        unpublished=unpublished,
                        order_by=asnd_dsnd,
                        sort_by=my_sort_choice
                            )
        
    @app.route('/name_song_asnd', methods=['GET'])
    @login_required
    def name_song_asnd():
    
        sorted_music = Music.query.order_by(Music.name.asc()).all()
        user = current_user
        music = Music.query.order_by(Music.name.asc()).all()
        print('music name_song_asnd: ', music)
    # most_downloaded = Music.query.filter(Music.user_id == user.uid).rder_by(Music.downloaded.desc()).all()
       
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        print('before return')
        #flash('select_asnd_dsnd')
        return render_template('music/sort_files/asnd_song_name.html', 
                            music=music,  
                            user=user, 
                            most_downloaded=most_downloaded,
                            most_played=most_played,
                            unpublished=unpublished,
                                )
        

    @app.route('/asnd_song_name/<pid>', methods=['GET'])
    @login_required
    def asnd_song_name(pid):
        if pid == 'asnd':
            return redirect(url_for('name_song_asnd'))
        elif pid == 'dsnd':
            return redirect(url_for('name_song_dsnd'))
        

    @app.route('/input_music')
    @login_required
    def input_music():
        user = current_user
        print('user input_music current user = ', user)

        music = Music.query.filter(Music.user_id == user.uid).all()
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()

        playlist =Music.query.filter(Music.playlist != "").all()
        unique = set(playlist.playlist for playlist in playlist)

        return render_template('music/music_input.html', 
                               unique_playlist=unique,
                               music=music,  
                               user=user, 
                               most_downloaded=most_downloaded,
                               most_played=most_played)
    
    
    @app.route('/input_user', methods=['GET', 'POST'])
    @login_required
    def input_user():
        if request.method == 'GET':
         user = current_user
         user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()
         music = Music.query.filter(Music.user_id == user.uid).all()
         most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
         most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
         unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
         return render_template('user/user_input.html', 
                               music=music,  
                               user=user, 
                               most_downloaded=most_downloaded,
                               most_played=most_played,
                               unpublished=unpublished)
        
        elif request.method == "POST":
            display_name = request.form.get('display_name')
            role = request.form.get('role')
            profile_img = request.files['profile_img']
            backdrop_image = request.files['backdrop']

            user = current_user
            user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()

            profile_img_url = None
            if profile_img:
                filename = secure_filename(profile_img.filename)
                profile_img_url = app.config['UPLOAD_FOLDER']+"/"+ user.username+"/"+filename
                filepath = os.path.join("static", app.config['UPLOAD_FOLDER'], user.username, filename)
                user_folder = os.path.join("static", app.config['UPLOAD_FOLDER'], current_user.username)
                # Ensure the directory exists
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                profile_img.save(filepath)

            backdrop_image_url = None
            if backdrop_image:
                filename = secure_filename(backdrop_image.filename)
                backdrop_image_url = app.config['UPLOAD_FOLDER']+"/"+ user.username+"/"+filename
                filepath = os.path.join("static", app.config['UPLOAD_FOLDER'], user.username, filename)
                user_folder = os.path.join("static", app.config['UPLOAD_FOLDER'], current_user.username)
                # Ensure the directory exists
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                backdrop_image.save(filepath)

            if display_name:
                user.display_name = display_name

            if role:
                user.role = role

            if profile_img_url:
                user.profile_image = profile_img_url

            if backdrop_image_url:
                user.backdrop_image = backdrop_image_url

            user.inputter = user.username

            db.session.commit()

        return redirect(url_for('input_music'))


    @app.route('/user_input')
    @login_required
    def user_input():
        return redirect(url_for('input_music'))        
   

    @app.route('/report_music')
    @login_required
    def report_music():
        user = current_user
        music = Music.query.filter(Music.user_id == user.uid).all()

       # most_downloaded = Music.query.filter(Music.user_id == user.uid).rder_by(Music.downloaded.desc()).all()
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        return render_template('music/music_report.html', 
                               music=music,  
                               user=user, 
                               most_downloaded=most_downloaded,
                               most_played=most_played,
                               unpublished=unpublished)

    @app.route('/music_input/', methods=['GET', 'POST'])
    @login_required
    def music_input():
        '''
        if current_user.role == 'admin':
            return 'My secret message!'
        else:
            return 'No Permission'
        
        return 'My secret message!'
        '''

        if request.method == 'GET':
            return redirect(url_for('input_music'))
        elif request.method == "POST":
            name = request.form.get('name')
            featuring_name = request.form.get('featuring_name')
            playlist = request.form.get('playlist')
            playlist_dropdown = request.form.get('playlist_dropdown')
            if playlist_dropdown:
                playlist = playlist_dropdown

            price = request.form.get('price')
            bpm = request.form.get('bpm')
            key = request.form.get('key')
            mood = request.form.get('mood')
            instrument = request.form.get('instrument')
            image = request.files['img_upload']
            music_upload = request.files['music_upload']
            featuring_image_dir = request.files['featuring_image']
            bulk_upload = request.files.getlist('folder')
            
            # Messages
           # if bulk_upload == '' and music_upload == '':
           #     print('I am inside here!!!')
           #     flash('Upload either music file or select a folder for bulk upload. Please choose one.')
           #     return redirect(url_for('signup', message="User Taken"))

            user = current_user
            user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()
            
            if bulk_upload:
                for upload in bulk_upload:
                    if upload:
                        filename = secure_filename(upload.filename)
                        music_url = "music/music/"+ user.username+"/"+filename
                        filepath = os.path.join("static", "music","music" , user.username, filename)
                        user_folder = os.path.join("static", "music", "music", user.username)
                    
                        # Ensure the directory exists
                        if not os.path.exists(user_folder):
                            os.makedirs(user_folder)
                        
                        upload.save(filepath)

                        if name:
                            name = name
                        else:
                            name = filename

                        if (name or music_url or image_url or featuring_name or featuring_music_url ):
                            music_details = Music(name=name, 
                                                file=music_url, 
                                                user_id=user.uid,
                                                date_time=datetime.now(),
                                                playlist=playlist,
                                                price=price,
                                                inputter=user.username,
                                                bpm=bpm,
                                                key=key,
                                                mood=mood,
                                                instrument=instrument)

                        if upload:
                            db.session.add(music_details)
                if upload:
                    db.session.commit()
                    return redirect(url_for('report_music'))

            image_url = None
            if image:
                filename = secure_filename(image.filename)
                image_url = "music/img/"+ user.username+"/"+filename
                filepath = os.path.join("static", 'music/img/' , user.username, filename)
                user_folder = os.path.join("static", 'music/img/', current_user.username)
            
                # Ensure the directory exists
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                
                image.save(filepath)

            music_url = None
            if music_upload:
                filename = secure_filename(music_upload.filename)
                if not name:
                    name = filename
                music_url = "music/music/"+ user.username+"/"+filename
                filepath = os.path.join("static", 'music/music/' , user.username, filename)
                user_folder = os.path.join("static", 'music/music/', current_user.username)
            
                # Ensure the directory exists
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                
                music_upload.save(filepath)
            
            featuring_music_url = None
            if featuring_image_dir:
                filename = secure_filename(featuring_image_dir.filename)
                featuring_music_url = "music/featured"+ user.username+"/"+filename
                filepath = os.path.join("static", 'music/featured' , user.username, filename)
                featuring_user_folder = os.path.join("static", 'music/featured', current_user.username)
            
                # Ensure the directory exists
                if not os.path.exists(featuring_user_folder):
                    os.makedirs(featuring_user_folder)
                
                music_upload.save(filepath)

            if name:
                name = name

            if name or music_url or image_url or featuring_name or featuring_music_url:
                music_details = Music(name=name, 
                                    file=music_url, 
                                    image=image_url,
                                    featuring_name=featuring_name,
                                    featuring_image_dir=featuring_music_url,
                                    user_id=user.uid,
                                    playlist=playlist,
                                    price=price,
                                    date_time=datetime.now(),
                                    inputter=user.username,
                                    bpm=bpm,
                                    key=key,
                                    mood=mood,
                                    instrument=instrument)

                db.session.add(music_details)
                db.session.commit()
        print('input')
        return redirect(url_for('report_music'))
    

    @app.route('/publish_input/<pid>', methods=['GET'])
    @login_required
    def publish_input(pid):
        print('publish pid', pid)
        user = current_user
        music = Music.query.filter(Music.mic == pid).first()
        print('music.publish', music.publish)
        if music.publish != 1:
            music.publish = 1
        else:
            music.publish = 0

        db.session.commit()
        return redirect(url_for('report_music'))


    @app.route('/music_edit/<pid>', methods=['GET', 'POST'])
    @login_required
    def music_edit(pid):
        if request.method == 'GET':
            music_edit = Music.query.filter(Music.mic == pid).order_by(Music.mic.desc()).first()
            user = current_user

            music = Music.query.filter(Music.user_id == user.uid).all()
            playlist =Music.query.filter(Music.playlist != "").all()
            unique = set(playlist.playlist for playlist in playlist)
            return render_template('music/music_edit.html',
                                    unique_playlist = unique,
                                    edit_music = music_edit,
                                    music=music,  
                                    user=user)
        
        elif request.method == 'POST':

            name = request.form.get('name')
            featuring_name = request.form.get('featuring_name')
            playlist = request.form.get('playlist')
            playlist_dropdown = request.form.get('playlist_dropdown')
            if playlist_dropdown:
                playlist = playlist_dropdown
                
            price = request.form.get('price')
            bpm = request.form.get('bpm')
            key = request.form.get('key')
            mood = request.form.get('mood')
            instrument = request.form.get('instrument')
            image = request.files['img_upload']
            music_upload = None
            featuring_image_dir = request.files['featuring_image']
            bulk_upload = request.files.getlist('folder')

            music_edit = Music.query.filter(Music.mic == pid).order_by(Music.mic.desc()).first()

            user = User.query.filter_by(uid=music_edit.user_id).order_by(User.uid.desc()).first()

            image_url = None
            if image:
                filename = secure_filename(image.filename)
                image_url = "music/img/"+ user.username+"/"+filename
                filename = os.path.join("static", 'music/img/' , user.username, filename)
                user_folder = os.path.join("static", 'music/img/', current_user.username)
            
                # Ensure the directory exists
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                
                image.save(filename)

            music_url = None
            if music_upload:
                filename = secure_filename(music_upload.filename)
                music_url = "music/music/"+ user.username+"/"+filename
                filename = os.path.join("static", 'music/music/' , user.username, filename)
                user_folder = os.path.join("static", 'music/music/', current_user.username)
            
                # Ensure the directory exists
                if not os.path.exists(user_folder):
                    os.makedirs(user_folder)
                
                music_upload.save(filename)
            
            featuring_image_url = None
            if featuring_image_dir:
                filename = secure_filename(featuring_image_dir.filename)
                featuring_image_url = "music/featured"+ user.username+"/"+filename
                filename = os.path.join("static", 'music/featured' , user.username, filename)
                featuring_user_folder = os.path.join("static", 'music/featured', current_user.username)
            
                # Ensure the directory exists
                if not os.path.exists(featuring_user_folder):
                    os.makedirs(featuring_user_folder)
                
                featuring_image_dir.save(filename)

            music = Music.query.filter(Music.mic == pid).order_by(Music.mic.desc()).first()
            
            if name:
             music.name = name

            if image:
             music.image = image_url

            if music_upload:
             music.file = music_url

            if featuring_name:
             music.featuring_name = featuring_name

            if featuring_image_dir:
             music.featuring_image_dir = featuring_image_url

            if price:
             music.price = price

            if playlist:
             music.playlist = playlist

            if bpm:
               music.bpm = bpm
            
            if key:
               music.key = key

            if mood:
               music.mood = mood

            if instrument:
               music.instrument = instrument

            music.inputter = user.username
            music.date_time = datetime.now()

            db.session.commit()

            user = current_user

            print('okay it there')
            return redirect(url_for('report_music'))


    @app.route('/music_delete/<pid>')
    @login_required
    def music_delete(pid):
        
        Music.query.filter(Music.mic == pid).delete() 
        db.session.commit()

        return redirect(url_for('report_music'))
    

# PLAY AND DOWNLOAD and ADD LIST
    @app.route('/play_music/<pid>', methods=['POST'])
    @login_required
    def play_music(pid):
        user = current_user
        music= Music.query.filter(Music.mic == pid).first()
        music_played = music.played
        if not music_played:
            music.played = 1
        else:
            music.played = music.played + 1
        
        music.inputter = user.username
        music.date_time = datetime.now()
        db.session.commit()

        user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()       
        music = Music.query.filter(Music.user_id == user.uid).all()
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        return render_template('media.html', 
                               music=music,  
                               user=user, 
                               most_downloaded=most_downloaded,
                               most_played=most_played)


    @app.route('/Download_music_payment/', methods=['GET'])
    @login_required
    def Download_music_payment():
        email = request.args.get('email')
        mic = request.args.get('mic')
        type = request.args.get('type')
        print('Download_music_payment email: ', email)
        music = Music.query.filter(Music.mic == mic).order_by(Music.mic.desc()).first()
        #email = email.sid
       # email = SendEmail.query.filter(SendEmail.sid == email).first()
        print('mic: ', mic)
        print('email before: ', email)
        price = music.price

        if price <= 0 :
            music_played = music.downloaded
            if not music_played:
                music.downloaded = 1
            else:
                music.downloaded = music.downloaded + 1
            
            music.inputter = 'downloaded'
            
            payment_received = PaymentReceived(email=email,
                                               music=mic,
                                               download_number=music.downloaded, 
                                               name=music.name,
                                               image=music.image,
                                               file=music.file,
                                               price=price,
                                               bpm=music.bpm,
                                               key=music.key,
                                               mood=music.mood,
                                               instrument=music.instrument,
                                               inputter='download')
            db.session.add(payment_received)

            try:    
                db.session.commit()
                # download song here to user maybe javascript or python

                # send email with attachements
                
                flash('Please find song and documentation in your inbox')
                return redirect(url_for('media'))
            
            except Exception as e:
                print("error: ", e)
                db.session.rollback()  # Rollback the session if commit fails
                flash('An error occurred. Please try again.')
                return redirect(url_for('media'))
        
        else:
            # fast Pay Here
            return 'Pay Fast'
        
        # Response from Fast pay


    @app.route('/download_music/<pid>', methods=['GET', 'POST'])
    @login_required
    def download_music(pid):
        if request.method == 'GET':
           # print('I really dont know whats yp: ', pid)
            return render_template('download_verify.html', mic=pid)
        
        elif request.method == 'POST':
            
            user = current_user
            music= Music.query.filter(Music.mic == pid).first()
            # check registered email in contact_us
            verified_email = contact_us()
            
            # update downloaded field in music module
            music_played = music.downloaded
            if not music_played:
                music.downloaded = 1
            else:
                music.downloaded = music.downloaded + 1
            
            music.inputter = user.username      

            db.session.commit()
            user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()
            music = Music.query.filter(Music.user_id == user.uid).all()
            most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
            most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
            return render_template('media.html', 
                                music=music,  
                                user=user, 
                                most_downloaded=most_downloaded,
                                most_played=most_played)
    
#
# Email  
    @app.route('/email_edit/<pid>', methods=['GET', 'POST'])
    @login_required
    def email_edit(pid):
        if request.method == 'GET':
            #return redirect(url_for('edit_email'))
            email = SendEmail.query.filter(SendEmail.sid==pid).first()
            user = current_user
            user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()
            music = Music.query.filter(Music.user_id == user.uid).all()
            group = SendEmail.query.filter(SendEmail.email_group != "").all()
            unique_group = set(group.email_group for group in group)
            sorted_email = SendEmail.query.order_by(SendEmail.date_time.desc()).all()
       
            return render_template('email/email_edit.html', 
                                music=music,  
                                user=user, 
                                email=email,
                                email_group=sorted_email,
                                unique_group=unique_group
                                )
        
        elif request.method == 'POST':
            email_group1 = request.form.get('email_group')
            email = request.form.get('email')
            email_group = SendEmail.query.filter(SendEmail.sid == pid).first()
            email_group.email_group = email_group1
            email_group.email = email
            email_group.inputter = current_user.username
            db.session.commit()
            return redirect(url_for('email_report'))
        else:
            return "System Error: "


    @app.route('/email_delete/<pid>')
    @login_required
    def email_delete(pid):
        
        SendEmail.query.filter(SendEmail.sid == pid).delete() 
        db.session.commit()

        return redirect(url_for('report_email'))


    @app.route('/report_email/', methods=['GET'])
    @login_required
    def report_email():
        user = current_user
        user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        email_group = SendEmail.query.filter().all()

        return render_template('email/email_report.html', 
                               email=email_group,  
                               user=user, 
                               most_downloaded=most_downloaded,
                               most_played=most_played,
                               email_group=email_group)


    @app.route('/email_report/', methods=['GET'])
    @login_required
    def email_report():
        return redirect(url_for('report_email'))
    
# Send Email
    @app.route('/input_email/', methods=['GET'])
    @login_required
    def input_email():
        user = current_user
        user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()
        group = SendEmail.query.filter(SendEmail.email_group != "").all()
        unique_group = set(group.email_group for group in group)

        email_group = SendEmail.query.filter().all()
        return render_template('email/email_input.html', 
                               email=email_group,  
                               user=user, 
                               unique_group=unique_group,
                               email_group=email_group)


    @app.route('/email_input/', methods=['GET', 'POST'])
    @login_required
    def email_input():
        if request.method == 'GET':
         return redirect(url_for('input_email'))
        
        elif request.method == 'POST':
            email_group = request.form.get('email_group')
            email = request.form.get('email')
            topic = request.form.get('topic')
            body = request.form.get('body')
            inputter = current_user.username
            attachement = None
            # Add all the gmail calls here...

            send_sms = SendEmail(email_group=email_group,
                                 email=email,
                                 topic=topic,
                                 body=body,
                                 attachement=attachement,
                                 inputter=inputter)
            db.session.add(send_sms)
            db.session.commit()

            return redirect(url_for('email_report'))
        

# Send Emails
    @app.route('/sort_choice_email/', methods=['GET'])
    @login_required
    def sort_choice_email():
        user = current_user

        asnd_dsnd = request.args.get('asnd_dsnd')
        sort_choice = request.args.get('sort_choice')

        if asnd_dsnd == 'asnd' and sort_choice == 'email':
            sorted_music = SendEmail.query.order_by(SendEmail.email.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Email'
        elif asnd_dsnd == 'dsnd' and sort_choice == 'email':
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Email'
            sorted_music = SendEmail.query.order_by(SendEmail.email.desc()).all()
        elif asnd_dsnd == 'asnd' and sort_choice == 'email_group':
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Group'
            sorted_music = SendEmail.query.order_by(SendEmail.email_group.asc()).all()
        elif asnd_dsnd == 'dsnd' and sort_choice == 'email_group':
            sorted_music = SendEmail.query.order_by(SendEmail.email_group.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Group'
        elif asnd_dsnd == 'asnd' and sort_choice == 'topic':
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Subject'
            sorted_music = SendEmail.query.order_by(SendEmail.topic.asc()).all()
        elif asnd_dsnd == 'dsnd' and sort_choice == 'topic':
            sorted_music = SendEmail.query.order_by(SendEmail.topic.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Subject'
        elif asnd_dsnd == 'asnd' and sort_choice == 'date':
            sorted_music = SendEmail.query.order_by(SendEmail.date_time.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Date'
        elif asnd_dsnd == 'dsnd' and sort_choice == 'date':
            sorted_music = SendEmail.query.order_by(SendEmail.date_time.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Date'
        elif asnd_dsnd == 'asnd' and sort_choice == 'type':
            sorted_music = SendEmail.query.order_by(SendEmail.inputter.asc()).all()
            asnd_dsnd = 'Asnd'
            my_sort_choice = 'Type'
        elif asnd_dsnd == 'dsnd' and sort_choice == 'type':
            sorted_music = SendEmail.query.order_by(SendEmail.inputter.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Type'

        
        else:
            sorted_music = SendEmail.query.order_by(SendEmail.date_time.desc()).all()
            asnd_dsnd = 'Dsnd'
            my_sort_choice = 'Date'

        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        user = User.query.filter_by(username=user.username).order_by(User.uid.desc()).first()
        group = SendEmail.query.filter(SendEmail.email_group != "").all()
        unique_group = set(group.email_group for group in group)
        email_group = SendEmail.query.order_by(SendEmail.date_time.desc()).all()
        return render_template('email/email_report.html', 
                    email=sorted_music,  
                    user=user, 
                    most_downloaded=most_downloaded,
                    most_played=most_played,
                    unpublished=unpublished,
                    order_by=asnd_dsnd,
                    sort_by=my_sort_choice,
                    unique_group=unique_group,
                    email_group=email_group
                        )

    @app.route('/email_sort_choice/', methods=['GET', 'POST'])
    @login_required
    def email_sort_choice():
        asnd_dsnd = request.form.get('asnd_dsnd')
        sort_choice = request.form.get('sort_choice')

        return redirect(url_for('sort_choice_email', asnd_dsnd=asnd_dsnd, sort_choice=sort_choice))
    
        
    @app.route('/email_send/', methods=['GET'])
    @login_required
    def email_send():
        user = current_user
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        
        group = SendEmail.query.filter(SendEmail.email_group != "").all()
        unique_group = set(group.email_group for group in group)
        sorted_email = SendEmail.query.order_by(SendEmail.date_time.desc()).all()

        return render_template('email/email_send.html', 
                    email=sorted_email, 
                    email_group=sorted_email, 
                    user=user,
                    unique_group=unique_group,
                    most_downloaded=most_downloaded,
                    most_played=most_played
                    )


# Report finance
    @app.route('/payment_received_report/', methods=['GET'])
    @login_required
    def payment_received_report():
        payment_received_list = PaymentReceived.query.filter().all()
        user = current_user
        music = Music.query.filter(Music.user_id == user.uid).all()

       # most_downloaded = Music.query.filter(Music.user_id == user.uid).rder_by(Music.downloaded.desc()).all()
        most_downloaded = Music.query.filter(and_(Music.user_id == user.uid, Music.downloaded > 0)).order_by(Music.downloaded.desc()).all()
        most_played = Music.query.filter(and_(Music.user_id == user.uid, Music.played > 0)).order_by(Music.played.desc()).all()
        unpublished = Music.query.filter(and_(Music.user_id == user.uid, Music.publish == 0)).order_by(Music.mic.desc()).all()
        return render_template('finance/payment_received_report.html', 
                               music=payment_received_list,  
                               user=user, 
                               most_downloaded=most_downloaded,
                               most_played=most_played,
                               unpublished=unpublished)
 