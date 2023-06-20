"""
    ABOUT:
        In this file you need to add classes that will represent 
        your table in the database

        # ======================================================= #
        If it is a turnkey development, 
        I myself will describe everything to your requirements
"""


import logging
# Enable logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - %(levelname)s | %(message)s')
# Module for work with the database
import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
# Just json
import json

# Creating a base database instance
Base = declarative_base()


class Table_News(Base):
    __tablename__ = 'news'
    id = sa.Column(sa.Integer,primary_key=True, autoincrement=True)
    new_name = sa.Column(sa.String)
    new_media_data = sa.Column(sa.Text)
    new_media_caption = sa.Column(sa.Text)
    new_media_button = sa.Column(sa.Text)

    async def get(self):
        try:
            return (
                int(self.id), self.new_name, json.loads(self.new_media_data), 
                self.new_media_caption, json.loads(self.new_media_button)
            )
        except json.decoder.JSONDecodeError:
            return (
                int(self.id), self.new_name, self.new_media_data, 
                self.new_media_caption, self.new_media_button
            )
