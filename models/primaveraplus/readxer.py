#'readxer.py'

# Loading built-in packages
from os.path import dirname, join
# Loading Pandas package
import pandas as pd
# Importing Excel package that allow usage of .xlsx file format (after 2003)
import xlsxwriter    

def readxer(filename, load_location, extract_location):
    '''RearXER reads data from Primavera XER file and convert its tables to Excel workbook, 
       each table in a separate sheet.
    The XER file is a tab-delimited file, "\t" is used to separate values.
    Each line starts with a specific notation "%" followed by one of the following characters:
       T   -  Table   : this line contains the table name of the primavera database schema
       F   -  First   : this line contains the names of the columns of the same table above
       R   -  Row     : this line contains the data inside the table mapped to the column names
       E   -  End of File : this line represents the last line of the file and contains no other data
    The first line of the file is an exception since it has no "%" notation, still contains other 
    information such as, Primavera revision, file creation date, file owner, Primavera Database name,
    and project currency''' 
    # Assign file name to variable and use it to "open" the file in read-only mode
    file_name = filename.split(sep='.xer')[0]+'.xlsx'
    with open(join(load_location,filename), mode = 'r') as  xerfile:  #open() is built-in functin that reads txt files
        # Read the file contents into a "list" of lines
        lines = xerfile.readlines()
        # Create the output Excel file "workbook" and assign it to variable
        with xlsxwriter.Workbook(join(extract_location,file_name)) as book:
            # rowcount is the number of data rows in each table, resetted to 1 with each new table
            rowcount=1
            # Reading line by line
            for line in lines:
                #if table
                if("%T" in line):
                    rowcount=1
                    #create new excel sheet with table name
                    sheet = book.add_worksheet(line.split(sep='\t')[1].split(sep='\n')[0])
                #if table head
                elif("%F" in line):
                    #row is the row index in the active excel sheet, the value 0 indicates the first row
                    row = 0
                    #each value in the line is assigned to excel column by index and value
                    for column, value in enumerate(line.split(sep='\t')):
                        #write the value excel sheet cell designated by row & column index
                        sheet.write(row, column, value.split(sep='\n')[0])
                #if table data
                elif("%R" in line):
                    #rowcount is the row count / index, with value of 1 at each new sheet which is the second row after
                    #recorded table column names in the same sheet
                    row = rowcount
                    #each value in the line is assigned to excel column by index and value
                    for column, value in enumerate(line.split(sep='\t')):
                        #write the value excel sheet cell designated by row & column index
                        sheet.write(row, column, value.split(sep='\n')[0])
                    #move to next row
                    rowcount+=1
                #if anything else, just print the line
                else:
                    print(line)


    with pd.ExcelFile(join(extract_location,file_name)) as xl:
        if not(('OBS' and 'PROJECT' and 'PROJWBS') in xl.sheet_names):
            return "No_Project"
        elif not 'TASK' in xl.sheet_names or xl.parse('TASK').iloc[:,0].count()==0:
            return "No_Activities"
        else: return "sucess"



            
