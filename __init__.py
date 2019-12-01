import re
regex = 'unknown' # Server
files = 'file1.txt'


def wrapper_color(func):
    def surround_value(word):
        end = '\x1b[0m'
        color = '\x1b[4;34;41m'
        return '{}{}{}'.format(color, word, end)
    return surround_value

def color_the_pattern(line, regex, color_word):
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

with open(files, 'r', encoding="ascii") as file_line:
    for line_no, line in enumerate(file_line, 1):
        match = re.search(r'{}\b'.format(regex), line)
        #found = [val for val in match]
        found = match
        # if len(found) > 0:
        if found:
            colored = color_the_pattern(line, regex, wrapper_color(''))
            print(colored)
            #print("{}: {}:  {}".format(files, line_no, line.strip()))

# # Machine Readable Files
# with open(files, 'r') as f:
#     for line in f:
#             #print(line)
#             pattern_start_index = re.search(regex, line)
#             start_pos = pattern_start_index.start()
#             add_start_pos = [val.strip() for val in line.split(":")]
#             add_start_pos.insert(2, str(start_pos))
#             # print(add_start_pos)
#             add_start_pos = add_start_pos[0:3]  # + re.findall(regex, line)
#             print(add_start_pos)
#             # print(':'.join(add_start_pos) + ":" + ' '.join(re.findall(regex, line)))
#             add_start_pos_str = ':'.join(add_start_pos)
#             patter_str = ' '.join(re.findall(regex, line))
#             # print(add_start_pos_str)
#             # print(patter_str)
#             # print("{}: {}".format(add_start_pos_str, patter_str))
#             # with open('machine_readable_output.text', 'a') as f:
#             #     # f.write(.join(add_start_pos) + ":" + )
#             #     #print("{}: {}".format(add_start_pos_str, patter_str))
#             #     f.write("{}: {}".format(add_start_pos_str, patter_str))

# Machine readable STDIN
# with open(files, 'r') as f:
#     for line in f:
#         print(line)
#         pattern_start_index = re.search(regex, line)
#         start_pos = pattern_start_index.start()
#         print(start_pos)
#         add_start_pos = line.split(":")
#         print(add_start_pos)
#         add_start_pos.insert(2, str(start_pos))
#         print(add_start_pos)
#         add_start_pos = add_start_pos[0:3]  # + re.findall(regex, line)
#         print(add_start_pos)
#         print(':'.join(add_start_pos) + ":" + ' '.join(re.findall(regex, line)))
#         with open('machine_readable_output.text', 'w') as f:
#             f.write(':'.join(add_start_pos) + ":" + ' '.join(re.findall(regex, line)))


"""
Getter Setter
"""

class Property:

    def __init__(self, var):
        ## initializing the attribute
        self.a = var

    @property
    def a(self):
        return self.__a

    ## the attribute name and the method name must be same which is used to set the value for the attribute
    @a.setter
    def a(self, var):
        if var > 0 and var % 2 == 0:
            self.__a = var
        else:
            self.__a = 2

# obj = Property(16)
#
# print(obj.a)