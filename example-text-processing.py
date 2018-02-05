#################################################################
# Example Text Processing and Cleaning With Regexs
# example-text-processing.py
# Author: Meredith M. Paker, merpaker@gmail.com
# Last edited: 5 February, 2018
# This script demonstrates how regular expressions in
#   python can be used to clean and process an OCR'd text
#   file with scanning errors and improper line breaks.
#################################################################

import re

### DELETE LEFTOVER TEXT FROM OCR ###

# Initialize list for edited text
v_edited = []

# Open file and read in line by line
with open("V1.txt", "r", encoding = 'utf-8') as f:
    file_text = f.read()
    lines = file_text.split('\n')

    # If line has a word that is an OCR error, do not include line
    for line in lines: 
        split = line.split()
        try:
            if split[0] == "Generated":
                continue
            if split[0] == "Public":
                continue
            if split[0] == "MAINTENANCE":
                continue
            if split[0] == "Original":
                continue
            if split[0] == "NEW":
                continue
            if split[0] == "Digitized":
                continue
        except:
                pass
        try: 
            if split[1] == "MAINTENANCE":
                continue
        except:
            pass

        
        v_edited.append(line)

        

### IDENTIFY NEW SPEAKERS IN THE TESTIMONY ###

# Compile regular expressions to match patterns found in the
# text that indicate a new speaker

# This matches patterns line "Mr. Robinson." or "Mr Smith."
# '\.*' indicates an optional period after "Mr"
# ' *' indicates an option space between "Mr" and the name
# '[A-za-z]+' allows words with capital or lowercase letters of any length
# '\.' requires a period after the name, which is used in the text to indicate the end of name
re1 = re.compile('Mr\.* *[A-Za-z]+\.')
# This matches patterns like "Senator Gallinger." paralleling the above
re2 = re.compile('Senator *[A-Za-z]+\.')
# This matches "The Chairman." allowing the whole word to also be capitalized
re3 = re.compile('The *Chairman\.', re.IGNORECASE)

# Initialize empty string
output = ""

# Cycle through and split on speaker names
for line in v_edited:
    mr = re1.match(line)
    senator = re2.match(line)
    chairman = re3.match(line)
    
    # If a line matches one of the regexs, add the match to the output string
    # and add a hashtag to delimit the speaker name from the rest of the text
    if mr:
        output += "\n"
        split = line.split(mr.group(), 1)
        name = mr.group().rstrip('.')
        output += name
        output += "# "
        output += split[1]
    elif senator:
        output += "\n"
        split = line.split(senator.group(), 1)
        name = senator.group().rstrip('.')
        output += name
        output += "# "
        output += split[1]
    elif chairman:
        output += "\n"
        split = line.split(chairman.group(), 1)
        name = chairman.group().rstrip('.')
        output += name
        output += "#"
        output += split[1]
    # If a line doesn't match, it's part of the comment of the above speaker.
    # So just add it to the output
    else:
        output += line


### IDENTIFY WHEN A NEW SECTION OF TESTIMONY BEGINS ###
# Add new lines after each new section of testimony
# and cut out any text before the new testimony heading

# Initialize empty string
output2 = ""

for line in output.splitlines():
    if 'ADDITIONAL TESTIMONY' in line:
        split = line.split("ADDITIONAL TESTIMONY", 1)
        output2 += split[0]
        output2 += "\n"
        output2 += "ADDITIONAL TESTIMONY"
        output2 += split[1]
        output2 += "\n"
    if 'TESTIMONY' in line:
        split = line.split("TESTIMONY", 1)
        output2 += split[0]
        output2 += "\n"
        output2 += "TESTIMONY"
        output2 += split[1]
        output2 += "\n"
    else:
        output2 += line
        output2 += "\n"
        
        
### ADD TESTIMONY SECTION TO EACH OUTPUT LINE ###

# This matches words with all capital letters to pull the testimony
# names away from other text that might be on the line
re4 = re.compile('[A-Z]+\.* *[A-Z]+\.* *[A-Z]+\.* *[A-Z]+\.*')

output3 = ""
testimony_group = "START"
# This is the index we will increment each time a new section of testimony begins
testimony_index = 0

for line in output2.splitlines():
    if 'TESTIMONY OF' in line:
        split = line.split('TESTIMONY OF', 1)
        test_name = re4.search(split[1])
        if test_name:
            print(test_name.group())
            testimony_group = test_name.group()
            testimony_index = testimony_index + 1
    else:
        if (line != "\n") & (line != "ADDITIONAL"):
            output3 += line
            output3 += "#"
            output3 += testimony_group
            output3 += "#"
            output3 += str(testimony_index)
            output3 += "\n"


### WRITE OUTPUT TO FILE ###

v1_output = open('V1Output.txt', mode = 'a', encoding = 'utf-8')
v1_output.write(output3)
v1_output.close()
