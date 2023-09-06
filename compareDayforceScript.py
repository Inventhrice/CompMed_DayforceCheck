import pandas as pd
import csv
import sys

def findDiscrep(wrk1, rowOne, wrk2, rowTwo):
    msg = ""
    if wrk1.iloc[rowOne, 1] != wrk2.iloc[rowTwo, 1]:
        msg += "Changed display name. "
    if wrk1.iloc[rowOne, 2] != wrk2.iloc[rowTwo, 2]:
        msg += "Changed AD name. "
    if wrk1.iloc[rowOne, 3] != wrk2.iloc[rowTwo, 3]:
        msg += "Changed department. "
    if wrk1.iloc[rowOne, 4] != wrk2.iloc[rowTwo, 4]:
        msg += "Changed position. "
    if wrk1.iloc[rowOne, 5] != wrk2.iloc[rowTwo, 5]:
        msg += "Changed manager. "
    if wrk1.iloc[rowOne, 6] != wrk2.iloc[rowTwo, 6]:
        msg += "Changed status. "
    return msg

def addMsgToRow(row, discrepMsg, adMsg):
    temp = row.tolist()
    temp.append(discrepMsg)
    temp.append(adMsg)
    return temp


    
wrk1 = sys.argv[1]
wrk1reader = pd.read_csv(wrk1)

wrk2 = sys.argv[2] 
wrk2reader = pd.read_csv(wrk2)

comp = ".\\compare.csv"
compFile = open(comp, 'w', newline='')

adFile = pd.read_csv(".\\ADUsers.csv")

if(len(wrk1reader) < len(wrk2reader)):
    temp = wrk1reader
    wrk1reader = wrk2reader
    wrk2reader = temp

wrk1Lim = len(wrk1reader)
wrk2Lim = len(wrk2reader)

columnNames = wrk1reader.columns.values.tolist()
columnNames.append("Reasons")
columnNames.append("Is an AD user?")

compwriter = csv.writer(compFile)
compwriter.writerow(columnNames)

adMsg = ""

rowToWrite = wrk1reader.loc[0]
rowTwo = 0

#print(adFile['SamAccountName'].values)

for rowOne in range(wrk1Lim):
    adMsg =  "Yes" if wrk1reader.iloc[rowOne,2].lower() in adFile['SamAccountName'].values else "No"
    if rowTwo < wrk2Lim:
        wrk1num = wrk1reader.iloc[rowOne,0]
        wrk2num = wrk2reader.iloc[rowTwo,0]

        if wrk1num != wrk2num:
            if not (wrk1num in wrk2reader['number'].values):
                compwriter.writerow(addMsgToRow(wrk1reader.loc[rowOne], "New Entry", adMsg))
                rowTwo -= 1
            else:
                val = wrk2reader.loc[wrk2reader['number'] == wrk1num].index
                if rowOne < val:
                    while rowTwo != val:
                        adMsg = "Yes" if wrk2reader.iloc[rowTwo,2].lower() in adFile['SamAccountName'].values else "No"
                        compwriter.writerow(addMsgToRow(wrk2reader.loc[rowTwo], "Entry Removed", adMsg))
                        rowTwo += 1
                else:
                    while rowOne != val:
                        compwriter.writerow(addMsgToRow(wrk1reader.loc[rowOne], "New entry", adMsg))
                        rowOne += 1
                
        else:
            discrepMsg = findDiscrep(wrk1reader, rowOne, wrk2reader, rowTwo)
            if discrepMsg != "":
                compwriter.writerow(addMsgToRow(wrk1reader.loc[rowOne], discrepMsg, adMsg))
        rowTwo += 1
    else:
        compwriter.writerow(addMsgToRow(wrk1reader.loc[rowOne], "New entry", adMsg))

compFile.close()
