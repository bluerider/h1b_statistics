#!/bin/python

## load some libraries
import sys

## import python modules in src
import imports, exports, algorithms, parsers

################ Main Insertion Point #####################
def main():
    ## intialize some empty variables
    state_count_dict = {}
    soc_count_dict = {}
    
    ## parse the cmdline
    try:
        input_paths, state_outfile, soc_outfile = parsers.parseArgs(sys.argv)
    except:
        print("Failed to parse the cmdline with : ", sys.argv)
        return
   
    ## extract data from input files into dictionaries
    try:
        for path in input_paths:
            print("Reading : ", path)
            try:
                ## get the dictionary array from reading a file
                dict_array = imports.readFile2(path,
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
        top_soc = algorithms.getTopTen(soc_count_dict)
        top_states = algorithms.getTopTen(state_count_dict)
    except:
        print("Failed to sort and calculate top 10 values!")
        return
    
    ## get percentages
    print("Calculating percentages...")
    try:
        top_soc_percentages = algorithms.getPercentages(top_soc, soc_count_dict)
        top_state_percentages = algorithms.getPercentages(top_states, state_count_dict)
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
            exports.writeFile(out_file,
                              header,
                              [[key, dictionary[key], percentages[key]] for key in array])
        except:
            print("Failed to write to : ", out_file)
            return
    
    print("Done with analysis!")

## run the main insertion function
if __name__ == '__main__':
    main()
