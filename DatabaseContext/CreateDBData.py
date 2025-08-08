import pyodbc
import os
import sys
import pandas as pd  # Import pandas for DataFrame handling
import config  # Import config module for database connection details

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


# Add EventLog
def create_eventlogs_data():
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        cursor.execute("EXEC sp_Add_EventLog ?", (provincecode.strip()))

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
  

# Add Transaction
def create_transaction_data():
     # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        #cursor.execute("EXEC sp_Generic_GetPoliceStationsPerProvince ?", (provincecode.strip()))

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
  

# Add UsereName and Password for Admin
def create_newuser_data():
     # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        #cursor.execute("EXEC sp_Generic_GetPoliceStationsPerProvince ?", (provincecode.strip()))

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
  

# Add or Update User Roles
def create_addupdateuserrole_data():
     # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        #cursor.execute("EXEC sp_Generic_GetPoliceStationsPerProvince ?", (provincecode.strip()))

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
  
