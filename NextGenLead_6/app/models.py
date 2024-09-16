from sqlalchemy import Column, String, Date, Text, DECIMAL, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

# Define the Account model
class Account(Base):
    __tablename__ = 'account'
    account_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    account_name = Column(String(255), nullable=False)

# Define the Dealer model
class Dealer(Base):
    __tablename__ = 'dealer'
    dealer_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    dealer_code = Column(String(50), nullable=False)
    opportunity_owner = Column(String(255), nullable=False)

# Define the Opportunity model
class Opportunity(Base):
    __tablename__ = 'opportunity'
    opportunity_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    opportunity_name = Column(String(255))
    account_id = Column(String, ForeignKey('account.account_id'))
    close_date = Column(Date)
    amount = Column(DECIMAL(10, 2))
    description = Column(Text)
    dealer_id = Column(String, ForeignKey('dealer.dealer_id'))
    dealer_code = Column(String(50))
    dealer_name_or_opportunity_owner = Column(String(255))
    stage = Column(String(50))
    probability = Column(Integer)
    next_step = Column(String(255))
    created_date = Column(TIMESTAMP, default=datetime.utcnow)
