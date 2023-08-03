from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
import re


class Booking:
    def __init__(self, data):
        self.id = data['id']
        self.client_name = data['client_name']
        self.email = data['email']
        self.phone = data['phone']
        self.date = data['date']
        self.time = data['time']
        self.service = data['service']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


# NEW APPT 
    @classmethod
    def new_appt(cls, data):
        query = """
        INSERT INTO bookings (client_name, email, phone, date, time, service) 
        VALUES (%(client_name)s, %(email)s, %(phone)s, %(date)s %(time)s, %(service)s)
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    

# GET APPT BY ID 
    @classmethod
    def get_by_id(cls,data):
        query="""
        SELECT * FROM bookings WHERE id = %(id)s
        """
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

# GET ALL APPTS - DISPLAY ON CALENDAR
    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM bookings 
        """
        results = connectToMySQL(DATABASE).query_db(query)
        all_appts = []
        if results:
            for row in results:
                this_appt = cls(row)
                all_appts.append(this_appt)
        return all_appts
    
# EDIT ADMIN 
    @classmethod
    def edit(cls, data):
        query = """
        UPDATE bookings
        SET client_name = %(client_name)s, email = %(email)s, date = %(date)s, time = %(time)s, service = %(service)s
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query,data)


# DELETE ADMIN 
    @classmethod
    def delete(cls, data):
        query = """
        DELETE FROM bookings 
        WHERE id = %(id)s;
        """
        return connectToMySQL(DATABASE).query_db(query, data)
    

# VALIDATION 
    @staticmethod
    def validation(data):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        
        is_valid = True
        
        # First Name 
        if (regex.search(data['client_name']) != None or len(data['client_name']) < 2):
            # first name contains special characters
            flash('Name contains special characters or does not have at least 2 characters.', "booking")
            is_valid = False
        
        # email 
        if (len(data['email']) < 2):
            flash('Email can not be empty', "booking")
            is_valid = False

        if (len(data['phone']) < 2):
            flash('Phone Number can not be empty', "booking")
            is_valid = False

        if (len(data['date']) < 2):
            flash('Date can not be empty', "booking")
            is_valid = False

        if (len(data['time']) < 2):
            flash('Time can not be empty', "booking")
            is_valid = False

        if (len(data['service']) < 2):
            flash('Service can not be empty', "booking")
            is_valid = False
        return is_valid