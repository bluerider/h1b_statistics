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
