from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi import HTTPException
from DatabaseContext import ExtractDBData, CreateDBData, CreateTransactions, CreateDBEventLogs, UpdateDBData,DeleteDBData
import json
from pydantic import BaseModel
#from Models.EventLogs import EventLog as EventLogModel
from typing import Optional
import traceback

app = FastAPI()

tags_metadata = [
    {"name": "RESET ALL DATA", "description": "These End-points reset all the data in the database"},
    {"name": "GENERIC CALLS", "description": "These End-points capture  all the generic operations"},
    {"name": "ADMIN CALLS", "description": "These End-points capture all the admin related operations"},
    {"name": "TRANSACTION CALLS", "description": "These End-points capture all the transaction related operations"},
     {"name": "AUDIT CALLS", "description": "These End-points capture all the audit related operations"},
]

#reset_all_data
@app.post("/Reset_All_Data/", tags=["RESET ALL DATA"])
def create_transaction():
    try:
        reset_all_data_result = CreateTransactions.reset_all_data()
        if reset_all_data_result is None:
            raise HTTPException(status_code=404, detail="Transaction data not found")

        # Directly return the dict
        return reset_all_data_result

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")




# Generic calls
#------------------

# Get Username and Password from Environment Variables
@app.get("/Get_All_Users/", tags=["GENERIC CALLS"])
def read_all_users():
    read_userdetails = ExtractDBData.read_userdetails_data()
    
    if read_userdetails is None:
        return {"error": "User details data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_userdetails.to_dict(orient='records')

# Get Username and Password from Environment Variables
@app.get("/Get_User_By_UName_Pword/", tags=["GENERIC CALLS"])
def read_userbyunamepword():
    read_userdetails = ExtractDBData.read_userdetails_data()
    
    if read_userdetails is None:
        return {"error": "User details data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_userdetails.to_dict(orient='records')

# Get Products List
@app.get("/Get_ProductsList/", tags=["GENERIC CALLS"])
def read_productslist():

    read_productslist_data = ExtractDBData.read_productslist_data()
    
    if read_productslist_data is None:
        return {"error": " Products list data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_productslist_data.to_dict(orient='records')

# Get Products
@app.get("/Get_ProductsList_By_ProviderName/", tags=["GENERIC CALLS"])
def read_productsdetail(ProviderName : str):
    #read_productslistbyprovidername_data
    read_productslistbyprovidername = ExtractDBData.read_productslistbyprovidername_data(ProviderName)
    
    if read_productslistbyprovidername is None:
        return {"error": " Products list data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_productslistbyprovidername.to_dict(orient='records')

# Get Products List
@app.get("/Get_Provider_By_Name/", tags=["GENERIC CALLS"])
def read_providerbyname(ProviderName : str):
    #read_providerbyname_data
    read_providerbyname = ExtractDBData.read_providerbyname_data(ProviderName)
    if read_providerbyname is None:
        return {"error": " Products list data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_providerbyname.to_dict(orient='records')


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
# class TransactionRequest(BaseModel):
#     ProductId: int
#     AmountPaid: int
#     TraderId: int
#     UserId: int
#     TAppType: int
#     PaymentMethod: str

@app.post("/Add_Transaction/", tags=["TRANSACTION CALLS"])
def create_transaction(ProductId: int,
    AmountPaid: int,
    TraderId: int,
    UserId: int,
    TAppType  : int,
    PaymentMethod: str):
    try:

   
        create_transactions = CreateTransactions.create_transactions_data(
            int(ProductId), int(AmountPaid), int(TraderId), int(UserId), int(TAppType), str(PaymentMethod).strip()
        )
        if create_transactions is None:
            raise HTTPException(status_code=404, detail="Transaction data not found")

        return json.loads(create_transactions.to_json(orient="records"))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# ========================
@app.get("/Get_TotalTransactions_PerUser_PerDateRange/", tags=["TRANSACTION CALLS"])
def read_totaltransactionsperuserperdaterange( UserId: int, StartDate: str, EndDate: str):
    try:

        read_totaltransactionsperuserperdaterange = ExtractDBData.read_totaltransactionsperuserperdaterange_data(UserId, StartDate, EndDate)
        if read_totaltransactionsperuserperdaterange is None:
            raise HTTPException(status_code=404, detail="Transaction data not found")

        return json.loads(read_totaltransactionsperuserperdaterange.to_json(orient="records"))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Audit User
#------------------
# Get EventLog per User 
@app.get("/Get_EventLog_PerUser/", tags=["AUDIT CALLS"])
def read_eventlogperuser(UserId: int, StartDate: str, EndDate: str):
    try:

        read_eventlogperuser_data = ExtractDBData.read_eventlogsperuser(UserId, StartDate, EndDate)
        if read_eventlogperuser_data is None:
            raise HTTPException(status_code=404, detail="Transaction data not found")

        return json.loads(read_eventlogperuser_data.to_json(orient="records"))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Get EventLog per Transaction Type per time period
@app.get("/Get_EventLog_PerDate/", tags=["AUDIT CALLS"])
def read_eventlogperperdate(StartDate: str, EndDate: str):
    try:

        read_eventlogsperdate = ExtractDBData.read_eventlogsperdate(StartDate, EndDate)
        if read_eventlogsperdate is None:
            raise HTTPException(status_code=404, detail="Transaction data not found")

        return json.loads(read_eventlogsperdate.to_json(orient="records"))
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# Admin calls
#------------------

# GetUserRolls
@app.get("/Get_User_Roles/", tags=["ADMIN CALLS"])
def read_userrolls():
    #read_userrolls_data
    read_userrolls = ExtractDBData.read_userrolls_data()

    if read_userrolls is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_userrolls.to_dict(orient='records')

# Get UserName and Password 
@app.get("/Get_User_By_Id/", tags=["ADMIN CALLS"])
def read_userbyid(UserId: int):
    #read_userbyid_data
    read_userbyid = ExtractDBData.read_userbyid_data(UserId)
    if read_userbyid is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_userbyid.to_dict(orient='records')

# Get Username and Password from Environment Variables
@app.get("/Get_UserName_By_UName_Pword/", tags=["ADMIN CALLS"])
def read_usernamebyunamepword(UserName: str, Password: str):
    #read_usernamebyunamepword_data
    read_usernamebyunamepword_data = ExtractDBData.read_usernamebyunamepword_data(UserName, Password)

    if read_usernamebyunamepword_data is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return read_usernamebyunamepword_data.to_dict(orient='records')


# Add or Update User Roles
@app.post("/Add_Voucher_To_VoucherList/", tags=["ADMIN CALLS"])
def create_addvouchertovoucherlist():
    return {"message": "User role updated successfully"}


# Delete User
@app.delete("/Delete_User/", tags=["ADMIN CALLS"])
def delete_user(UserId: int,UserIdDelete: int):
     #read_usernamebyunamepword_data
    delete_user_data = DeleteDBData.delete_user_data(UserId,UserIdDelete)

    if delete_user_data is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return delete_user_data.to_dict(orient='records')

# Delete Voucher
@app.delete("/Delete_Voucher/", tags=["ADMIN CALLS"])
def delete_voucher(VoucherNumber: int,UserId: int):
    
    delete_voucher_data = DeleteDBData.delete_voucher_data(VoucherNumber,UserId)

    if delete_voucher_data is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return delete_voucher_data.to_dict(orient='records')

# Update
@app.put("/Update_Provider_Status/", tags=["ADMIN CALLS"])
def update_provider_status(UserId: int,ProviderName: str,Status: int):
    update_provider_status_data = UpdateDBData.update_provider_status_data()

    if update_provider_status_data is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return update_provider_status_data.to_dict(orient='records')

# Update
@app.put("/Update_Trader_Status/", tags=["ADMIN CALLS"])
def update_trader_status(UserId: int,IdNumber: str,Status: int):
    update_trader_status_data = UpdateDBData.update_trader_status_data(UserId,IdNumber,Status)

    if update_trader_status_data is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return update_trader_status_data.to_dict(orient='records')

# Update
@app.put("/Update_User_Status/", tags=["ADMIN CALLS"])
def update_user_status(UserId: int,Email: str,Status: int):
    update_user_status_data = UpdateDBData.update_user_status_data(UserId,Email,Status)

    if update_user_status_data is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return update_user_status_data.to_dict(orient='records')

# Update
@app.put("/Update_Voucher_Status/", tags=["ADMIN CALLS"])
def update_voucher_status(UserId: int,VoucherNumber: int,Status: int):
    update_voucher_status_data = UpdateDBData.update_voucher_status_data(UserId,VoucherNumber,Status)

    if update_voucher_status_data is None:
        return {"error": "User roles data not found"}
    
    # Convert DataFrame to JSON serializable format (list of dictionaries)
    return update_voucher_status_data.to_dict(orient='records')






