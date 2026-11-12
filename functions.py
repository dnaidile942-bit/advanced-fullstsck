# from sqlalchemy import Integer, String, Column, ForeignKey, create_engine,Date,func
# from sqlalchemy.orm import Session, declarative_base
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from datetime import date,timedelta,datetime


# DB_PATH = "warehouse.db"
# engine = create_engine(f"sqlite:///{DB_PATH}")
# Base = declarative_base()

from sqlalchemy import create_engine,Integer,String,Date,Column

from sqlalchemy.orm import Session,declarative_base
from fastapi import FastAPI,HTTPException
from datetime import date,datetime,timedelta
DB_PATH = "warehouse.db"

engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

class Package(Base):
    __tablename__ = "package"

    id = Column(Integer,primary_key= True)
    name=Column(String) 
    destination = Column(String)
    weight = Column(Integer)
    arrival_date=Column(Date)
    status = Column(String)

class Dispatch(Base):
        __tablename__ = "dispatch"
        id = Column(Integer,primary_key= True)
        vehicle = Column(String)
        destination = Column(String)
        dstatus=Column(String)

Base.metadata.create_all(engine)

def get_package(id):
    session = Session(engine)
    package=session.get(Package,id)
    if package is None:
         session.close()
         raise HTTPException(status_code=404,detail="Package not found")   
    response={
            "id":package.id,
            "name":package.name,
            "destination":package.destination,
            "weight":package.weight,
            "arrival_date":package.arrival_date,
            "status":package.status,
           }
    session.close()
    return response   

def register_package(name,destination,weight,arrival_date,status):
    session=Session(engine)
    package=Package(name=name,destination=destination,weight=weight,arrival_date=arrival_date,status=status)
    session.add(package)
    session.commit()
    response={
                "id":package.id,
                "name":package.name,
                "destination":package.destination,
                "weight":package.weight,
                "arrival_date":package.arrival_date,
                "status":package.status,
            }
    session.close()
    return response


