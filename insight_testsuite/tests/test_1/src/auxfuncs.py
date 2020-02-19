#--------------------Declarations of classes and containers used in the program----------------#

class Entry:
    def __init__(self, border, date, measure, value, average):
        self.border = border
        self.date = date
        self.measure = measure
        self.value = int(value)
        self.average = average
        
def get_border_date_measure(filename):
    master_dict = {}
    f = open(filename, 'r')
    f.readline()
    currentdate = str(-1)
    while f:
        line = f.readline()
        if not line:
            break
        cols = line.split(",")
        border = cols[3]
        date = cols[4].split(" ")[0]
        if currentdate!=date:
            currmonth_bm = {}
            currentdate = date
        measure = cols[5]
        value = int(cols[6])
        bm_key = border + " " + measure
        key = border + "," + date + "," + measure
        if bm_key in currmonth_bm:
            master_dict[key] += value
        else:
            currmonth_bm[bm_key] = 1.0
            master_dict[key] = value
    return master_dict
    
def generate_output_records(master_dict):
    cumsum_measures = {}
    output = []
    months_passed = 0
    currentdate = str(-1)
    key_strings = list(master_dict.keys())
    for i in range(len(key_strings)-1, -1, -1):
        measure = key_strings[i].split(",")[2]
        date = key_strings[i].split(",")[1]
        border = key_strings[i].split(",")[0]
        if(currentdate == "-1"):
            currentdate = date
        border_measure = border + " " + measure
        if date!=currentdate:
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
        output.append(Entry(border, date, measure, master_dict[key_strings[i]], avg))
    return output
        
def write_to_file(filename, output_records_sorted):
    fout = open(filename, 'w')
    fout.write("Border,Date,Measure,Value,Average\n")
    for i in range(len(output_records_sorted)-1, -1, -1):
        fout.write(output_records_sorted[i].border + "," + output_records_sorted[i].date + " 12:00:00 AM," + output_records_sorted[i].measure + "," + str(output_records_sorted[i].value) + "," + str(output_records_sorted[i].average) + "\n")
