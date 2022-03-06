from flask_app import app, session
from flask import render_template, redirect, request
from flask_app.config.helper import login_required
from flask_app.models.user import User
import os

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.post('/register')
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    user_id = User.create_user(request.form)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.post('/login')
def login():
    user_status = User.validate_login(request.form)
    if not user_status:
        return redirect('/')
    session['user_id'] = user_status.id
    return redirect('/dashboard')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user = User.retrieve_one(id=session['user_id']))

@app.route('/profile/edit/<int:id>')
@login_required
def edit_profile(id):
    return render_template('edit_profile.html', user = User.retrieve_one(id=id))

@app.post('/profile/update/<int:id>')
@login_required
def update_profile(id):
    print(request.files)
    avatar = request.files.get('avatar')
    if avatar:
        avatar.save(os.path.join(app.static_folder, f"img/{session['user_id']}.webp"))
    if not User.validate_update(request.form):
        return redirect(f'/profile/edit/{id}')
    data = {
      **request.form,
      'avatar': f"{session['user_id']}.webp" if avatar else "user-circle.png"
    }
    User.update(**data, id=id)
    return redirect(f'/profile/{id}')

@app.post('/profile/updatecover/<int:id>')
@login_required
def update_profile_cover(id):
    print(request.files)
    avatar = request.files.get('avatar')
    if avatar:
        avatar.save(os.path.join(app.static_folder, f"img/{session['user_id']}.webp"))
    cover_photo = request.files.get('cover_photo')
    if cover_photo:
        cover_photo.save(os.path.join(app.static_folder, f"img/{session['user_id']}_cover.webp"))
    if not User.validate_update(request.form):
        return redirect(f'/profile/edit/{id}')
    data = {
      **request.form,
      'cover_photo': f"{session['user_id']}_cover.webp" if cover_photo else "default-cover.jpg"
    }
    User.update(**data, id=id)
    return redirect(f'/profile/{id}')

@app.route('/profile/<int:id>')
@login_required
def view_profile(id):
    followers = User.retrieve_all(id=id)
    follower_count = 0
    for row in range(len(followers)):
        follower_count += row
    return render_template('profile.html', user = User.retrieve_one(id=id), follower_count = follower_count)

@app.route('/profile/friends/<int:id>')
@login_required
def view_friends(id):    
    return render_template('friends.html', followers = User.retrieve_all(id=id))

@app.route('/user/delete/<int:id>')
@login_required
def delete(id):
    User.delete(id=id) 
    return redirect('/users')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')