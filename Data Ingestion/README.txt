The only prerequisites to use this program is to have Python 3 and pip installed on the local machine.

I have written the program for this task in python. Please run the script by executing openaq_support.bat, which will use pip to install the two non-standard dependencies, Pandas and Requests.

Pandas:
https://pandas.pydata.org/

Requests:
https://2.python-requests.org/en/master/

 This target folder is where all output files will be saved.

Next another prompt window will appear which will ask for a .txt file. This file should contain have all desired countries listed in it as either the 2 letter ISO Code, or the full name. This is case insensitive, 
though for full country names, the name will have to appear with the same spelling from the library of country names to iso codes included in the program. For example, 'United States' as well as 'UNITED STATES' and 'US' will 
be accepted, but 'United States of America' will not. Handling for various different inputs would be very time consuming so I have decided to leave this as is for now.

When the list of countries has been selected, the script will run, will return the results for all functions in main() of the file. The program will also output a text file called Countries_without_Sources.txt which will 
list any countries passed by the user, for which a source url was not found in the API Call. 