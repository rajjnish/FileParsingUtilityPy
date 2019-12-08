"""
Implement a Python script, that searches for lines matching regular expression -r (--regex) in file/s -f (--files).
Use STDIN if file/s option wasn’t provided.
Assume that input is ASCII, you don't need to deal with a different encoding.
If a line matches, print it. Please print the file name and the line number for every match.
The script accepts list optional parameters which are mutually exclusive:
-u ( --underscore ) which prints '^' under the matching text
-c ( --color ) which highlight matching text [1]
-m ( --machine ) which generate machine-readable output
format: file_name:no_line:start_pos:matched_text
Multiple matches on a single line are allowed, without overlapping.
"""
import re
import sys
import os
import glob
import argparse
from functools import wraps


class SearchPattern:

    def __init__(self, files=None, regex=None, color=None, machine=None):
        """
        Initializing the attributes through setter
        @property is used to get the value of a private attribute without using any getter methods.
        We have to put a line @property in front of the method where we return the private variable.

        To set the value of the private variable, we use @method_name.setter in front of the method.
        We have to use it as a setter.
        """
        self.__files = files
        self.__regex = regex
        self.__color = color
        self.__machine = machine

    @property
    def opts_val(self):
        """
         Using @property decorator to achieve getters and setters behaviour (encapsulate the CL options)
         """
        return self.__files, self.__regex, self.__color, self.__machine

    @opts_val.setter
    def opts_val(self, *args):
        """
        Setter func
        """
        self.__files = args[0]
        self.__regex = args[1]
        self.__color = args[2]
        self.__machine = args[3]

    @staticmethod
    def wrapper_color(func):
        """
        returns a function that take single arg, a Wrapper function
        to Decorate the color_pattern func.
        It can be extended for multiple colors patterns highlight
        """

        @wraps(func)
        def surround_value(word):
            """
            A class of Color can be created for variety of color to highlight the pattern
            """
            end = '\x1b[0m'
            color = '\x1b[4;34;41m'
            return '{}{}{}'.format(color, word, end)
        return surround_value

    @staticmethod
    def color_the_pattern(line, regex, color_word):
        """
        This to print colored pattern in output, with -c option on command line
        it takes a line, regex and wrapper func(decorator) as argument which should be colored
        """
        result = ''
        for word in line.split():
            if regex in word:
                re_pos = re.search(regex, word)
                re_start = re_pos.start()
                re_end = re_pos.end()
                start = word[0:re_start]
                word_color = word[re_start:re_end]
                end = word[re_end:]
                result += start + ' {}'.format(color_word(word_color)) + end
            else:
                result += ' {}'.format(word)
        return result

    @staticmethod
    def get_iterator_values(iterator):
        """
        get iterator which is start and end index of matched regex
        and return a list of tuple(start,end) indexes
        """
        res = [(v.start(), v.end()) for v in iterator]
        return res

    @staticmethod
    def remove_files_post_use():
        """
        use the intermediate files as temp and remove it after use
        """
        file_list = glob.glob('*.text')
        for file in file_list:
            os.remove(file)

    @staticmethod
    def machine_readable(file, regex):
        """
        format -> file_name:line_no:start_pos:matched_text
        reads the output file from default print format and convert to machine readable format
        """
        with open(file, 'r') as f:
            for line in f:
                pattern_start_index = re.search(regex, line)
                start_pos = pattern_start_index.start()
                add_start_pos = [val.strip() for val in line.split(":")]
                add_start_pos.insert(2, str(start_pos))
                add_start_pos = add_start_pos[0:3]
                # print(':'.join(add_start_pos) + ":" + ' '.join(re.findall(regex, line)))
                add_start_pos_str = ':'.join(add_start_pos)
                patter_str = ' '.join(re.findall(regex, line))
                print("{}:{}".format(add_start_pos_str, patter_str))

    @staticmethod
    def parse_stdin_default(std_input, regex):
        """
        Parse the Standard input data, the case when file name is not provided and
        raw data provided as Standard input
        default output, :line_no: line
        -m then , :line_no:start_pos:line
        -c then color the matched pattern in output
        """
        for line_no, line in enumerate(std_input, 1):
            match = re.finditer(r'\b{}\b'.format(regex), line)
            found = [val for val in match]
            if len(found) > 0:
                with open('default_output_stdin.text', 'a') as f:
                    f.write(":{}:{}".format(line_no, line))

    @staticmethod
    def pattern_search_files(files, regex):
        """
        When one or more file names provided in command line
        then parse the files on by one and search the pattern and print output
        :param files: All the files provided with -f option on command line
        :param regex: regular expression to be searched in the file
        """
        try:
            for file in files:
                with open(file, 'r', encoding="ascii") as file_line:
                    for line_no, line in enumerate(file_line, 1):
                        match = re.finditer(r'{}\b'.format(regex), line)
                        found = [val for val in match]
                        if len(found)> 0:
                            with open('default_output_files.text', 'a') as f:
                                f.write("{}: {}:  {}".format(file, line_no, line))
        except Exception as e:
            print("File {} doesnt exist".format(file))

    @staticmethod
    def file_print(files):
        with open(files, 'r') as f:
            for line in f:
                print(line.strip())

    @staticmethod
    def file_color_print(files):
        with open(files, 'r') as f:
            for line in f:
                colored = search.color_the_pattern(line, opts.regex, search.wrapper_color(''))
                print(colored)


if __name__ == "__main__":
    """
     Grabs the command line options
     -f , , default=[sys.stdin]
      default="file_name:no_line:start_pos:matched_text"
     """
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--regex', type=str, help="Regex pattern to search in file")
    parser.add_argument('-f', '--files', help="Files on command line", nargs='*')
    # group.add_argument('-u', '--underscore', type=str, default="^", help="prints '^' under the matching text")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--color', help="Highlights matching text [1]")
    group.add_argument('-m', '--machine', help="machine-readable output")
    opts = parser.parse_args()

    # When the file/s name/s not provided on the command line the read from STDIN
    # Exp: cat file.text | python file_parse.py -r find_this_text

    search = SearchPattern(opts.files, opts.regex, opts.color, opts.machine)

    print(search.opts_val)

    try:
        if opts.files:
            if opts.machine:
                search.pattern_search_files(opts.files, opts.regex)
                search.machine_readable('default_output_files.text', opts.regex)
                search.remove_files_post_use()
            elif opts.color:
                search.pattern_search_files(opts.files, opts.regex)
                search.file_color_print('default_output_files.text')
                search.remove_files_post_use()
            else:
                search.pattern_search_files(opts.files, opts.regex)
                search.file_print('default_output_files.text')
                search.remove_files_post_use()

        elif sys.stdin:
            input_stdin = [x for x in sys.stdin]
            if opts.machine:
                search.parse_stdin_default(input_stdin, opts.regex)
                search.machine_readable('default_output_stdin.text', opts.regex)
                search.remove_files_post_use()
            elif opts.color:
                search.parse_stdin_default(input_stdin, opts.regex)
                search.file_color_print('default_output_stdin.text')
                search.remove_files_post_use()
            else:
                search.parse_stdin_default(input_stdin, opts.regex)
                search.file_print('default_output_stdin.text')
                search.remove_files_post_use()

    except Exception as e:
        print(e)
        print('Please use proper format and filename/regex to parse a file')
        print('“Use <-h > For help”')
        # raise Exception
