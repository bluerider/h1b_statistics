import os, csv

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