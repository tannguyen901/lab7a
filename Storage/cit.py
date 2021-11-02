from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Cit(Base):
    """ Class information """

    __tablename__ = "cit"

    id = Column(Integer, primary_key=True)
    class_id = Column(String(250), nullable=False)
    class_name = Column(String(250), nullable=False)
    instructor = Column(String(250), nullable=False)
    max_class_size = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    
    


    def __init__(self, class_id, class_name, instructor, max_class_size):
        """ Initializes a blood pressure reading """
        self.class_id = class_id
        self.class_name = class_name
        self.instructor = instructor
        self.max_class_size = max_class_size
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['class_id'] = self.class_id
        dict['class_name'] = self.class_name
        dict['instructor'] = self.instructor
        dict['max_class_size']= self.max_class_size
        dict['date_created'] = self.date_created

        return dict
