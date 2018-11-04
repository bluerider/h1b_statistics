import csv

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