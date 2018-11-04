#!/bin/python

## load some libraries
import sys, os, csv

################ Main Insertion Point #####################
def main():
    ## intialize some empty variables
    state_count_dict = {}
    soc_count_dict = {}
    
    ## parse the cmdline
    try:
        input_paths, state_outfile, soc_outfile = parseArgs(sys.argv)
    except:
        print("Failed to parse the cmdline with : ", sys.argv)
        return
   
    ## extract data from input files into dictionaries
    try:
        for path in input_paths:
            print("Reading : ", path)
            try:
                ## get the dictionary array from reading a file
                dict_array = readFile2(path,
                                      state_count_dict = state_count_dict,
                                      soc_count_dict = soc_count_dict)
            except:
                print("Failed to read : ", path, "Not using data from ", path)
                return
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
    for out_file, header, dictionary, percentages, array in zip([state_outfile, soc_outfile],
                                                                [['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'],
                                                                 ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']],
                                                                [state_count_dict, soc_count_dict],
                                                                [top_state_percentages, top_soc_percentages],
                                                                [top_states, top_soc]):
        try:
            print("Writing results to : ", out_file)
            writeFile(out_file,
                      header,
                      [[key, dictionary[key], percentages[key]] for key in array])
        except:
            print("Failed to write to : ", out_file)
            return
    
    print("Done with analysis!")
    
###########################################################

################ Functions ################################
## technically these functions should be in a separate    #
## script to import since this would allow the use of     #
## py_cache but external libraries are specificially      #
## forbidden                                              #
###########################################################

## process cmdline arguments
## return the needed input and output file paths
def parseArgs(args):
    ## set initial values
    input_path = "input"
    state_outfile = "output/top_10_states.txt"
    soc_outfile = "output/top_10_occupations.txt"
    
    if len(args) > 1:
        input_path = args[1]
    ## get the soc input file path
    if len(args) > 2:
        state_outfile = args[2]
    ## get the soc output file path
    if len(args) > 3:
        soc_outfile = args[3]
    ## we don't support more than 3 arguments
    if len(args) > 4:
        print("Unused arguments : ", args[4:])
    
    ## if input path is a directory
    ## retrieve an array of all input files
    ## only goes one dir deep
    if os.path.isdir(input_path):
        input_paths = getFiles(input_path, [])
    else:
        input_paths = [input_path]
        
    ## return needed paths
    return input_paths, state_outfile, soc_outfile
    

## write csv files
## takes the output file path
## takes the header for the output file
## takes an array of lines
def writeFile(path,
              header,
              array):
    with open(path, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';', quotechar='"')
        csvwriter.writerow(header)
        for line in array:
            csvwriter.writerow(line)

## get all csv files in the input directory
## returns an array of file paths [file1, file2, ...]
def getFiles(path,
             file_paths = []
            ):
    ## get the files in the path
    files = os.listdir(path)
    for file in files:
        ## filter only for .csv files
        if file.endswith('.csv'):
            ## make a usable file path
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
        ## parse the header
        header = next(csvfile)
        ## the column indices change for the csv files
        ## we'll need to determine them from the first line
        ## loop through the split_line to find our needed values
        ## if it doesn't find them, we use the defaults specified
        ## in the function parameters
        for index in range(len(header)):
            if header[index].upper() == "STATUS" or header[index].upper() == "CASE_STATUS":
                status_index = index
            if header[index].upper() == "WORKSITE_STATE" or header[index].upper() == "PRIMARY_WORKSITE_STATE" or header[index].upper() == "LCA_CASE_WORKLOC1_STATE":
                state_index = index
            if header[index] == "LCA_CASE_SOC_NAME" or header[index].upper() == "SOC_NAME":
                soc_index = index
        ## parse line by line
        for split_line in csvfile:
            ## check if we are certified
            if split_line[status_index] == "CERTIFIED":
                ## handle case sensitivity
                soc = split_line[soc_index].upper()
                state = split_line[state_index].upper()
                ## if we encounter a key in the dictionary
                ## increase keys' value by 1
                ## otherwise add the key to the dictionary
                if soc in soc_count_dict:
                    soc_count_dict[soc] += 1
                else:
                    soc_count_dict[soc] = 1
                if state in state_count_dict:
                    state_count_dict[state] += 1
                else:
                    state_count_dict[state] = 1
                    
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
        ## round to 2 digits
        percentage = round(dictionary[key] / total, 2)
        ## convert to percentages
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
        top_ten = sorted_vals[0:10]    
    
    ## return the top 10 keys
    return top_ten

###########################################################

## run the main insertion function
if __name__ == '__main__':
    main()
