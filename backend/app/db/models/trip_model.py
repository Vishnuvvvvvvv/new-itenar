from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Trip(Base):

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)

    user_input = Column(String)

    destination = Column(String)

    status = Column(String)