#!/bin/python

## load some libraries
import sys, os, csv

################ Main Insertion Point #####################
def main():
    ## intialize some empty variables
    state_count_dict = {}
    soc_count_dict = {}
    
    ## parse the cmdline
    ## use custom input files if available
    if len(sys.argv) > 1:
        paths = [sys.argv[1]]
        print("Using : ", paths)
    else:
        ## get the directories in the input directory
        try:
            paths = getFiles("input", [])
            print("Found input files : ", paths)
        except:
            print("Failed to find input files!")
            return
    ## loop for all paths
    try:
        for path in paths:
            print("Reading : ", path)
            try:
                ## get the dictionary array from reading a file
                dict_array = readFile2(path,
                                      state_count_dict = state_count_dict,
                                      soc_count_dict = soc_count_dict)
            except:
                print("Failed to read : ", path, "Not using data from ", path)
    except:
        print("Failed to read input files!")
        return
    ## get top 10 values
    print("Calculating top 10 values...")
    try:
        top_soc = getTopTen(soc_count_dict)
        top_states = getTopTen(state_count_dict)
    except:
        print("Failed to sort and calculate top 10 values!")
        return
    ## get percentages
    print("Calculating percentages...")
    try:
        top_soc_percentages = getPercentages(top_soc, soc_count_dict)
        top_state_percentages = getPercentages(top_states, state_count_dict)
    except:
        print("Failed to calculate percentages!")
        return
    ## write values to csv file
    ## use output file if supplied
    if len(sys.argv) > 2:
        soc_outfile = sys.argv[2]
    else:
        soc_outfile = "output/top_10_occupations.txt"
    print("writing results to", soc_outfile)
    try:
        with open(soc_outfile, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"')
            csvwriter.writerow(['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])
            for key in top_soc:
                csvwriter.writerow([key, soc_count_dict[key], top_soc_percentages[key]])
    except:
        print("Failed to write to", soc_outfile)
        return
    ## use output file if supplied
    if len(sys.argv) > 3:
        state_outfile = sys.argv[3]
    else:
        state_outfile = "output/top_10_states.txt"
    print("Writing results to", state_outfile)
    try:
        with open(state_outfile, 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"')
            csvwriter.writerow(['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'])
            for key in top_states:
                csvwriter.writerow([key, state_count_dict[key], top_state_percentages[key]])
    except:
        print("Failed to write to", state_outfile)
        return
    print("Check ouput/ for analysis")
    
###########################################################

################ Functions ################################
## technically these functions should be in a separate    #
## script to import since this would allow the use of     #
## py_cache but external libraries are specificially      #
## forbidden                                              #
###########################################################

## get all csv files in the input directory
## returns an array of file paths [file1, file2, ...]
def getFiles(path,
             file_paths = []
            ):
    files = os.listdir(path)
    for file in files:
        if file.endswith('.csv'):
            file_paths.append(os.path.join(path, file))
            
    ## return the file paths
    return file_paths

## read a file
## dictionaries can be passed in to allow updating data
## returns an array of two dicts [state_counts, soc_counts]
## #################### dict layout #########################
## # {state, count}                                         #
## # {soc, count}                                           #
## ##########################################################
def readFile2(path,
             state_count_dict = {},
             soc_count_dict = {},
             status_index = 2,
             state_index = 12,
             soc_index = 24,
            ):
    ## open file for parsing
    with open(path) as file:
        csvfile = csv.reader(file, delimiter=';', quotechar='"')
        ## parse line by line
        for split_line in csvfile:
            ## check if we're at the first line
            if split_line[0] != "":
                ## if we aren't proceed to parse the data
                ## check if we are certified
                if split_line[status_index] == "CERTIFIED":
                    ## handle case sensitivity
                    soc = split_line[soc_index].upper()
                    state = split_line[state_index].upper()
                    if soc in soc_count_dict:
                        soc_count_dict[soc] += 1
                    else:
                        soc_count_dict[soc] = 1
                    if state in state_count_dict:
                        state_count_dict[state] += 1
                    else:
                        state_count_dict[state] = 1
            ## the column indices change for the csv files
            ## we'll need to determine them from the first line
            else:
                ## loop through the split_line to find our needed values
                ## if it doesn't find them, we use the defaults specified
                ## in the function parameters
                for index in range(len(split_line)):
                    if split_line[index] == "STATUS" or split_line[index] == "CASE_STATUS":
                        certified_index = index
                    #if split_line[index] == "LCA_CASE_EMPLOYER_STATE" or split_line[index] == "EMPLOYER_STATE":
                    if split_line[index] == "WORKSITE_STATE" or split_line[index] == "PRIMARY_WORKSITE_STATE" or split_line[index] == "LCA_CASE_WORKLOC1_STATE":
                        state_index = index
                    if split_line[index] == "LCA_CASE_SOC_NAME" or split_line[index] == "SOC_NAME":
                        soc_index = index
                        
    ## return the dictionaries in an array
    return [state_count_dict, soc_count_dict]

## calculate the percentages
## we don't allow initial total values to be passed in
## due to dictionary specificity
## returns a dictionary {keys, percentage}
def getPercentages(keys,
                   dictionary
                  ):
    ## set some initial values
    total = 0
    
    ## loop to get the sum
    for key in dictionary:
        total += dictionary[key]
        
    ## loop to get percentages
    percentages = {}
    for key in keys:
        ## main two digit rounding
        percentage = round(dictionary[key] / total, 2)
        percentages[key] = "{:.1%}".format(percentage)
    
    ## retun the percentages array
    return percentages

## get the ten most frequent states/soc
## returns an array [key1, key2, ...]
def getTopTen(dictionary):
    
    ## sort the dictionary by its keys
    ## sort first by alphabet
    sorted_chars = sorted(dictionary, reverse=False)
    ## sort by values
    sorted_vals = sorted(sorted_chars, reverse=True, key = dictionary.get)
    ## check if we have 10 entries to return
    if len(sorted_vals) < 10:
        top_ten = sorted_vals
    else:
        ## if we have more than 10, return the top ten
        top_ten = sorted_vals[0:9]
    ## we'll sort again alphabetically
    
    
    ## return the top 10 keys
    return top_ten

###########################################################

if __name__ == '__main__':
    main()