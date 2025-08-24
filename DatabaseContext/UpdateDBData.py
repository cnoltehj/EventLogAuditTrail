import pyodbc
import os
import sys
import pandas as pd  # Import pandas for DataFrame handling
import config  # Import config module for database connection details
import uuid
import time
from functools import wraps
from pydantic import BaseModel
from typing import Optional

def connect_to_database():
    try:
        # Get the current script path
        current_path = os.path.dirname(os.path.abspath(__file__))
        print("Current path:", current_path)
    except NameError:
        # Fallback if __file__ is not defined (e.g., in Jupyter)
        current_path = os.getcwd()
        print("Current path:", current_path)

    # Add the parent directory to the system path
    sys.path.append(os.path.dirname(current_path))

    # Database connection parameters from config
    server = config.DefaultConnection['server']
    database = config.DefaultConnection['database']
    username = config.DefaultConnection['username']
    password = config.DefaultConnection['password']

    # Establish database connection
    cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return cnxn


# Update Provider Status
def update_provider_status_data(UserId: int, ProviderName: str, Status: int):
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        iCorreclationId = str(uuid.uuid4())
        iDuration = 5

        cursor.execute("EXEC sp_Update_Provider_Status ?,?,?,?,?", (
            int(UserId),
            str(ProviderName).strip(),
            int(Status),
            int(iDuration),
            str(iCorreclationId)
        ))

        cnxn.commit()
        print("Executed stored procedure sp_Update_Provider_Status.")

        # ✅ If SP returns rows, serialize them
        if cursor.description is not None:
            rows = cursor.fetchall()
            headings = [col[0] for col in cursor.description]
            results = [dict(zip(headings, row)) for row in rows]  # JSON safe
            return {"status": "success", "data": results}
        else:
            return {
                "status": "success",
                "message": f"Provider '{ProviderName}' updated to status {Status} by user {UserId}"
            }

    except pyodbc.Error as e:
        print("Error executing SQL query:", e)
        return {"status": "error", "message": str(e)}

    finally:
        cursor.close()
        cnxn.close()

  
# Delete Voucher
def update_trader_status_data(UserId: int,IdNumber: str,Status: int):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    print("Creating event logs data with model:")

    try:
        iCorreclationId = str(uuid.uuid4())  # Generate a new UUID for CorrelationId
        iDuration = 5 #time.perf_counter() + 7

        cursor.execute("EXEC sp_Update_Trader_Status ?,?,?,?,?", (
            int(UserId),           # 1 -> @UserId
            str(IdNumber),   
            int(Status),         # 3 -> @iStatus
            int(iDuration),         # 3 -> @iDuration
             str(iCorreclationId)  # 4 -> @iCorrelationId
        ))
        
        print("Executed stored procedure sp_Add_EventLog with parameters.")

        cnxn.commit()

        # Fetch the results after executing the stored procedure
        rows = cursor.fetchall()

        # Fetch the column descriptions (headings)
        headings = [column[0] for column in cursor.description]

        # Reshape the rows data to match the expected shape
        rows = [list(row) for row in rows]

        # Create a DataFrame from the fetched rows and headings
        df = pd.DataFrame(rows, columns=headings)

        # Replace null values with 0's
        df.fillna(0, inplace=True)

        return df
        #return df  # Return the DataFrame

    except pyodbc.Error as e:
        # Print an error message if there's an exception
        print("Error executing SQL query:", e)
        return None  # Return None if there's an error

    finally:
        # Close the cursor and connection
        cursor.close()
        cnxn.close()    
  
# Delete Voucher
def update_user_status_data(UserId: int,Email: str,Status: int):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    print("Creating event logs data with model:")

    try:
        iCorreclationId = str(uuid.uuid4())  # Generate a new UUID for CorrelationId
        iDuration = 5 #time.perf_counter() + 7

        cursor.execute("EXEC sp_Update_User_Status ?,?,?,?,?", (
            int(UserId),          # 1 -> @UserId
            str(Email),   
            int(Status),         # 3 -> @iStatus   
            int(iDuration),         # 4 -> @iDuration
             str(iCorreclationId)  # 5 -> @iCorrelationId
        ))
        
        print("Executed stored procedure sp_Add_EventLog with parameters.")

        cnxn.commit()

        # Fetch the results after executing the stored procedure
        rows = cursor.fetchall()

        # Fetch the column descriptions (headings)
        headings = [column[0] for column in cursor.description]

        # Reshape the rows data to match the expected shape
        rows = [list(row) for row in rows]

        # Create a DataFrame from the fetched rows and headings
        df = pd.DataFrame(rows, columns=headings)

        # Replace null values with 0's
        df.fillna(0, inplace=True)

        return df
        #return df  # Return the DataFrame

    except pyodbc.Error as e:
        # Print an error message if there's an exception
        print("Error executing SQL query:", e)
        return None  # Return None if there's an error

    finally:
        # Close the cursor and connection
        cursor.close()
        cnxn.close()    
  
# Delete Voucher
def update_voucher_status_data(UserId: int,VoucherNumber: int,Status: int):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    print("Creating event logs data with model:")

    try:
        iCorreclationId = str(uuid.uuid4())  # Generate a new UUID for CorrelationId
        iDuration = 5 #time.perf_counter() + 7

        cursor.execute("EXEC sp_Update_Voucher_Status ?,?,?,?,?", (
            int(UserId),           
            int(VoucherNumber), 
            int(Status),         # 3 -> @iStatus     
            int(iDuration),         # 3 -> @iDuration
             str(iCorreclationId)  # 4 -> @iCorrelationId
        ))
        
        print("Executed stored procedure sp_Add_EventLog with parameters.")

        cnxn.commit()

        # Fetch the results after executing the stored procedure
        rows = cursor.fetchall()

        # Fetch the column descriptions (headings)
        headings = [column[0] for column in cursor.description]

        # Reshape the rows data to match the expected shape
        rows = [list(row) for row in rows]

        # Create a DataFrame from the fetched rows and headings
        df = pd.DataFrame(rows, columns=headings)

        # Replace null values with 0's
        df.fillna(0, inplace=True)

        return df
        #return df  # Return the DataFrame

    except pyodbc.Error as e:
        # Print an error message if there's an exception
        print("Error executing SQL query:", e)
        return None  # Return None if there's an error

    finally:
        # Close the cursor and connection
        cursor.close()
        cnxn.close()    
  

