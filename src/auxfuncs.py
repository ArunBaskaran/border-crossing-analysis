#--------------------Definitions of classes, containers, and functions used in the program----------------#

# Class whose objects are the columns required in the output file. Defined in order to make the sorting process more efficient
class Entry:
    def __init__(self, border, date, measure, value, average):
        self.border = border
        self.date = date
        self.measure = measure
        self.value = int(value)
        self.average = average
        
# The following function checks if the date column in the input file has mm/dd/yy hh:mm:ss AM
def validate_date(date):
    if (len(date.split(" ")) == 3 and len(date.split(" ")[0].split("/"))==3):
        mm=date.split(" ")[0].split("/")[0]
        dd=date.split(" ")[0].split("/")[1]
        yyyy=date.split(" ")[0].split("/")[2]
        return yyyy + "/" + dd + "/" + mm
    else:
        return -1
    
# The following function checks if the border column in the input file has the words Mexico or Canada in it. Designed to protect against different variants of "US-Mexico Border" and "US-Canada Border"
def validate_border(border):
    if "Mexico" in border:
        return "US-Mexico Border"
    elif "Canada" in border:
        return "US-Canada Border"
    else:
        return -1
        
# The following function reads the input file line-by-line, stores the relevant columns in a dictionary and returns the dictionary
def get_border_date_measure(filename):
    master_dict = {}  # Dictionary that will store values for unique {border-date-measure, values} combos.
    currentdate = str(-1)
    
    try:   #Safecheck 1 - To ensure that the file exists and was opened correctly
        f = open(filename, 'r')
    except IOError:
        print("Error opening the file")
        exit()
            
    f.readline()

    while f:
        line = f.readline()
        if not line:
            break
            
        cols = line.split(",")
        try:     #Safecheck 2 - To ensure that this row has 7 columns. If not, the row is skipped. This is a general safecheck to protect against missing entries. 
            len(cols)==7
        except:
            continue
            
        border = validate_border(cols[3])
        try:     #Safecheck 3 - To ensure that either Canada or Mexico is present in the border column. If not, the row is skipped.
            border != -1
        except:
            continue
        
        date = validate_date(cols[4])
        try:     #Safecheck 4 - To ensure that the date has the correct format. If not, the previous entry's date is used. 
            date != -1
        except:
            date = currentdate
        
        if currentdate!=date:
            currmonth_bm = []   #Auxillary list that is defined to hold border-measure combos for the current date iteration. Reset to new everytime a new date is encountered
            currentdate = date
        measure = cols[5]
        
        try:     #Safecheck 5 - To ensure that the number of crossings is an integer value. If not, the row is skipped. 
            value = int(cols[6])
        except:
            continue
            
        bm_key = border + " " + measure
        key = border + "," + date + "," + measure
        if bm_key in currmonth_bm:   # Check to ensure if that particular border-measure combo has been encountered for this date
            master_dict[key] += value
        else:
            currmonth_bm.append(bm_key)
            master_dict[key] = value
    return master_dict
    
# The following function generates the tuples to write to the output file
def generate_output_records(master_dict):
    cumsum_measures = {} # Dictionary that stores the running average of border-measure combos. 
    output = []  # List container to store objects of class Entry for writing to the output file
    months_passed = 0
    currentdate = str(-1)
    key_strings = list(master_dict.keys()) 
    for i in range(len(key_strings)-1, -1, -1):  # Traversing the list in the reverse order in order to generate monthly averages from the beginning
        measure = key_strings[i].split(",")[2]
        date = key_strings[i].split(",")[1]
        border = key_strings[i].split(",")[0]
        if(currentdate == "-1"):
            currentdate = date
        border_measure = border + " " + measure
        if date!=currentdate:  # Update months_passed if the date changes. Assuming that all the dates are kept to the beginning of the month.
            months_passed += 1
            currentdate = date
        if border_measure in cumsum_measures:
            temp = cumsum_measures[border_measure]/months_passed
            if(temp - int(temp) >= 0.5):
                avg = int(temp) + 1
            else:
                avg = int(temp)
            cumsum_measures[border_measure] += master_dict[key_strings[i]]
        else:
            cumsum_measures[border_measure] = master_dict[key_strings[i]]
            avg = 0
        output.append(Entry(border, date, measure, master_dict[key_strings[i]], avg))  # The record-to-be-written is stored as a tuple in the output list.
    return output
        
# The following function writes the sorted rows to the output file
def write_to_file(filename, output_records_sorted):
    fout = open(filename, 'w')
    fout.write("Border,Date,Measure,Value,Average\n")
    for i in range(len(output_records_sorted)-1, -1, -1):
        datecurr = output_records_sorted[i].date.split("/")[2] + "/" + output_records_sorted[i].date.split("/")[1] + "/" + output_records_sorted[i].date.split("/")[0] 
        fout.write(output_records_sorted[i].border + "," + datecurr + " 12:00:00 AM," + output_records_sorted[i].measure + "," + str(output_records_sorted[i].value) + "," + str(output_records_sorted[i].average) + "\n")
