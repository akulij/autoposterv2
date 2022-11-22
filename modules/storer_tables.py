from .storer import BaseModel
from peewee import (
    ForeignKeyField,
    CharField,
    IntegerField,
    DateField,
    BooleanField,
    FloatField,
    TextField,
)

class User(BaseModel):
    id = IntegerField(unique=True, primary_key=True)
    state = CharField()
    
class PostId(BaseModel):
    product_id = IntegerField()
    chat_id = IntegerField()
    message_id = IntegerField()
    
class PostPhoto(BaseModel):
    product_id = IntegerField()
    chat_id = IntegerField()
    message_id = IntegerField()
    
class SalePostId(BaseModel):
    product_id = IntegerField()
    chat_id = IntegerField()
    message_id = IntegerField()
    date_posted = DateField(formats=["%d-%m-%Y"])
    
class NoPhotoSalePostId(BaseModel):
    product_id = IntegerField()
    chat_id = IntegerField()
    message_id = IntegerField()

class PostFormat(BaseModel):
    format_text = TextField()

class SalePostFormat(BaseModel):
    format_text = TextField()
    
class Admin(BaseModel):
    user_id = IntegerField(unique=True)

class RenewPosts(BaseModel):
    flag = BooleanField(default=True)

class RefreshAll(BaseModel):
    flag = BooleanField(default=True)

class Prepost(BaseModel):
    chat_id = IntegerField()
    message_id = IntegerField()

class PrepostInfo(BaseModel):
    photo = TextField()
    caption = TextField()
