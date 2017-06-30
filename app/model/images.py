"""
Images db table structure
"""
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT, VARCHAR
from .. import db

class Images(db.Model):
    """
    images表
    """
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    filename = Column(VARCHAR(2048), default=None)

