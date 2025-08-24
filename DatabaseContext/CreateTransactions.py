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



# Add Transactions
def create_transactions_data( iProductId : int,
                              iAmountPaid : int,
                              iTraderId : int,
                              iUserId : int,
                              iTAppType  : int,
                              iPaymentMethod: str
                               ):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
   
        iCorreclationId = str(uuid.uuid4())  # Generate a new UUID for CorrelationId
        iDuration = 5 #time.perf_counter() + 7

        print(f"  ProductId={iProductId}, AmountPaid={iAmountPaid}, TraderId={iTraderId}")
        print(f"  UserId={iUserId}, PaymentMethod={iPaymentMethod}")
        print(f"  Duration={iDuration}, CorrelationId={iCorreclationId}")

        cursor.execute("EXEC sp_AddTransaction ?,?,?,?,?,?,?,?", (
            int(iUserId),           # 1 -> @iUserId
            int(iProductId),        # 2 -> @iProductId
            int(iAmountPaid),       # 3 -> @iAmountPaid
            int(iTraderId),         # 4 -> @iTraderId
            int(iTAppType),         # 5 -> @iTAppTypec
            str(iPaymentMethod).strip(),  # 6 -> @iPaymentMethod
            str(iCorreclationId).strip(), # 7 -> @iCorreclationId
            int(iDuration)          # 8 -> @iDuration
        ))

        #cnxn.commit() 
        
        print("Executed stored procedure sp_AddTransaction with parameters.")

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
  

def reset_all_data():
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        cursor.execute("EXEC sp_Reset_Voucher_Status")
        cnxn.commit()
        
        # Fetch the confirmation message
        result = cursor.fetchone()
        if result:
            return {"Result": result[0]}
        else:
            return {"Result": "Reset completed, no additional data returned."}

    except pyodbc.Error as e:
        print("Error executing SQL query:", e)
        return {"Error": str(e)}

    finally:
        cursor.close()
        cnxn.close()
