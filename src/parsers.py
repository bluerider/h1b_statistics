import os
import imports

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
        input_paths = imports.getFiles(input_path, [])
    else:
        input_paths = [input_path]
        
    ## return needed paths
    return input_paths, state_outfile, soc_outfile