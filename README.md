## Example-Text-Processing-and-Cleaning-with-Regexs
This script demonstrates how regular expressions in Python can be used to clean and process OCR text with many errors in order to generate a workable dataset. The goal in this specific example is to clean US Senate testimony to make a dataset listing the speaker in one column with their testimony in the next column. I also show how to categorize the comments by the section of testimony they are in and how to give an index for these sections.

## What you'll need

### System requirements

This is a Python script designed for Python 3, so you'll need an up-and-running Python distribution.

### Input file
The script as written requires an input file called "V1". In this case, the file is OCRd text of Senate testimony from 1913. The text delineates the speaker at the start of each comment (e.g. "Senator Gallinger") and then gives the comment. There are also various section breaks (e.g. "TESTIMONY OF TRUMAN G. PALMER—Continued."). These comments and section breaks are the text data we are interested in.

The original book printed the title of the work and the page number on the top of each page (e.g. "MAINTENANCE OF A LOBBY TO INFLUENCE LEGISLATION 1087"), which is picked up by the OCR. In the process of the book being scanned, "Digitized by Google" was printed on the PDFs, as well as the date of download from the web. The OCR also erroneously picks up all of this. Finally, the OCR software put a paragraph break at the end of each line instead of at the end of each comment in the testimony, making it difficult to distinguish the various speakers.

For your own use, feel free to any utf-8 encoded .txt file.

### Output file
The output file will be a utf-8 encoded .txt file called "V1Output". You can initialize this file beforehand by creating a blank .txt file of this name. After the script runs, the updated file will have a hashtag-separated list that can be easily imported into other software for analysis.

## How the script works

The script has four sections. The first section strips out excess information that the OCR picked up (e.g. "Digitized by Google"). The second section identifies when a new speaker begins to give a comment. The third section isolates the testimony section heading. The fourth section outputs the section of testimony and the index of the testimony to each line of output.

The head of the script just has the regex import statement. The file I/O is incorporated in the first loop.
```
import re
```

The next section opens a .txt file with a messy OCR scan and artificial line breaks. First, open and read the file, and then split by line breaks. Then, for each line, see if it contains the OCR errors. You can change these to match whatever errors your OCR scan has picked up. If a line has this excess information, skip adding the line to your final text dataset. 

In general, it's a bad idea to use "continue" statements in loops, but in this case I thought it made the code intuitive and self-documented. If you're new to programming, it could be a fun challenge to try to rewrite this section of the code without "continue" statements. 

The try/pass statements are included because some of my OCR errors appeared as the second word on the line. This is an easy way to handle checking the second word of a line when some lines only have one word.

If the line has no errors, add the line to your text dataset v_edited[].

```
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
```

The next chunk of code compiles regular expressions. The basic idea is that you describe a pattern, compile the pattern, and then "search" the whole string or "match" the first part of a string for the pattern you described. Regexs are especially useful for searching for repeated patterns backwards and forwards in a string, and they get complicated quickly! The patterns I search for here, however, are easy and should help you get a flavor for what working with regexs is like.

I compile three patterns to try to identify the changing speakers in the dataset. Fortunately, this Senate testimony indicates a new speaker by using their title, last name, and then putting a period after the name (see the example input below). So we want to match strings like "Mr. Robinson." but not "Mr. Robinson". The first pattern, re1, handles this case, and I describe the components in the code.


```
# Compile regular expressions to match patterns found in the text that indicate a new speaker

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

```

Then cycle through the lines in the text dataset. If the line matches one of the regexs, add the matched text to the output string to indicate the name of the speaker. Then add a hashtag to delimit it from the comment, which follows. If a line doesn't have a change of speaker, just add it output string as part of the preceding comment. 

This section of the code takes the artificial line breaks out, adding line breaks only to indicate a change in the speaker. This is an important step to achieving a hashtag-delimited file with one speaker and one comment on each line.

```
# Initialize empty string
output = ""

# Cycle through and split on speaker names
for line in v_edited:
    mr = re1.match(line)
    senator = re2.match(line)
    chairman = re3.match(line)
    
    # If a line matches one of the regexs, add the match to the output string
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
```

Next we want to pull out the title of each section of the testimony, e.g. "TESTIMONY OF TRUMAN G. PALMER". This is especially messy in my dataset, because there is text before and after the section headings that we need to preserve. First add line breaks before these labels to make it easier to find the headings. Then pull out the full name in the testimony label using another regex -- this time, one that grabs words in all capital letters. Add that section title to each speaker-comment line in your output file, as well as an index for the section of testimony, all delimited with hashtags.

```
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
```

Finally, write the final string to an output file, described as below, and you're done!

```
v1_output = open('V1Output.txt', mode = 'a', encoding = 'utf-8')
v1_output.write(output3)
v1_output.close()
```

## Understanding the output

The output is a hashtag-separated list. Each line represents one comment in the inputted Senate testimony and contains four hashtag-separated pieces of information about the comment.

The four output variables, in order, are:
1. The name of the person speaking, e.g. "Senator Gallinger"
2. The comment the person made, e.g. "As the questions have been repeatedly read and printed in the proceedings, I presume it is not necessary that I should read them in full."
3. The section of testimony under which the comment was said, e.g. "TRUMAN G. PALMER" for the section "TESTIMONY OF TRUMAN G. PALMER"
4. The index of the testimony, incrementing by one each time a new section of testmiony

With only a few straightforward edits, the code can be adjusted to only output some of this information.

Example input:
```
Mr. Robinson. Oh, they have done a banking business for Cuban 
planters for a great many years. They are advancing money on 
sugar crops. That is a part of their banking business.
```

Example output:
```
Mr. Robinson#  Oh, they have done a banking business for Cuban planters for a great many years. They are advancing money on sugar crops. That is a part of their banking business. #ALBEBT G. ROBINSON.#4
```

## Author
Meredith M. Paker

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Further documentation
No further documentation
