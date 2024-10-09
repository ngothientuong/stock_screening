# This module is to clean up the first
# three rows of exported watch list from TDAmeritrade
# The file will be created in memory
#
# Syntax: delete_multiple_lines(original_file, [list of line_numbers to be deleted])
# Example:  delete_multiple_lines(r"C:\TuongSharedSpace\Trading\WatchLists\test2.csv", [0,3,7,8])
#
import os
def delete_multiple_lines(original_file, aList):
    is_skipped = False
    override_file = False
    dummy_file = original_file + '.bak'
    with open(original_file, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Line by line copy data from original file to dummy file
        counter = 0
        for line in read_obj:
            for index in range(0,len(aList)):
                if counter == aList[index]:
                    is_skipped = True
                    override_file = True
                    break
                else:
                    is_skipped = False
            if is_skipped == False:
                write_obj.write(line)
                #print(line)
            counter += 1
    # If any line is skipped then rename dummy file as original file        
    if override_file:
        os.remove(original_file)
        os.rename(dummy_file, original_file)
    else:
        os.remove(dummy_file)            
    read_obj.close()
    write_obj.close()
    del is_skipped, override_file, dummy_file, counter, index, override_file, write_obj, read_obj