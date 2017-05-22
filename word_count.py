"""MIT License

Copyright (c) 2017 Uka Osim

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""

import sys
import re


def count_words(lines):

    # use a python dictionary -> new_list to store a
    new_list = []
    # make sure that a list type is used at all times
    if not isinstance(lines, list):
        lines = lines.split()
    for line in lines:
        new_list += [word for word in regex.sub("", line).lower().split()]

    # used a python set comprehension to generate an ordered list of tuples
    # containing (<word>, <count>)
    # the list is sorted by the count and also alphabetically(first letter of the word)
    sorted_list = sorted({(word, new_list.count(word)) for word in new_list},
                         key=lambda tup: (-tup[1], tup[0]),
                         reverse=True
                         )
    # returning a reversed list which orders the list starting with the highest word count
    return sorted_list[::-1]

# remove special characters from string except for white spaces
regex = re.compile("[^a-zA-Z\w\s:]")

if __name__ == '__main__':

    stream = sys.stdin
    lines = stream.readlines()
    count_words(lines)
    for word, count in count_words(lines):
        print(word, count)
