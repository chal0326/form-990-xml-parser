
from helpers.database.interface import MongoInterface 
from helpers.database.d1_interface import D1Interface
import sys

# Overview: 3 Classes (1 per document)  with one interface per form, each interface contains methods to access databases 

class FormBase(MongoInterface):
    """
    Base class that handles routing to either Mongo or D1 based on flags
    """
    def __init__(self, all_data, schedules, form_type):
        super(FormBase, self).__init__(all_data, schedules, form_type)
        self.all_data = all_data
        self.schedules = schedules
        self.form_type = form_type
        self.use_d1 = '--d1' in sys.argv[1:]
        if self.use_d1:
             self.d1_interface = D1Interface()

    def insert_data_to_mongo(self):
        if self.use_d1:
             self.d1_interface.insert_form(self.all_data, self.schedules, self.form_type)
        else:
             super(FormBase, self).insert_data_to_mongo()

    def insert_data_force_to_mongo(self):
        if self.use_d1:
             # D1 insert uses INSERT OR REPLACE, so force is implied
             self.d1_interface.insert_form(self.all_data, self.schedules, self.form_type)
        else:
             super(FormBase, self).insert_data_force_to_mongo()

    def update_data_mongo(self):
        if self.use_d1:
             # D1 insert uses INSERT OR REPLACE
             self.d1_interface.insert_form(self.all_data, self.schedules, self.form_type)
        else:
             super(FormBase, self).update_data_mongo()

class Form990PF (FormBase):

	'''

	This class represents a form 990pf document with schedules

	Each variable that is passed to this class "Mongo interface"
	gives the class/object access to methods necessary to insert data into mongo

	In other words: Say you have a form that needs to be inserted into Mongo or removed etc. 
	The intefaces allow you to do that. 

	'''

	def __init__(self, all_data, schedules):
		super(Form990PF, self).__init__(all_data, schedules, "990PF") 
		self.form_type = "990PF"
        # Creates a form 990PF
        # w variables all data & schedules --> allows us to bind the data that will be passed from parser
        # setting the form type variable as 990pf

class Form990 (FormBase):


	'''

	This class represents a form 990 document with schedules

	Each variable that is passed to this class "Mongo interface"
	gives the class/object access to methods necessary to insert data into mongo

	In other words: Say you have a form that needs to be inserted into Mongo or removed etc. 
	The intefaces allow you to do that. 

	'''

	def __init__(self, all_data, schedules):
		super(Form990, self).__init__(all_data, schedules, "990")
		self.form_type = "990"
        # Creates a form 990
        # w variables all data & schedules --> allows us to bind the data that will be passed from parser
        # setting the form type variable as 990


class Form990EZ (FormBase):

	'''

	This class represents a form 990ez document with schedules

	Each variable that is passed to this class "Mongo interface "
	gives the class/object access to methods necessary to insert data into mongo

	In other words: Say you have a form that needs to be inserted into Mongo or removed etc. 
	The intefaces allow you to do that. 

	'''

	def __init__(self, all_data, schedules):
		super(Form990EZ, self).__init__(all_data, schedules, "990EZ")
		self.form_type = "990EZ"
        # Creates a form 990EZ
        # w variables all data & schedules --> allows us to bind the data that will be passed from parser
        # setting the form type variable as 990ez
