from fastapi import FastAPI, HTTPException , Body , Header
from fastapi.middleware.cors import CORSMiddleware
import AM_functions 
import SU_functions
import NA_functions

app = FastAPI()
ROLES = ["admin","staff"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def authorize(token, allowed_roles):
    donation = SU_functions.verify_token(token=token, token_type="access")
    if not donation:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    if donation["role"] not in allowed_roles:
        raise HTTPException(status_code=403, detail="You do not have permission to do this")
    return donation

@app.post("/login")
def login(username=Body(),password=Body()):
    token = SU_functions.verify_login(username=username, password=password)
    if not token :
        raise HTTPException(status_code= 401 , detail="Invalid Credintials")
    return token

@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    donation = SU_functions.verify_token(token=refresh_token , token_type="refresh")
    if not donation:
        raise HTTPException(status_code=401, detail="invalid or expired token")
    access_token= SU_functions.create_token(username=donation["username"], token_type="access", user_id=donation["user_id"], role=donation["role"])
    return{"access_token":access_token}

@app.post("/registar")
def registar_user( user_name = Body() , password = Body(), role = Body("staff")):
    if role not in ROLES:
        raise HTTPException(status_code=400, detail="role must be admin or staff")
    if SU_functions.registar_user(user_name = user_name , password= password, role=role):
        return{"message":"user registar succesfully"}
    raise HTTPException(status_code=400, detail="user already exist")

#E1 GET all donors
@app.get("/donors")
def donors(blood_group=None , token=Header(None)):
    authorize(token, ["admin","staff"])
    return SU_functions.get_all_donors(blood_group=blood_group)

#E8 GET eligible donors by blood group
@app.get("/donors/eligible")                              
def get_eligible_donors(blood_group , token=Header(None)):
    authorize(token, ["admin","staff"])
    response = NA_functions.get_eligible_donors(blood_group)
    return response


#E2 GET DONORS by roll number
@app.get("/donors/{roll_no}")
def get_donor(roll_no, token=Header(None)):
    authorize(token, ["admin", "staff"])
    return SU_functions.get_donor(roll_no.upper())

#E3 Add donor
@app.post("/donors")
def add_donor(roll_no, name, blood_group, weight_kg, token=Header(None)):
    authorize(token,["admin","staff"])
    return SU_functions.add_donor(roll_no=roll_no, name=name, blood_group=blood_group, weight_kg=weight_kg)

#E4 Book appointment
@app.post("/appointments")
def book_appoint(roll_no, drive_date, slot , token=Header(None)):
    authorize(token,["admin","staff"])
    return AM_functions.book_appoint(roll_no.upper(), drive_date, slot.lower())

#E5 Cancel appointment
@app.patch("/appointments/{id}/cancel")
def cancel_appoint(id, token=Header(None)):
    authorize(token, ["admin","staff"])
    return AM_functions.cancel_appoint(id)

#E6 Mark appointment
@app.patch("/appointments/{id}/status")
def mark_appoint(id, status, token=Header(None)):
    authorize(token, ["admin"])
    return AM_functions.mark_appoint(id, status.lower())

#E7 GET appointments by date
@app.get("/appointments") 
def get_appointments(drive_date , token=Header(None)):
    authorize(token, ["admin", "staff"])
    response = NA_functions.get_appointments_by_date(drive_date)
    return response 

#E9 GET units donated by blood group
@app.get("/appointments/status/units")                                         
def get_units(token=Header(None)):
    authorize(token, ["admin"])
    response = NA_functions.get_units()
    return response