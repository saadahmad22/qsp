'''Does setup related work
- sets publicly accessible classes
'''

# import the submodules files in thee individual files they are used. Otherwise there is the risk of a circular import

# import this modules files in
from .calendar_ import Calendar
from .user import User
from .class_schedules import ClassSchedules
from .class_types import ClassTypes 
from .enrollments import Enrollments
from .payments import Payments
from .schedules import Schedules
from .teachers import Teachers


__all__ = ["User", "Calendar", "ClassSchedules", "ClassTypes", "Enrollments", "Payments", "Schedules", "Teachers"]

# code to go through each imported model and load to DB is found in date_access -> 