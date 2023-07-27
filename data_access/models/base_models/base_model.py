'''Outlines BaseModel, the basic representation of any SQLite table

Note: 
    - The method to add a class type to the possible values is as follows
        - Add the following fields to __type_mappings__ (make sure to add new ones and not delete the old ones)
            - A default value to the "default" field
            - A converter function (from str to YourClass and raises ValueError is the conversion fails)
            - a to_str function

Variables:
    __vars__ : dict
        The instance variable which matches SQL column names (in str form) to their data type (e.g., datetime.datetime)
            e.g., "col1" : int, "col2" : str, ...
        NOTE: after initiation, __vars__ WON'T have cols mapped to types, rather they'll be mapped to values 
            (either default, or end_user generated)
    __type_mappings__ : dict
        A class variable which matches date types (e.g., datetime.datetime) to necessary information about them
            - e.g., int : {"default_value" : 0, "converter" : int}, str : {...}...
            - Fields
                "default_value":
                    Stores the default value, in the correct python type, for a specified type
                "converter"
                    Stores a function to convert strings to the needed type (should throw ValueError if it fails)

Functions:
    def __init__(self) -> None:
        This super init should be called after the user has filled __vars__ with the necessary value
        It turns the types to their default values, specified in the __type_mappings__ attribute.
        See :py:attr:`__vars__ <BaseModel.__vars__>` or :py:attr:`__type_mappings__ <BaseModel.__type_mappings__>` for more details.
    def init_subclass(cls) -> None:
        Updates the __repr__ and __str__ functions of the object. 
        See :py:func:__repr__ <BaseModel.__repr__> and :py:func:__str__ <BaseModel.__str__> for more details.
    def __repr__(self):
        Returns a string version of the object, which is a string of the __vars__ dict 
    def __str__(self):
        Returns a string version of the object, which is a string of the __vars__ dict 
    def fetch_cols(self, *args) -> dict:
        Returns the stored values for the given columns, or an error message
    def init_from_data(self, data : tuple) -> None:
        Takes a tuple of the SQLite table.* and loads it, throwing an error in the case of a failure
    
        
    
                    
Internal Note
    - ONLY the end user may give types in the __vars__ field; after the init, it stores values, NOT types. 
      It must be handled as such
'''

from typing import Type

from .converters import str_to_bool


class BaseModel:
    '''BaseModel serves as the parent of any SQLite table, with convenience functions to help'''

    # stores all the fields of the sql table
    __vars__ : dict
    # maps types to their needed functionality (e.g., an function to convert the sql's str to an int)
    __type_mappings__ = {
        str : {
            "default_value" : "",
            "converter" : str,
            "to_str" : str
        },
        int : {
            "default_value" : 0,
            "converter" : int
        },
        bool : {
            "default_value" : False,
            "converter" : str_to_bool
        }, 
        float : {
            "default_value" : 0.0,
            "converter" : float
        }
    }

    def __init__(self) -> None:
        for name, annotation in self.__vars__.items():
            temp_vars = {name.strip() : val for name, val in self.__vars__.items()}
            self.__vars__ = temp_vars
            self.__vars__[name] = "" if annotation not in BaseModel.__type_mappings__ else BaseModel.__type_mappings__[annotation]["default_value"]

    def __init_subclass__(cls) -> None:
        cls.__repr__ = lambda self : str(self.__vars__)
        cls.__str__ = cls.__repr__

    def fetch_cols(self, *args) -> dict:
        '''Returns the stored values for the given columns, or an error message'''
        
        args = list(map(str, args))
        return_dict = {}
        for arg in args:
            if arg not in self.__vars__:
                this_class = self.__class__
                raise AttributeError(f"The column {arg} not found in {this_class.__module__}.{this_class.__name__}")
            else:
                return_dict[arg] = self.__vars__[arg]
        return return_dict
    
    def init_from_data(self, data : tuple) -> None:
        '''Takes a tuple of the SQL table.* and loads it'''

        new_vars = {}
        for i, (field, field_type) in enumerate(self.__vars__.items()):
            new_vars[field] = self._str_to_correct_type(data[i], type(field_type))
        
        self.__vars__ = new_vars

    def get(self, field : str):
        '''Returns the stored value, or an error if it fails'''

        try: 
            return self.__vars__[str(field)]
        except Exception:
            raise ValueError(f'The field, {field}, cannot be found in {self.__vars__}')

    
    @staticmethod
    def _str_to_correct_type(val : str, val_type : Type):
        if not isinstance(val, str):
            return val
        if val_type is str:
            return val
        try:
            return next(map(BaseModel.__type_mappings__[val_type]["converter"], {val}))
        except (ValueError, StopIteration, IndexError) as error:
            this_class = BaseModel.__class__
            error_message = f'''
Error occurred in {this_class.__module__}.{this_class.__name__}
The type of {val} (i.e., {val_type}) could not be found in the stored typings (listed below)
{BaseModel.__type_mappings__.keys()}
The system error message is {str(error)}'''
            raise TypeError(error_message)
        except Exception as error:
            this_class = BaseModel.__class__
            raise TypeError(f''' 
An error occurred in {this_class.__module__}.{this_class.__name__} while converting the value {val} to the type {val_type}
The system error message is {str(error)}'''
            )
            