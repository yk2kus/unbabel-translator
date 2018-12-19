from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super(BaseModel, self).__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class BaseTerm(BaseModel, db.Model):
    """ Model for source string """
    __tablename__ = 'base_term'

    def __init__(self, term, uid = False):
        self.term = term
        uid = uid

    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String, nullable=False)
    uid = db.Column(db.String)
    translated_term = db.Column(db.String)
    status = db.Column(db.String, default='new') #new, translating, completed
    translated_term_ids = db.relationship('TranslatedTerm', backref='base_term', lazy=True)


class TranslatedTerm(BaseModel, db.Model):
    """ Model for Translated string """
    __tablename__ = 'translated_term'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('base_term.id'))
