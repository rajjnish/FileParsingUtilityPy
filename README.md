# FileParsingUtilityPy
File parsing tool with default, machine redable and color highlight functionality

Implementation of a Python script, that searches for lines matching regular expression -r (--regex) in file/s -f (--files).
Use STDIN if file/s option wasn’t provided.
Assume that input is ASCII, you don't need to deal with a different encoding.
If a line matches, print it. Please print the file name and the line number for every match.
The script accepts list optional parameters which are mutually exclusive:
-u ( --underscore ) which prints '^' under the matching text
-c ( --color ) which highlight matching text [1]
-m ( --machine ) which generate machine-readable output
format: file_name:no_line:start_pos:matched_text
Multiple matches on a single line are allowed, without overlapping.
