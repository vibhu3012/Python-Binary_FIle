from datetime import datetime
import os
import sys
import pickle
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
import subprocess
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tabulate'])
from tabulate import tabulate
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#checks
#PK - Primary Key
#OLS = Only Letters And Spaces
#ON - Only Numbers
#NLZ - No Leading Zeroes
#CH - Choice
#DEC - Decimal Number
#LEN - Length
#DATE - Date
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
fields = ['Phone Number','Name','Nickname','Gender(M,F,O)','Address','Date of Birth(YYYY/MM/DD)','Type','Company Name','Designation','Office Address']
checks = ['PK0/ON/NLZ/LEN10','OLS','','CH("M","F","O")','','DATE','OLS','','','']
searchChecks = ['ON','OLS','','CH("M","F","O")','','DATE','OLS','','','']
strSearch = [True,True,True,True,True,False,True,True,True,True]
number = [False,False,False,False,False,False,False,False,False,False]
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
sortAccTo = 1
primaryKey = 0
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def isAllowed(value,valueChecks):
    for check in valueChecks.split('/'):
        if check[0:2] == 'PK':
            data = readAllData()
            col = int(check[2:])
            for record in data:
                if record[col] == value:
                    return '(Primary key already exists)'
        if check == 'OLS':
            for char in value:
                if not char.isalpha() and not char == ' ':
                    return '(Input contains characters other than letters and spaces)'
        if check == 'ON':
            for char in value:
                if not char.isdigit():
                    return '(Input contains characters)'
        if check == 'NLZ':
            if len(value) > 0 and value[0] == '0':
                return '(Input contains leading zeroes)'
        if check[0:2] == 'CH':
            if value not in eval(check[2:]):
                return '(Option does not exist)'
        if check == 'DEC':
            try:
                float(value)
            except:
                return '(Not a decimal number)'
        if check[0:3] == 'LEN':
            t = int(check[3:])
            if not len(value) == t:
                return '(Length is not '+str(t)+')'
        if check == 'DATE':
            t = value.split('/')
            try:
                datetime(int(t[0]),int(t[1]),int(t[2]))
            except:
                return '(Date does not exist)'
    return 'Allowed'
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def readAllData():
    data = []
    try:
        fin = open('records.dat','rb')
    except FileNotFoundError:
        return []
    while True:
        try:
            data += pickle.load(fin)
        except EOFError:
            fin.close()
            return data
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def deleteAllData():
    if os.path.isfile('records.dat'):
        os.remove('records.dat')
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def dumpData(data):
    deleteAllData()
    with open('records.dat','wb') as fout:
        pickle.dump(data,fout)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def addData(record):
    oldData = readAllData()
    for i in range(len(oldData)):
        if record[sortAccTo] < oldData[i][sortAccTo]:
            newData = oldData[:i] + [record] + oldData[i:]
            newPos = i
            break
    else:
        newData = oldData + [record]
        newPos = len(oldData)
    dumpData(newData)
    return newPos
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def displayData(data):
    print(tabulate([fields] + data, headers = 'firstrow'))
    print()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def inputData():
    newRecord = []
    for i in range(len(fields)):
        value = input('Enter '+fields[i]+': ')
        isAllowedOutput = isAllowed(value,checks[i])
        while not isAllowedOutput == 'Allowed':
            print('Invalid Entry, Please Try Again'+isAllowedOutput+'\n')
            value = input('Enter '+fields[i]+': ')
            isAllowedOutput = isAllowed(value,checks[i])
        newRecord.append(value)
    addData(newRecord)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def deleteData(ID):
    oldData = readAllData()
    for i in range(len(oldData)):
        if oldData[i][primaryKey] == ID:
            newData = oldData[:i] + oldData[i+1:]
            break
    else:
        return False
    dumpData(newData)
    return True
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def compSearchMenu(fieldNo):
    print('1: Search exact value')
    print('2: Search greater than entered value')
    print('3: Search less than entered value')
    print('4: Back')

    ch = input('Please choose an option: ')
    while ch not in [str(i) for i in range(1,5)]:
        print('Invalid Option, Please Try Again\n')
        ch = input('Please choose an option: ')
    ch = int(ch)

    if ch == 4:
        return True

    searchValue = input('Enter the value to be searched: ')
    isAllowedOutput = isAllowed(searchValue,searchChecks[fieldNo])
    while not isAllowedOutput == 'Allowed':
        print('Invalid Entry, Please Try Again'+isAllowedOutput+'\n')
        searchValue = input('Enter the value to be searched: ')
        isAllowedOutput = isAllowed(searchValue,searchChecks[fieldNo])
            
    if number[fieldNo]:
        data = readAllData()
        searchedData = []
        for i in range(len(data)):
            if ch == 1 and float(searchValue) == float(data[i][fieldNo]):
                searchedData.append(data[i])
            if ch == 2 and float(searchValue) < float(data[i][fieldNo]):
                searchedData.append(data[i])
            if ch == 3 and float(searchValue) > float(data[i][fieldNo]):
                searchedData.append(data[i])
        if len(searchedData) == 0:
            print('No Such Record Found!\n')
            return
    else:
        data = readAllData()
        searchedData = []
        for i in range(len(data)):
            if ch == 1 and searchValue == data[i][fieldNo]:
                searchedData.append(data[i])
            if ch == 2 and searchValue < data[i][fieldNo]:
                searchedData.append(data[i])
            if ch == 3 and searchValue > data[i][fieldNo]:
                searchedData.append(data[i])
        if len(searchedData) == 0:
            print('No Such Record Found!\n')
            return
    print()
    print(len(searchedData),'Records Found!')
    print('Sorting according to: ' + fields[sortAccTo] + '\n')
    displayData(searchedData)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def searchMenu():
    for i in range(len(fields)):
        print(str(i+1)+': Search by '+fields[i])
    print(str(len(fields)+1)+': Back')

    inp = input('Please choose an option: ')
    while inp not in [str(i) for i in range(1,len(fields)+2)]:
        print('Invalid Option, Please Try Again\n')
        inp = input('Please choose an option: ')
    inp = int(inp)
    print()
    
    if inp == len(fields)+1:
        return True

    inp-=1
    if strSearch[inp]:
        searchValue = input('Enter the value to be searched: ')
        isAllowedOutput = isAllowed(searchValue,searchChecks[inp])
        while not isAllowedOutput == 'Allowed':
            print('Invalid Entry, Please Try Again'+isAllowedOutput+'\n')
            searchValue = input('Enter the value to be searched: ')
            isAllowedOutput = isAllowed(searchValue,searchChecks[inp])
        data = readAllData()
        searchedData = []
        for i in range(len(data)):
            if searchValue in data[i][inp]:
                searchedData.append(data[i])
        if len(searchedData) == 0:
            print('No Such Record Found!\n')
            return
        print()
        print(len(searchedData),'Records Found!')
        print('Sorting according to: ' + fields[sortAccTo] + '\n')
        displayData(searchedData)
    else:
        while not compSearchMenu(inp):
            pass
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def editMenu(pos):
    data = readAllData()
    print('Sorting according to: ' + fields[sortAccTo] + '\n')
    displayData([data[pos]])
    
    for i in range(len(fields)):
        print(str(i+1)+': Edit '+fields[i])
    print(str(len(fields)+1)+': Back')

    ch = input('Please choose an option: ')
    while ch not in [str(i) for i in range(1,len(fields)+2)]:
        print('Invalid Option, Please Try Again\n')
        ch = input('Please choose an option: ')
    ch = int(ch)
    print()

    if ch == len(fields)+1:
        return True

    ch-=1
    newValue = input('Enter new value: ')
    isAllowedOutput = isAllowed(newValue,checks[ch])
    while not isAllowedOutput == 'Allowed':
        print('Invalid Entry, Please Try Again'+isAllowedOutput+'\n')
        newValue = input('Enter new value: ')
        isAllowedOutput = isAllowed(newValue,checks[ch])
    print()
    
    oldData = data[pos]
    deleteData(data[pos][primaryKey])
    oldData[ch] = newValue
    newPos = addData(oldData)

    print('Record Editted!\n')

    if not pos == newPos:
        return newPos
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def sortData():
    data = readAllData()
    deleteAllData()
    for record in data:
        addData(record)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def sortMenu():
    for i in range(len(fields)):
        print(str(i+1)+': Sort According to '+fields[i])
    print(str(len(fields)+1)+': Back')
    
    ch = input('Please choose an option: ')
    while ch not in [str(i) for i in range(1,len(fields)+2)]:
        print('Invalid Option, Please Try Again\n')
        ch = input('Please choose an option: ')
    ch = int(ch)
    print()
    
    if ch == len(fields)+1:
        return True
        
    ch-=1
    global sortAccTo
    sortAccTo = ch
    sortData()
    print('Records Sorted!')
    print('Sorting according to: ' + fields[sortAccTo] + '\n')
    displayData(readAllData())
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def menu():
    print('1: Add a record')
    print('2: Display all records')
    print('3: Search within records')
    print('4: Delete a record')
    print('5: Delete all records')
    print('6: Edit a record')
    print('7: Sort According to a field')
    print('8: Exit')

    inp = input('Please choose an option: ')
    if inp not in [str(i) for i in range(1,9)]:
        print('Invalid Option\n')
        return
    inp = int(inp)
    print()

    if inp == 1:
        inputData()
        print('\nRecord Added!\n')

    if inp == 2:
        data = readAllData()
        if len(data) == 0:
            print('No Records Found!\n')
            return
        print(len(data),'Records Found!')
        print('Sorting according to: ' + fields[sortAccTo] + '\n')
        displayData(data)

    if inp == 3:
        while not searchMenu():
            pass
    
    if inp == 4:
        ID = input('Enter '+fields[primaryKey]+': ')
        isAllowedOutput = isAllowed(ID,searchChecks[primaryKey])
        while not isAllowedOutput == 'Allowed':
            print('Invalid Entry, Please Try Again'+isAllowedOutput+'\n')
            ID = input('Enter '+fields[primaryKey]+': ')
            isAllowedOutput = isAllowed(ID,searchChecks[primaryKey])
        if not deleteData(ID):
            print('\nNo Such Record Found!\n')
        else:
            print('\nRecord Deleted!\n')

    if inp == 5:
        deleteAllData()
        print('All Records Deleted!\n')

    if inp == 6:
        ID = input('Enter '+fields[primaryKey]+': ')
        data = readAllData()
        for i in range(len(data)):
            if data[i][primaryKey] == ID:
                pos = i
                break
        else:
            print('\nNo Such Record Found!\n')
            return
        print()
        while True:
            output = editMenu(pos)
            if type(output) == int:
                pos = output
            elif output:
                break

    if inp == 7:
        while not sortMenu():
            pass

    if inp == 8:
        sys.exit()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
sortData()
while True:
    menu()
