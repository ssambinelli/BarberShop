from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re


class Admin:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

# User registration 
    @classmethod
    def create_admin(cls, data):
        query = """
        INSERT INTO admins (first_name, last_name, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        
        return results
    

# Get user by ID 
    @classmethod
    def get_by_id(cls,data):
        query="""
        SELECT * FROM admins WHERE id = %(id)s
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

# Check users e-mail
    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM admins WHERE email = %(email)s'
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False
    
# TO GET ALL ADMINS
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM admins 
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_admins = []
        if results:
            for row in results:
                this_admin = cls(row)
                all_admins.append(this_admin)
        return all_admins

# EDIT ADMIN 
    @classmethod
    def edit(cls, data):
        query = """
        UPDATE admins
        SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


# DELETE ADMIN 
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM admins 
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)



    @staticmethod
    def validation(data):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        # First Name 
        if (regex.search(data['first_name']) != None or len(data['first_name']) < 2):
            # first name contains special characters
            flash('First name contains special characters or does not have at least 2 characters.', "admin")
            is_valid = False
        
        # Last Name 
        if (regex.search(data['last_name'])!= None or len(data['last_name']) < 2):
            # last name contains special characters
            flash('Last name contains special characters or does not have at least 2 characters.', "admin")
            is_valid = False
        
        # Password 
        if (len(data['password']) < 8):
            # password is too short
            flash('Password needs to have at least 8 characters', "admin")
            is_valid = False
            
        if (re.search('[0-9]', data['password']) == None):
        # password does not contain digits
            flash('Password must container at least one number', "admin")
            is_valid = False
        
        if (re.search('[A-Z]', data['password']) == None):
            # password does not contain uppercase letters
            flash('Password must contain at least one uppercase letter', "admin")
            is_valid = False
            
        if (regex.search(data['password']) == None):
            # password contains not special characters
            flash('Password must contain at least one special character', "admin")
            is_valid = False
        
        if (data['password']!= data['confirm_password']):
            flash('Passwords do not match', "admin")
            is_valid = False
        
        # email 
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        
        if (re.fullmatch(regex, data['email'])):
            # need to check if the email is already in use
            this_user = {
                'email': data['email']
            }
            potential_user = Admin.get_user_by_email(data) 
            
            if potential_user:
                flash('Email is already in use, please try a different email', "admin")
                is_valid = False
        else:
            flash('Email must be a valid format', "admin")
            is_valid = False
        
        return is_valid

    @staticmethod
    def valid(data):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        # First Name 
        if (regex.search(data['first_name']) != None or len(data['first_name']) < 2):
            # first name contains special characters
            flash('First name contains special characters or does not have at least 2 characters.', "edit")
            is_valid = False
        
        # Last Name 
        if (regex.search(data['last_name'])!= None or len(data['last_name']) < 2):
            # last name contains special characters
            flash('Last name contains special characters or does not have at least 2 characters.', "edit")
            is_valid = False
        
        return is_valid