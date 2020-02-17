from operator import itemgetter, attrgetter

f = open("../input/Border_Crossing_Entry_Data.csv", 'r')
#f = open("sample.csv", 'r')
f.readline()

master_dict = {}
cumsum_measures = {}
output = []
months_passed = 0
currentdate = str(0)

class Entry:
    def __init__(self, border, date, measure, value, average):
        self.border = border
        self.date = date
        self.measure = measure
        self.value = int(value)
        self.average = average

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
    
key_strings = list(master_dict.keys())

for i in range(len(key_strings)-1, -1, -1):
    measure = key_strings[i].split(",")[2]
    date = key_strings[i].split(",")[1]
    border = key_strings[i].split(",")[0]
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

output_sorted = sorted(output, key=attrgetter('date', 'value', 'measure', 'border'))

fout = open("../output/report.csv", 'w')
fout.write("Border,Date,Measure,Value,Average\n")
for i in range(len(output_sorted)-1, -1, -1):
    fout.write(output_sorted[i].border + "," + output_sorted[i].date + "," + output_sorted[i].measure + "," + str(output_sorted[i].value) + "," + str(output_sorted[i].average) + "\n")

    

