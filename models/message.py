import datetime

from database import db, ma


# Model
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.String(30), nullable=False)
    receiver = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    read_by_receiver = db.Column(db.Boolean, default=False, nullable=True)

    def __repr__(self):
        return '<%r - %r: %r>' % (self.creation_date, self.subject, self.message)


# Schema
class MessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message


# Init Schemas
message_schema = MessageSchema()
messages_schema = MessageSchema(many=True)
