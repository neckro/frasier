#!/usr/bin/env python
# coding=utf-8

import fileinput
import sys
from re import match, sub
from glob import glob


def parse(input, characters=[], prefix_speaker=False):
    if len(characters) == 0:
        characters = ["Frasier"]
    characters = map(str.lower, characters)
    parse = False
    out = ""
    for line in input:
        if len(line.strip()) == 0:
            continue
        result = match(r"^(\s*)(.+?)\: (.*?)(\s*)$", line)
        if result:
            speaker = result.group(2).lower()
            text = result.group(3)
            if any(c.lower() in speaker for c in characters):
                parse = True
                print_out(out)
                if prefix_speaker:
                    out = speaker + ": " + text
                else:
                    out = text
                continue
        if parse:
            result = match(r"^ {8}(.+?)$", line)
            if result:
                text = result.group(1).strip()
                if text[len(text)-1] != u"-":
                    out += u" "
                out += text
            else:
                parse = False
    if len(out) > 0:
        print_out(out)


def print_out(out):
    out = sub(r"( *)\[.+\]( *)", " ", out)
    out = sub(r" +", " ", out).strip()
    if len(out) > 0:
        out = unsmarten(out)
        print out.encode("utf-8")


def unsmarten(text):
    # smart single quotes: ‘’
    text = text.replace(u"\u2018", "'").replace(u"\u2019", "'")
    # smart double quotes: “”
    text = text.replace(u"\u201c", '"').replace(u"\u201d", '"')
    # dashes: –
    text = text.replace(u"\u2013", "-")
    return text

if __name__ == "__main__":
    input = fileinput.FileInput(
        files=glob("scripts/*.txt"),
        openhook=fileinput.hook_encoded("utf8")
    )
    parse(input, sys.argv[1:])
