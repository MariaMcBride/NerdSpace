from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from datetime import date, datetime
from flask_app import DB, bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.dob = data['dob']
        self.avatar = data['avatar']
        self.cover_photo = data['cover_photo']
        self.bio = data['bio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def age(self):
        return User.get_age(self.dob)

    @staticmethod
    def get_age(born):
        print("test", born)
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @property
    def followers(self):
        return self.retrieve_all(followeduser_id = self.id)

# ---------- CRUD ---------- #

    @classmethod # CREATE
    def create_user(cls, data):
        query = f'''INSERT into `users` 
        ({", ".join(f"`{key}`" for key in data)}) 
        VALUES 
        ({", ".join(f"%({key})s" for key in data)});'''
        data = {
            **data,
            'password': bcrypt.generate_password_hash(data['password'])
        }
        user_id = connectToMySQL(DB).query_db(query, data)
        return user_id

    @classmethod # READ ONE 
    def retrieve_one(cls, **data):
        query = f'''SELECT * FROM `users` WHERE 
        {" AND ".join(f"`{key}` = %({key})s" for key in data)};'''
        result = connectToMySQL(DB).query_db(query, data)
        if result: 
            return cls( result[0] ) 

    @classmethod
    def retrieve_all(cls, **data):
        query = 'SELECT * FROM users;'
        if data:
            query = f'''SELECT followers.* FROM users AS followed
            LEFT JOIN follows ON followeduser_id = followed.id
            LEFT JOIN users AS followers ON followers.id = follower_id
            WHERE 
            {" AND ".join(f"{key} = %({key})s" for key in data)};'''
        results = connectToMySQL(DB).query_db(query, data)
        all_users = []
        if results:
            for row in results:
                all_users.append( cls(row) )
        return all_users

    @classmethod # UPDATE
    def update(cls, id = None, **data):
        query = f'''UPDATE users SET 
        {", ".join(f"{key} = %({key})s" for key in data)}
        WHERE `id`= %(id)s;'''
        data = {
            **data,
            'id': id
        }
        result = connectToMySQL(DB).query_db(query, data)
        return result

    @classmethod # DELETE
    def delete(cls, **data): 
        query = "DELETE FROM users WHERE id = %(id)s;"
        result = connectToMySQL(DB).query_db(query, data)
        return result

# ---------- VALIDATATIONS ---------- #

    @staticmethod # REGISTRATION
    def validate_user(data):
        errors = {}
        if 'first_name' in data and len(data['first_name']) < 3:
            errors['first_name'] = 'First name must be at least 3 characters.'
        elif 'first_name' in data and not data['first_name'].isalpha():
            errors['first_name'] = 'First name must contain only letters.'
        if 'last_name' in data and len(data['last_name']) < 3:
            errors['last_name'] = 'Last name must be at least 3 characters.'
        elif 'last_name' in data and not data['last_name'].isalpha():
            errors['last_name'] = 'Last name must contain only letters.'
        if 'email' in data and not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Email format is invalid.'
        elif 'email' in data and User.retrieve_one(email=data['email']):
            errors['email'] = 'Email is already in use. Please log in.'
        if 'password' in data and len(data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        elif 'confirm_password' in data and 'password' in data and data['password'] != data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match.'
        if 'dob' in data:
            if data['dob'] == '':
                errors['dob'] = 'Date cannot be blank.'
            elif User.get_age(datetime.strptime(data['dob'], "%Y-%m-%d")) < 18:
                errors['dob'] = 'You must be at least 18 years old!'
        for category, message in errors.items():
            flash(message, category)
        return len(errors) == 0
    
    @staticmethod 
    def validate_update(data):
        errors = {}
        if 'first_name' in data and len(data['first_name']) < 3:
            errors['first_name'] = 'First name must be at least 3 characters.'
        elif 'first_name' in data and not data['first_name'].isalpha():
            errors['first_name'] = 'First name must contain only letters.'
        if 'last_name' in data and len(data['last_name']) < 3:
            errors['last_name'] = 'Last name must be at least 3 characters.'
        elif 'last_name' in data and not data['last_name'].isalpha():
            errors['last_name'] = 'Last name must contain only letters.'
        if 'email' in data and not EMAIL_REGEX.match(data['email']):
            errors['email'] = 'Email format is invalid.'
        for category, message in errors.items():
            flash(message, category)
        return len(errors) == 0

    @staticmethod # LOGIN
    def validate_login(data):
        if not EMAIL_REGEX.match(data['email']):
            flash('Invalid Email/Password', 'login')
            return False
        if len(data['password']) < 8:
            flash('Invalid Email/Password', 'login')
            return False
        if not User.retrieve_one(email=data['email']):
            flash('Invalid Email/Password', 'login')
            return False        
        user_in_db = User.retrieve_one(email=data['email'])
        if not bcrypt.check_password_hash(user_in_db.password, data['password']):
            flash('Invalid Email/Password', 'login')
            return False
        return user_in_db
