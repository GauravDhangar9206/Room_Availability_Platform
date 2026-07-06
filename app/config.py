import os

class Config:
    SECRET_KEY = "roomplatform123"

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Gaurav@localhost:5432/room_platform"

    SQLALCHEMY_TRACK_MODIFICATIONS = False