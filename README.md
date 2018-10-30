# Table of Contents
1. [Problem](README.md#Problem)
2. [Approach](README.md#Approach)
3. [Run Instructions](README.md#Instructions)
4. [Run Tests](README.md#Tests)
5. [Usage](README.md#Usage)
6. [Questions?](README.md#questions?)

# Problem

Expertise in the diversified US economy is of high demand. One method of filling a perceived skill gap is to attract foreign talent using H1B (H-1B, H-1BA, E-3) visas. Tracing the demographics of which professions are in need of talents as well as which are more frequently certified by the United States Department of Labor can provide valuable insight towards past, current, and future economic growth. 

# Approach
## Overview
In order to obtain quantitative measures of H1B visas certifications, I obtained data from  [United States Department of Labor](https://www.foreignlaborcert.doleta.gov/performancedata.cfm). I extracted the **Working State**, **Occupation Name**, as well as **Status of Certification** fields to determine states with higher frequencies of foreign labor **H1B visa certifications**, as well as which **occupations** were most likely to be certified. By compiling the frequencies of H1B certifications per **state** and **occupation name**, I was able to obtain the **percentages** and **counts** of the **top 10 states** and the **top 10 occupations** for the years 2014-2016.

# Instructions
1. Download data from [Google Drive](https://drive.google.com/drive/folders/1Nti6ClUfibsXSQw5PUIWfVGSIrpuwyxf?usp=sharing) to the **input** directory. If the files were downloaded as a **.zip** file, remember to extract them beforehand.
2. Run `bash run.sh` to analyze the data.
3. Two output files summarizing the analysis will be written to:
	 * `output/top_10_occupations.txt` : Top 10 occupations for certified visa applications 
     ```
        TOP_OCCUPATIONS;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        COMPUTER SYSTEMS ANALYSTS;107736;20.0%
        SOFTWARE DEVELOPERS, APPLICATIONS;88806;16.0%
        COMPUTER PROGRAMMERS;81032;15.0%
        COMPUTER OCCUPATIONS, ALL OTHER;50277;9.0%
        SOFTWARE DEVELOPERS, SYSTEMS SOFTWARE;15364;3.0%
        MANAGEMENT ANALYSTS;12037;2.0%
        ACCOUNTANTS AND AUDITORS;9841;2.0%
        NETWORK AND COMPUTER SYSTEMS ADMINISTRATORS;9494;2.0%
        FINANCIAL ANALYSTS;8194;1.0%
     ```

	* `output/top_10_states.txt` : Top 10 states for certified visa applications
    ```
	    TOP_STATES;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE
        CA;289944;18.0%
        TX;159851;10.0%
        NY;141165;9.0%
        NJ;119880;8.0%
        IL;85213;5.0%
        MA;59145;4.0%
        GA;58972;4.0%
        PA;58454;4.0%
        WA;55193;4.0%
    ```
         
# Tests
I highly suggest running `bash insight_testsuite/run_tests.sh` to ensure the program is functioning properly. It should **pass** all its tests.
        
# Usage

##  Analyzing a single file
While the default behavior for `h1b_countin.py` is to analyze data in ``input``, it is sometimes desirable to analyze single H1B visa years.
1. Obtain data from [United States Department of Labor](https://www.foreignlaborcert.doleta.gov/performancedata.cfm)
2.  Convert the .xslx data into **semi-colon separated** values `";"` `.csv` file. 
3.  Run `h1b_countin.py` script with the following commands
`python3 src/h1b_countin.py <input file> <state_output_file> <occupation_output_file>`
4. Obtain the output files specified in `<state_output_file>` and `<occupation_output file>`.

## Analyzing multiple files
`h1b_countin.py` will analyze all files in `input` as its default behavior. Simply add additional data in a **semi-color-separated** format `";"` `.csv` file into the `input` directory and run `python3 h1b_countin.py`.

# Questions/FAQ
1. *I've encountered an error in your program!*
	Please file a bug request with representative data and detailed instructions to replicate the error.
2. *I am having strange field separators in my the output text files. What can the problem be?*
	Please ensure you are using python3 when running `h1b_count.py`. Otherwise file a bug report with representative data and detailed instructions to replicate the error.
3. *Two digit precision is not enough for frequencies of H1B visa calculations, can I have higher precision?*
	Yes, although such precision will require a slight modification of the `h1b_count.py`. Future versions will probably include a configuration file.