# import sqlite3 as sql

# def create_indices(connection : sql.Connection):
#     connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS user_ids ON users(user_id, permission_levels)")
#     connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS class_types_ids ON class_types(type_id)")
#     connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS class_ids ON classes(class_id, type_id)")
#     connection.execute("CREATE UNIQUE INDEX IF NOT EXISTS enrlm_ids ON enrollments(class_id, user_id)")
#     connection.commit()

# def create_tables(connection : sql.Connection):
#     create_user(connection)
#     create_class_type(connection)
#     create_class(connection)
#     create_enrollments(connection)
#     create_payments(connection)
#     create_schedules(connection)


# def create_user(connection : sql.Connection):
#     connection.execute(
# '''CREATE TABLE IF NOT EXISTS users (
# user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
# first TEXT, 
# last TEXT,
# phone TEXT,
# password_hash TEXT, 
# email TEXT UNIQUE ON CONFLICT ROLLBACK,
# time_stamp DATETIME,
# permission_levels TINYINT)
# ''' )
# # add phone number, first and last name, address: city state zip country, 
#     connection.commit()


# def create_class_type(connection : sql.Connection):
#     connection.execute(
# '''CREATE TABLE IF NOT EXISTS class_types (
# type_id INTEGER PRIMARY KEY AUTOINCREMENT, 
# type_name TEXT)
# ''' )
#     connection.commit()


# def create_class(connection : sql.Connection):
#     connection.execute(
# '''CREATE TABLE IF NOT EXISTS classes (
# class_id INTEGER PRIMARY KEY AUTOINCREMENT, 
# title TEXT,
# type_id INTEGER, 
# start_date DATETIME,
# end_date DATETIME,
# price DECIMAL(10,2),
# teacher_id INTEGER,
# link TEXT,
# FOREIGN KEY(type_id) REFERENCES class_types(type_id),
# FOREIGN KEY(teacher_id) REFERENCES users(user_id))
# ''' )
#     connection.commit()

# def create_schedules(connection : sql.Connection):
#     '''Creates a schedules table with PK, FK to classes, start/end time, weekday, and notes
    
#     schedule_id is an INTEGER PK autoincrementing
#     class_id is an INTEGER foreign key to classes
#     weekday is a TEXT value restricted to capital case weekdays or 'N/A'
#     start_time is a DATETIME with the hour:minute:sec value set to 0:0:0 if n/a
#     end_time is a DATETIME with the hour:minute:sec value set to 0:0:0 if n/a
#     '''

#     connection.execute('''CREATE TABLE IF NOT EXISTS schedules (
# schedule_id INTEGER PRIMARY KEY AUTOINCREMENT,
# class_id INTEGER,
# weekday TEXT DEFAULT "N/A" CHECK( weekday IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Saturday', 'Sunday', 'Friday', 'N/A')),
# start_time DATETIME,
# end_time DATETIME,
# notes TEXT,
# FOREIGN KEY(class_id) REFERENCES classes(class_id))
#     ''')
#     connection.commit()

# def create_payments(connection : sql.Connection):
#     '''Creates a payments table

#     payments_id INTEGER PK for the specific enrollment in a date range
#     enrollment_number INTEGER FK to enrollments (access to classes, users, etc.))
#     price DOUBLE for the price to pay in date range (e.g., monthly of $100 from $1200 yearly)
#     period_start DATETIME
#     period_end DATETIME
#     pay_date DATETIME deadline to pay
#     inactive_pay_date DATETIME deadline before account is inactive for that class
#     '''

#     connection.execute('''CREATE TABLE IF NOT EXISTS payments (
# payments_id INTEGER PRIMARY KEY AUTOINCREMENT,
# enrollment_number INTEGER,
# price DECIMAL(10,2),
# period_start DATETIME,
# period_end DATETIME,
# pay_date DATETIME, 
# inactive_pay_date DATETIME,
# paid BOOLEAN DEFAULT FALSE,
# FOREIGN KEY(enrollment_number) REFERENCES enrollments(enrollment_number))
#     ''')
#     connection.commit()



# def create_enrollments(connection : sql.Connection):
#     connection.execute(
# '''CREATE TABLE IF NOT EXISTS enrollments (
# enrollment_number INTEGER PRIMARY KEY AUTOINCREMENT, 
# user_id INTEGER, 
# class_id INTEGER,
# active BOOLEAN DEFAULT TRUE,
# FOREIGN KEY(class_id) REFERENCES classes(class_id),
# FOREIGN KEY(user_id) REFERENCES users(user_id))
# ''' )
# # add active/inactive DONE
# # add payment table linked to enrollment id: payment due date, payment reminder date, paid for next month, paid for current month, paid for all
#     connection.commit()


# '''
# #
# classes to represent the database
# (ABSTRACT) can be instantiated if needed; extra memory for no reason
# - users 
#     - Userid
#     - username
#     - password hash
#     - email?
#     - time stamp of creation
#     - permission levels
#         - 0 = student, 1 = teacher, 2 = administrator
# - class (ALL times in UTC, need to be converted per session)
#     - Classid
#     - title
#     - Typeid
#     - start date
#     - end date
#     - start timing
#     - end timing
#     - cost
#     - teacher id
# - classtype
#     - Typeid
#     - String type : Nazirah, etc. Can be manually created
#     - created by : ...

# - enrollments
#     - Userid
#     - Classid
#     - has_paid ; default false


# class User: 
#     user_id : int
#     username : str
#     password : str
#     email : str
#     timestamp : dt
#     permission_level : int

#     def __init__(self, id=0, name="", password_hash="", email_address="", creation_time=dt.utcnow( ), permissions=0) -> None:
#         self.user_id = id
#         self.username = name
#         self.password = password_hash
#         self.email = email_address
#         self.timestamp = creation_time
#         self.permission_level = permissions


# class Class:
#     class_id : int      # internal id to quickly identify the class
#     title : str         # String title of the class
#     type_id : int       # link to the ClassType id that represents this kind of class 
#     start : dt          # dt representation of the start date
#     end : dt            # dt representation of the end date
#     cost : float        # price, in USD, of the class
#     teacher_id : int  # teacher's name
#     link : str          # store the zoom link, etc. as a str
#     days : list         # store in a list of size 7—i in range [0, 6]—of the 24-hour representations of the time
#                             # each day's format: days[i] -> ((start_hour, start_minute), (end_hour, end_minute)) 

#     def __init__(self, id=0, title="", type=0, start_time=dt.utcnow(), end_time=dt.utcnow(),
#                   cost=.0, teacher=0, link="", days=[]) -> None:
#         self.user_id = id
#         self.title = title
#         self.type_id = type
#         self.start = start_time
#         self.end = end_time
#         self.cost = cost
#         self.teacher_name = teacher
#         self.link = link
#         self.days = days

#     # returns the us central time in the following format:
#     # (day, month, year, hour, minute, second)
#     def get_start_date(self): 
#         return Class.convert_time(self.start)
    
#     def get_end_date(self):
#         return Class.convert_time(self.end)
    
#     @staticmethod
#     def convert_time(datetime_instance : dt) -> tuple:
#         copy_dt = datetime_instance.astimezone(tz.timezone('US/Central'))
#         return (copy_dt.day, copy_dt.month, copy_dt.year, copy_dt.hour, copy_dt.minute, copy_dt.second)
    
# class ClassType:
#     type_id: int
#     type_name : str  # string title of the class

#     def __init__(self, id=0, name="") -> None:
#         self.type_id = id
#         self.type_name = name
# class Enrollments:
#     user_id : int
#     class_id : int
#     has_paid : bool # ; default false

#     def __init__(self, user_id=0, class_id=0, has_paid=False) -> None:
#         self.user_id = user_id
#         self.class_id = class_id
#         self.has_paid = has_paid
# '''