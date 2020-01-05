#!/usr/bin/env python3
# coding=utf-8

import fileinput
import sys
from re import match, sub
from glob import glob


def parse(input, characters=[], prefix_speaker=False):
    if len(characters) == 0:
        characters = ["Frasier"]
    characters = list(map(str.lower, characters))
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
                if prefix_speaker:
                    out = speaker + ": " + text
                else:
                    out = text
                continue
        if parse:
            result = match(r"^ {8}(.+?)$", line)
            if result:
                text = result.group(1).strip()
                if text[len(text)-1] != "-":
                    out += " "
                out += text
            else:
                parse = False
                print_out(out)


def print_out(out):
    out = sub(r"( *)\[.+\]( *)", " ", out)
    out = sub(r" +", " ", out).strip()
    if len(out) > 0:
        out = unsmarten(out)
        print(out)


def unsmarten(text):
    # smart single quotes: ‘’
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    # smart double quotes: “”
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    # dashes: –
    text = text.replace("\u2013", "-")
    return text


if __name__ == "__main__":
    input = fileinput.FileInput(
        files=glob("scripts/*.txt"),
        openhook=fileinput.hook_encoded("utf8")
    )
    parse(input, sys.argv[1:])
