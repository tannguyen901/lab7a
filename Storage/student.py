from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Student(Base):
    """ Heart Rate """

    __tablename__ = "student"

    id = Column(Integer, primary_key=True)
    student_id = Column(String(250), nullable=False)
    student_name = Column(String(250), nullable=False)
    student_age = Column(Integer, nullable=False)
    start_date = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, student_id, student_name, student_age, start_date):
        """ Initializes a heart rate reading """
        self.student_id = student_id
        self.student_name = student_name
        self.student_age = student_age
        self.start_date = start_date
        self.date_created = datetime.datetime.now() # Sets the date/time record is created
 

    def to_dict(self):
        """ Dictionary Representation of a heart rate reading """
        dict = {}
        dict['id'] = self.id
        dict['student_id'] = self.student_id
        dict['student_name'] = self.student_name
        dict['student_age'] = self.student_age
        dict['start_date'] = self.start_date
        dict['date_created'] = self.date_created

        return dict
