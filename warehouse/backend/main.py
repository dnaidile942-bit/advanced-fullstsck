# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# import functions

# app = FastAPI(
#     title="warehouse API",
#     description="manage and dispatch the orders",
# )
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/packages/{package_id}")
# def get_package(package_id: int):
#     return functions.get_package(package_id=package_id)

# @app.post("/warehouse/add/{package_id}/{quantity}")
# def add_to_cart(item_id: int, quantity: int):
#     return functions.add_to_cart(item_id=item_id, quantity=quantity)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import functions

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/package")
def register_package(name,destination,weight,arrival_date,status):
    return functions.register_package(name=name,destination=destination,weight=weight,arrival_date=arrival_date,status=status)
    
@app.get("/package/{id}")
def get_package(id):
    return functions.get_package(id)

