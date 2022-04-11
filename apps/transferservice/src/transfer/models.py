from flask import (
    current_app,
)

from uuid import uuid4
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

from src import db


class TransferKey(db.Model):
    __tablename__ = "transfer_key"
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    key = db.Column(db.String(30))
    target = db.Column(db.String(200))
    last_update = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, key, target):
        self.key = key
        self.target = target

    @classmethod
    def get_key(cls, key):
        """
        Check the given key is in database or not
        """        
        filters = {"key": key}
        return cls.query.filter_by(**filters).first()

    @classmethod
    def check_collision(cls, key, target):
        """
        Check the given key is in database or not
        """
        res = cls.get_key(key)
        return True if res and res.target != target else False

    @classmethod
    def update_key(cls, key):
        """
        Check the given key is in database or not
        """        
        try:
            res = cls.get_key(key)
            if res:
                res.last_update = datetime.now()
                db.session.commit()
                current_app.logger.info(f"Key existed and update successfully -- {key}")
        except:
            pass

    @classmethod
    def set_key(cls, key, target):
        """
        Check the given key is in database or not
        """
        try:
            res = cls.get_key(key)
            if res:
                cls.update_key(key)
            else:
                data = cls(key=key, target=target)
                db.session.add(data)
                db.session.commit()
                current_app.logger.info(f"Set successfully -- {key}")
            return True
        except:
            current_app.logger.error()
            return False

    @classmethod
    def del_key(cls, key):
        """
        Check the given key is in database or not
        """
        try:
            res = cls.get_key(key)
            db.session.delete(res)
            db.session.commit()
            return True 
        except:
            return False