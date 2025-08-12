from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from DatabaseContext import ExtractDBData, CreateDBData, CreateDBEventLogs
import json
from pydantic import BaseModel
#from Models.EventLogs import EventLog as EventLogModel
from typing import Optional

app = FastAPI()

tags_metadata = [
    {"name": "GENERIC CALLS", "description": "These End-points capture  all the generic operations"},
    {"name": "ADMIN CALLS", "description": "These End-points capture all the admin related operations"},
    {"name": "TRANSACTION CALLS", "description": "These End-points capture all the transaction related operations"},
     {"name": "AUDIT CALLS", "description": "These End-points capture all the audit related operations"},
]


# Generic calls
#------------------

# Get Username and Password from Environment Variables
@app.get("/Get_UserDetails/", tags=["GENERIC CALLS"])
def read_userdetails():
    read_userdetails = ExtractDBData.read_userdetails_data()
    
    if read_userdetails is None:
        return {"error": "User details data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_userdetails.to_dict(orient='records')

# Get Products List
@app.get("/Get_Products_List/", tags=["GENERIC CALLS"])
def read_productslist():
    return {"products": ["Product1", "Product2", "Product3"]}

# Get Products
@app.get("/Get_Products_Detail/", tags=["GENERIC CALLS"])
def read_productsdetail():
    return {"products": ["Product1", "Product2", "Product3"]}

# Add EventLog
@app.post("/Add_EventLogs/", tags=["GENERIC CALLS"])
def create_eventlogs(Event: str,
                        UserId: int,
                        TransactionId: str,
                        CorrelationId: Optional[str] = None,
                        Url: Optional[str] = None,
                        RequestBody: Optional[str] = None,
                        ResponseBody: Optional[str] = None,
                        Duration: Optional[int] = 0):
    
    create_eventlogs = CreateDBEventLogs.create_eventlogs_data(Event,
                        UserId,
                        TransactionId,
                        CorrelationId,
                        Url,
                        RequestBody,
                        ResponseBody,
                        Duration)
    

    if create_eventlogs is None:
        return {"error": "Event logs data not found"}
  
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return create_eventlogs.to_dict(orient='records')

# TRANSACTION User
#------------------
# Add Transaction
@app.post("/Add_Transaction/", tags=["TRANSACTION CALLS"])
def create_transaction():
    return {"message": "Transaction added successfully"}

# Audit User
#------------------
# Get EventLog per User 
@app.get("/Get_EventLog_Per_User/", tags=["AUDIT CALLS"])
def read_eventlogperuser():
    return {"event_logs": ["Log1", "Log2", "Log3"]}

# Get EventLog per Transaction Type per time period
@app.get("/Get_EventLog_Per_Product/", tags=["AUDIT CALLS"])
def read_eventlogperproduct():
    return {"event_logs": ["Log1", "Log2", "Log3"]}

# Admin calls
#------------------
# Get Accesslogs
@app.get("/Get_Accesslogs/", tags=["ADMIN CALLS"])
def read_accesslogs():
    return {"event_logs": ["Log1", "Log2", "Log3"]}

# GetUserRolls
@app.get("/Get_User_Rolls/", tags=["ADMIN CALLS"])
def read_userrolls():
    #read_userrolls_data
    read_userrolls = ExtractDBData.read_userrolls_data()

    if read_userrolls is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_userrolls.to_dict(orient='records')

# Get UserName and Password 
@app.get("/Get_Users/", tags=["ADMIN CALLS"])
def read_userdetails():
    return {"username": "admin", "password": "password123"}

# Add UsereName and Password for Admin
@app.post("/Add_New_User/", tags=["ADMIN CALLS"])
def create_newuser():
    return {"message": "New user added successfully"}

# Add or Update User Roles
@app.post("/Add_Update_UserRole/", tags=["ADMIN CALLS"])
def create_addupdateuserrole():
    return {"message": "User role updated successfully"}



