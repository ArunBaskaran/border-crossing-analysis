from operator import attrgetter
import sys
from auxfuncs import *
        
#-----------------------------------------------------------------------------------------------#

master_dict = get_border_date_measure(sys.argv[1])  #Read the records from the input file, and store them in an intuitive dictionary

output_records = generate_output_records(master_dict) #Calculate the monthly running average of each border-measure combo

output_records_sorted = sorted(output_records, key=attrgetter('date', 'value', 'measure', 'border'))  #Sort the records. output_records is in reverse order, so the sorting is done in asc order.

write_to_file(sys.argv[2], output_records_sorted)   #Write the report to the output file

#------------------------------------------------------------------------------------------------#
    

