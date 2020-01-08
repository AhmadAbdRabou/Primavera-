#loadschema.py

# Loading built-in packages
from os.path import dirname, join
# Loading Pandas package
import pandas as pd

def loadschema():
    ''' LoadSchema loads Excel-book into a List of Dictionaries
    Each sheet of the Excel-book contains an empty table (columns' names only) with table name is the sheet name
    LoadSchema record the sheet / table name as dictionary key and column's names as the value of the dictionary key in form of list
    Each dictionary contains one table only
    All dictionaries are appened to one list with is returned by the end of the execution

    Note: The Excel-book with name 'schema.xlsx' contains few tables of original Primavera schema
        and later when the user loads the actual project, only the tables from 'schema.xlsx'
        will be updated. This is because of two reasons:
        One, conflict of tables' names due to different version of Primavera schema or difference of schema utilization from one project to another
        Two, better loading performance
        Nevertheless, for loaded projects, all tables will be available to the user to download in Excel format''' 
    # Define the path to the Excel-book, which is in the same folder as the module
    schema_file = join(dirname(__file__), "schema.xlsx")
    # Open Excel-book 
    with pd.ExcelFile(schema_file) as xl:
        # Initiate return container
        schema = []
        # Access each sheet in the Excel-book
        for sheet in xl.sheet_names:
            # Load the sheet into Pandas DataFrame
            data = xl.parse(sheet)
            # Create Dictionary with key=Excel-sheet name and value=List of column's names
            table = {sheet : list(data.columns.values)}
            # Append the Dictionary to the return container
            schema.append(table)
    # Return
    return schema
