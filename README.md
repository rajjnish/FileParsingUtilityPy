# FileParsingUtilityPy
File parsing tool with default, machine readable and color highlight functionality

Implementation of a Python script, that searches for lines matching regular expression -r (--regex) in file/s -f (--files).
Used STDIN if file/s option was not provided.
Assumption that input is ASCII and don't need to deal with a different encoding.
If a line matches, print it:
print the file name and the line number for every match.

The script accepts list optional parameters which are mutually exclusive:
-u ( --underscore ) which prints '^' under the matching text
-c ( --color ) which highlight matching text [1]
-m ( --machine ) which generate machine-readable output
format: file_name:no_line:start_pos:matched_text
Multiple matches on a single line are allowed, without overlapping.

# Excel Worksheets remover script
Remove worksheets from Excel file.
Arguments : File name and no of sheets to remove

