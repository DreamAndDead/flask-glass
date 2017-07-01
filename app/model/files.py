"""
table files in db
"""
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from .. import db

class Files(db.Model):
    """
    entries of table files
    """
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    filename = Column(VARCHAR(2048), default=None)

