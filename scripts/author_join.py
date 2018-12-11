# author_join.py
# Join session files created by different authors into a single file.
# Set the source directory to a folder that contains folders for each author.
# The name of the author (surrounded by square brackets) will be appended to
# the description fields of their overlays.
# Example directory structure:
# some_directory/
# ├── Dr. House/
# │   └── sample.session.xml
# ├── Dr. Wilson/
# │   └── sample.session.xml
# └── Dr. Taub/
#     └── sample.session.xml

import argparse
import copy
import os
import re
import xml.etree.ElementTree as ET

# define command line arguments
parser = argparse.ArgumentParser(
    "Join sedeen session files produced by multiple authors")

parser.add_argument("-v", "--verbose",
                    help="increase output verbosity", action="store_true")
parser.add_argument(
    "dir", help="path to source directory containing author subfolders")
parser.add_argument("-o", "--output-dir",
                    help="directory to store output session file", default=".")

# parse command line arguments
args = parser.parse_args()

if args.verbose:
    print(F"looking for subfolders in {args.dir}")

# get the author folders in the specified directory
authors = [name for name in os.listdir(
    args.dir) if os.path.isdir(name)]

if len(authors) < 2:
    print("error - {} must contain at least 2 subdirectories (contains {})".format(args.dir, len(authors)))
    raise SystemExit

if args.verbose:
    for author in authors:
        print(F"  found author {author}")

# get full paths to the author folders
author_dirs = [os.path.join(args.dir, author) for author in authors]

# ensure each author folder contain similar session files
filenames = [f for f in os.listdir(author_dirs[0]) if os.path.isfile(f)]
for dir in author_dirs[1:]:
    pass

# filename=os.listdir(authors[0])[0]
# filepath=os.path.join(args.output_dir, filename)

# if args.verbose:
#     print(F"joining files into {filepath}")

# # Use the first file as base; clear all its overlays
# tree = ET.parse(authors[0] + '/' + filename)
# root = tree.getroot()
# image = root.find('image')
# overlay = image.find('overlays')
# for graphic in overlay.findall('graphic'):
#     overlay.remove(graphic)

# # Get each authors session and append it to the base
# for author in authors:
#     t = ET.parse(author + '/' + filename)
#     r = t.getroot()
#     i = r.find('image')
#     o = i.find('overlays')
#     for graphic in o.findall('graphic'):
#         overlay.append(graphic)
#         graphic.attrib['description'] += ' [' + author + ']'

# tree.write(filename)
