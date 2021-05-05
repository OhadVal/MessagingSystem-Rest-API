from database import db, ma


# Model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(80))


# Schema
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        fields = ('user_id', 'username')


# Init Schema
user_schema = UserSchema()
