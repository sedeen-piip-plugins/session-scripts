#!/usr/bin/env python3

# author_split.py
# Split session by author.
# Author is specified in the description field between square brackets.
# Example: My great description [Dr. Thomas]
# Folders will be created for each author.

import argparse
import copy
import os
import re
import xml.etree.ElementTree as ET

# define command line arguments
parser = argparse.ArgumentParser(
    "Split sedeen session files produced by multiple authors")

parser.add_argument("-v", "--verbose",
                    help="increase output verbosity", action="store_true")
parser.add_argument("input", help="path to session file to split")

# parse command line arguments
args = parser.parse_args()

# convert the input path to an absolute path
if os.path.isabs(args.input):
    source_path = args.input
else:
    source_path = os.path.join(os.getcwd(), args.input)

# get the filename to use later
source_filename = os.path.basename(source_path)

# use the location of the input file as a base to store the split sessions
output_dir = os.path.dirname(source_path)

if args.verbose:
    print(F"splitting file {source_path}")

# build a regex to find string between []
author_finder = re.compile('(?<=\\[)(.*?)(?=\\])')

tree = ET.parse(source_path)
root = tree.getroot()

# find all authors referenced in session file
authors = set()
image = root.find('image')
overlay = image.find('overlays')
for graphic in overlay.findall('graphic'):
    if 'description' in graphic.attrib:
        description_field = graphic.attrib['description']
    else:
        description_field = ""
    m = author_finder.search(description_field)
    if not description_field or not m or len(m.groups()) is 0:
        if args.verbose:
            print("found overlay with no author")
        authors.add("")
    else:
        author_name = m.group(0)
        if args.verbose:
            print(F"found author {author_name}")
        authors.add(m.group(0))

# create new session file for each author
for author in authors:
    unassigned = False
    if not author:
        author = "unassigned"
        unassigned = True
        if args.verbose:
            print("building session file for unassigned overlays")
    else:
        if args.verbose:
            print(F"building session file for {author}")
    t = copy.deepcopy(tree)
    r = t.getroot()
    image = r.find('image')
    overlay = image.find('overlays')
    for graphic in overlay.findall('graphic'):
        if 'description' in graphic.attrib:
            description_field = graphic.attrib['description']
        else:
            description_field = ""
        m = author_finder.search(description_field)
        print(F"description: {description_field}")
        if unassigned:
            if m:
                # remove all assigned graphics
                overlay.remove(graphic)
        else:
            if not m or author != m.group(0):
                overlay.remove(graphic)
    author_dir = os.path.join(output_dir, author)
    if args.verbose:
        print(F"creating directory {author_dir}")
    os.makedirs(author_dir)
    author_file = os.path.join(author_dir, source_filename)
    if args.verbose:
        print(F"writing file {author_file}")
    t.write(author_file)
