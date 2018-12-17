#!/usr/bin/env python3

# author_join.py
# Join session files created by different authors into a single file.
# Set the source directory to a folder that contains folders for each author.
# The name of the author (surrounded by square brackets) will be appended to
# the description fields of their overlays.
# Example directory structure:


import argparse
import copy
import os
import re
import xml.etree.ElementTree as ET

T10_COLORS = ["#4e79a7ff",
              "#59a14fff",
              "#9c755fff",
              "#f28e2bff",
              "#edc948ff",
              "#bab0acff",
              "#e15759ff",
              "#b07aa1ff",
              "#76b7b2ff",
              "#ff9da7ff"]

# define command line arguments
parser = argparse.ArgumentParser(
    "Join sedeen session files produced by multiple authors")

parser.add_argument("-v", "--verbose",
                    help="increase output verbosity", action="store_true")
parser.add_argument(
    "dir", help="path to source directory containing author subfolders")
parser.add_argument("-o", "--output-dir",
                    help="directory to store output session file", default=".")
parser.add_argument("-c", "--color-by-author",
                    help="override color by author", action="store_true")

# parse command line arguments
args = parser.parse_args()

# if the provided dir is absolute, use it; otherwise, make it absolute
if os.path.isabs(args.dir):
    source_dir = args.dir
else:
    source_dir = os.path.join(os.getcwd(), args.dir)

if args.verbose:
    print(F"looking for subfolders in {source_dir}")

# get the author folders in the specified directory
authors = [name for name in os.listdir(
    source_dir) if os.path.isdir(os.path.join(source_dir, name))]

if len(authors) < 2:
    print("error - {} must contain at least 2 subdirectories (contains {})".format(source_dir, len(authors)))
    raise SystemExit

if args.verbose:
    for author in authors:
        print(F"  found author {author}")
    print("looking for common files to merge")

# get full paths to the author folders
author_dirs = [os.path.join(source_dir, author) for author in authors]

# ensure each author folder contains similar session files
filenames = set([f for f in os.listdir(author_dirs[0]) if os.path.isfile(os.path.join(author_dirs[0], f))])

for dir in author_dirs[1:]:
    filenames_tmp = set([f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))])
    filenames.intersection_update(filenames_tmp)

if args.verbose:
    for f in filenames:
        print(F"  found file {f}")

for filename in filenames:
    if args.verbose:
        print(F"joining file {filename}")

    # use the first file as a reference; clear all its overlays
    tree_out = ET.parse(os.path.join(author_dirs[0], filename))
    root_out = tree_out.getroot()
    image_out = root_out.find('image')
    overlay_out = image_out.find('overlays')
    for graphic in overlay_out.findall('graphic'):
        overlay_out.remove(graphic)

    # Get each authors session and append it to the base
    for i, author in enumerate(authors):
        tree = ET.parse(os.path.join(author_dirs[i], filename))
        root = tree.getroot()
        image = root.find('image')
        overlays = image.find('overlays')
        for graphic in overlays.findall('graphic'):
            overlay_out.append(graphic)
            graphic.attrib['description'] += ' [' + author + ']'
            if args.color_by_author:
                pen = graphic.find('pen')
                pen.attrib['color'] = T10_COLORS[i]


    # save the joined session file
    filepath_out = os.path.join(args.output_dir, filename)
    tree_out.write(filepath_out)
