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



# Delete User
def delete_user_data( UserId: int,iDeleteUserId: int):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    print("Creating event logs data with model:")

    try:
        iCorreclationId = str(uuid.uuid4())  # Generate a new UUID for CorrelationId
        iDuration = 5 #time.perf_counter() + 7

        cursor.execute("EXEC sp_Delete_User ?,?,?,?", (
            int(UserId),           # 1 -> @iUserId
            int(iDeleteUserId),      # 2 -> @iUserIdDelete
            int(iDuration),        # 3 -> @iDuration
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
def delete_voucher_data(VoucherNumber: int,UserId: int):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    print("Creating event logs data with model:")

    try:
        iCorreclationId = str(uuid.uuid4())  # Generate a new UUID for CorrelationId
        iDuration = 5 #time.perf_counter() + 7

        cursor.execute("EXEC sp_Delete_Voucher ?,?,?,?", (
            int(VoucherNumber),           # 1 -> @VoucherNumber
            int(UserId),      # 2 -> @iUserId
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
  
