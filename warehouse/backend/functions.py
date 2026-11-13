from os import close

from sqlalchemy import create_engine,Integer,String,Date,Column
from sqlalchemy.orm import Session,declarative_base
from fastapi import FastAPI,HTTPException
from datetime import date,datetime,timedelta,timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()

DB_PATH = "warehouse.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()

# USERNAME = "Naidile"
# PASSWORD = "asdfghjkl"
ACCESS_TOKEN_EXPIRY = 15 #minites
REFRESH_TOKEN_EXPIRY=7*24*60
SECRET_KEY = "1234567890"
ALGORITHM = "HS256"

class Pakage(Base):
    __tablename__ = "pakage"
    id = Column(Integer,primary_key= True)
    name=Column(String) 
    destination = Column(String)
    weight = Column(Integer)
    arrival_date=Column(Date)
    status = Column(String)
    dispatched_id = Column(Integer)

class Dispatch(Base):
        __tablename__ = "dispatch"
        id = Column(Integer,primary_key= True)
        vehicle = Column(String)
        destination = Column(String)
        dstatus=Column(String)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer , primary_key= True)
    user_name = Column (String )
    password = Column (String)
    
Base.metadata.create_all(engine)


# 	Get the details of a specific package
def get_pakage(id):
    session = session(engine)
    pakage=session.get(Pakage,id)
    if pakage is None:
         raise HTTPException(Status_code=404,detail="Pakage not found")   
    response={
            "id":pakage.id,
            "name":pakage.name,
            "destination":pakage.destination,
            "weight":pakage.weight,
            "arrival_date":pakage.arrival_date,
            "status":pakage.status,
           }
    session.close()
    return response   

# 	Register a package
def registar_pakage(name,destination,weight,arrival_date,status):
    session=session(engine)
    pakage=pakage(name=name,destination=destination,weight=weight,arrival_date=arrival_date,status=status)
    session.add(pakage)
    session.commit()
    response={
                "id":pakage.id,
                "name":pakage.name,
                "destination":pakage.destination,
                "weight":pakage.weight,
                "arrival_date":pakage.arrival_date,
                "status":pakage.status,
            }
    session.close()
    return response

def verify_login(username,password):
        session =Session(engine)
        user = session.query(User).filter_by(user_name=username).first()
        if user is None:
             session.close()
             return False
        try:
            ph.verify(user.password , password)
        except VerifyMismatchError:
            return False
        session.close()
        # return True
        session.close()
        access_token = create_token(username=username, token_type="access")
        refresh_token = create_token(username=username, token_type="refresh")
        return {"access_token": access_token, "refresh_token":refresh_token}
     
    # if username==USERNAME and password==PASSWORD:
    #     access_token = create_token(username=USERNAME, token_type="access")
    #     refresh_token = create_token(username=USERNAME, token_type="refresh")
    #     return {"access_token":access_token, "refresh_token":refresh_token}
    # return None

def create_token(username , token_type):
    time=ACCESS_TOKEN_EXPIRY
    if token_type=="refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload = {"username": username, "token_type": token_type , "exp": datetime.now(timezone.utc) + timedelta(minutes=time)}
    token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token, token_type="access"):
    try:
        playload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except:
        return False
    if playload["token_type"]== token_type:
        return playload["username"]
    return False

# users
def registar_user(user_name , password):
    session=Session(engine)
    user_exists= session.query(User).filter_by(user_name=user_name ).first()
    if user_exists is not None:
        session.close()
        return False
    session.add(User(user_name=user_name,password=ph.hash(password)))
    session.commit()
    session.close()
    return True     

# update pakages
def update_pakage (id):
    session = session(engine)
    pakage=session.get(pakage,id)
    if pakage is None:
        raise HTTPException(Status_code=404,detail="Package not found") 
    response=update_pakage()
    session.close()
    return response

# delete pakages 
def delete_pakages(id):
     session = session(engine)
     pakage = session.get(pakage,id)
     if pakage is None:
          session.close()
          raise HTTPException(status_code=404 , detail="pakage not found")
     if pakage.status == "dispatched":
          session.close()
          raise HTTPException(status_code = 409, detail="dispatched pakage cannot delete")
     session.delete(pakage)
     session.commit()
     session.close()
     return {"mrssage": "pakage deleted"}

# search and filter 
def search_pakages (id):
    session = session(engine)
    pakage=session.query(pakage,id)
    if pakage is None:
             raise HTTPException(Status_code=404,detail="Package not found")   
    response={
                "id":pakage.id,
                "name":pakage.name,
                "destination":pakage.destination,
                "weight":pakage.weight,
                "arrival_date":pakage.arrival_date,
                "status":pakage.status,
               }
    session.close()
    return response   


# view
def get_dispatched(dispatched=Dispatch):
     session = session(engine)
     dispatched = session.get(dispatched)
     if dispatched is None:
         raise HTTPException(status_code = 404 , detail= "pakage not found")
     response =({
          "id":dispatched.id,
            "vehicle":dispatched.vehicle,
            "destination":dispatched.destination,
            "dstatus":dispatched.dstatus,
            "pakage_id":dispatched.pakage_id
            })
     session.close()
     return response(dispatched=dispatched)

# wearhouse statistics 
def get_statics  ():
     session=session(engine)
     pakage=session.query(pakage)
     response=[]
     session.close()
     return response

# dispatch details
def add_data():
     session=session(engine)
     pakage=pakage()
     session.add(pakage)
     session.commit()
     response={
                "id":pakage.id,
                "name":pakage.name,
                "destination":pakage.destination,
                "weight":pakage.weight,
                "arrival_date":pakage.arrival_date,
                "status":pakage.status,
            }
     session.close()
     return response
     

          
       


     
     
       
    



