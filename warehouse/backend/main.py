from fastapi import FastAPI , HTTPException,  Header , Body
from fastapi.middleware.cors import CORSMiddleware
import functions
from datetime import date 
from pydantic import BaseModel

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class pakagein (BaseModel):
    name: str
    destination: str
    weight: int
    arrival_date: date
    status: str

class pakageupdate(BaseModel):
    name: str = None
    destination: str = None
    weight: int = None
    arrival_date: date = None
    status: str = None

class dispatchin(BaseModel):
    vehicle: str
    destination: str
    dstatus: str
    pakage_id: int


# Register a pakage
@app.post("/pakage")
def registar_pakage(pakage=pakagein, token=Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.registar_pakage(pakage=pakagein)

# details of a specific pakage   
@app.get("/pakage/{id}")
def get_pakages(id , token=Header(None) ):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.get_pakage(id)

# login
@app.post("/login")
def login(username= Body(),password=Body()):
    token = functions.verify_login(username=username, password=password)
    if not token :
        raise HTTPException(status_code= 401 , detail="Invalid Credintials")
    return token

# new access token in refresh name 
@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    username= functions.verify_token(token=refresh_token , token_type="refresh")
    if not username:
        raise HTTPException(status_code=401, detail="invalid or expired token")
    access_token= functions.create_token(username=username, token_type="access")
    return{"access_token":access_token}

# registar
@app.post("/registar")
def registar_user( user_name = Body() , password = Body()):
    if functions.registar_user(user_name = user_name , password= password):
        return{"message":"user registar succesfully"}
    raise HTTPException(status_code=400, detail="user already exist")

# update pakage details
@app.patch("/pakage/{id}")
def update_pakage(id , pakage:pakageupdate , token=Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return functions.update_pakage(id,pakageupdate)

# delete pakage 
@app.delete("/pakage/{id}")
def delete_pakage(id , token=Header(None)):
    username =function.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401, detail="invalid or expired token")
    return functions.delete_pakage(id)

# search and filter 
@app.get("/pakages")
def search_pakages(id , token=Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException(status_code=401 , detail="invalid or expired token")
    return functions.search_pakages(id)

# view dispatched pakages
@app.get("/dispatched")
def get_dispatched(dispatched=dispatchin, token=Header(None)):
    username = functions.verify_token(toekn=token)
    if not username:
        raise HTTPException(status_code = 401 , detail="invali or expired token")
    return functions.get_dispatched(dispatched=dispatchin)

# warehouse statistics
@app.get("/wearhouse/stats")
def get_statics(token=Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException (status_code=401, detail="invalidor expiredtoken")
    return functions.get_statics ()

# dispatch details
@app.post("/dispatch")
def add_data(dispatch =dispatchin , token=Header(None)):
    username = functions.verify_token(token=token)
    if not username:
        raise HTTPException (status_code=401, detail="invalidor expiredtoken")
    return functions.add_data (dispatch =dispatchin)



    
