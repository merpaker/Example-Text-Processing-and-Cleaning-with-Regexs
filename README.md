## Example-Text-Processing-and-Cleaning-with-Regexs
This script demonstrates how regular expressions in Python can be used to clean and process OCR text with many errors in order to generate a workable dataset. The goal in this specific example is to clean Senate testimony to make a dataset listing the speaker in one column with their testimony in the next column. I also show how to give each comment in the testimony a separate indicator, and how to categorize the comments by the section of testimony they are in.

## What you'll need

### System requirements

This is a Python script designed for Python 3, so you'll need an up-and-running Python distribution. You'll also need an internet connection as the script runs.

### Input file
The script as written requires an input file called "V1". In this case, the file is OCRd text of Senate testimony from 1913. The text delineates the speaker at the start of each comment (e.g. "Senator Gallinger") and then gives the comment. There are also various section breaks (e.g. "TESTIMONY OF TRUMAN G. PALMER—Continued."). This is the text data we are interested in.

The original book printed the title of the work and the page number on the top of each page (e.g. "MAINTENANCE OF A LOBBY TO INFLUENCE LEGISLATION 1087"), which is picked up by the OCR. In the process of the book being scanned, "Digitized by Google" was printed on the PDFs, as well as the date of download from the web. The OCR also erroneously picks up all of this. Finally, the OCR software put a paragraph break at the end of each line instead of at the end of each comment in the testimony, making it difficult to distinguish the various speakers.

For your own use, feel free to any utf-8 encoded .txt file.

### Output file
The output file will be a utf-8 encoded .txt file called "V1Output". You can initialize this file beforehand by creating a blank .txt file of this name. After the script runs, the updated file will have a hashtag-separated list that can be easily imported into other software for analysis.

## How the script works

To be written

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
