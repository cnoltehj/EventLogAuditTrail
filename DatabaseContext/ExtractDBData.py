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

    print(server, database, username, password)

    # Establish database connection
    cnxn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return cnxn


# Get Totaltransactionsperuserperdaterange
def read_totaltransactionsperuserperdaterange_data( UserId: int, StartDate: str, EndDate: str
                               ):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        print(f"  UserId={UserId}, StartDate={StartDate}, EndDate={EndDate}")
        cursor.execute("EXEC sp_Get_TotalTransactions_PerUser_PerDateRange ?,?,?", (
            int(UserId),           # 1 -> @iUserId
            str(StartDate),        # 2 -> @StartDate
            str(EndDate),       # 3 -> @EndDate
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


# Get EventLog per User
def read_eventlogsperuser( UserId: int, StartDate: str, EndDate: str):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        print(f"  UserId={UserId}, StartDate={StartDate}, EndDate={EndDate}")
        cursor.execute("EXEC sp_Get_EventLogs_PerUser ?,?,?", (
            int(UserId),           # 1 -> @iUserId
            str(StartDate),        # 2 -> @StartDate
            str(EndDate),       # 3 -> @EndDate
        ))

        #cnxn.commit() 
        
        print("Executed stored procedure ")

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


# Get EventLog per Date Range
def read_eventlogsperdate(StartDate: str, EndDate: str
                               ):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        print(f" StartDate={StartDate}, EndDate={EndDate}")
        cursor.execute("EXEC sp_Get_EventLogs_PerDate ?,?", (
            str(StartDate),     # 1 -> @StartDate
            str(EndDate),       # 2 -> @EndDate
        ))

        #cnxn.commit() 
        
        print("")

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
  

# Get Username and Password from Environment Variables
def read_userdetails_data():
     # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
       
        cursor.execute("EXEC sp_Get_UserRoles")

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
  

# Get Products List
def read_productslist_data():
      # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
       
        cursor.execute("EXEC sp_Get_ProductList")

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
  

# Get Products
def read_productslistbyprovidername_data(ProviderName : str):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
       
        cursor.execute("EXEC sp_Get_ProductList_By_ProviderName ?", (ProviderName.strip()))

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
  
# Get EventLog per Transaction Type per time period
def read_providerbyname_data(ProviderName : str):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
       
        cursor.execute("EXEC sp_Get_Provider_By_Name ?", (ProviderName.strip()))

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
  

# Get Accesslogs
def read_accesslogs_data():
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
  

# GetUserRolls
def read_userrolls_data():
     # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        cursor.execute("EXEC sp_Get_UserRoles")

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

        print(df)

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
  

# Get UserName and Password 
def read_userdetails_data():
     # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
        cursor.execute("EXEC sp_Get_UserDetails")

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
  

# Get Products
def read_usernamebyunamepword_data(UserName: str, Password: str):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
       
        cursor.execute("EXEC sp_Get_User_By_UName_Pword ?,?", (UserName.strip(), Password.strip()))

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

        # Get Products


def read_userbyid_data(UserId  : int):
    # Connect to the database
    cnxn = connect_to_database()
    cursor = cnxn.cursor()

    try:
       
        cursor.execute("EXEC sp_Get_User_By_Id ?", (UserId))

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
