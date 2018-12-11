# author_split.py
# Split session by author.
# Author is specified in the description field between square brackets.
# Example: My great description [Dr. Thomas]
# Folders will be created for each author.

import copy
import os
import re
import xml.etree.ElementTree as ET

source_filename = 'sample.session.xml'

# Regex to find string between []
author_finder = re.compile('(?<=\\[)(.*?)(?=\\])')

tree = ET.parse(source_filename)
root = tree.getroot()

# Find all authors referenced in session file
authors = set()
image = root.find('image')
overlay = image.find('overlays')
for graphic in overlay.findall('graphic'):
    m = author_finder.search(graphic.attrib['description'])
    authors.add(m.group(0))

# Create new session file for each author
for author in authors:
    t = copy.deepcopy(tree)
    r = t.getroot()
    image = r.find('image')
    overlay = image.find('overlays')
    for graphic in overlay.findall('graphic'):
        m = author_finder.search(graphic.attrib['description'])
        if author != m.group(0):
            overlay.remove(graphic)
    os.makedirs(author)
    t.write(author + '/' + source_filename)


