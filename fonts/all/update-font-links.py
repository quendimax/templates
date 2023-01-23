#!/usr/bin/env python3

import os

all_dir = os.path.normpath(os.path.join(os.path.dirname(__file__)))
font_dir = os.path.normpath(os.path.join(all_dir, '..'))

# clean `all` folder
for filename in os.listdir(all_dir):
    if filename.endswith('.ttf') or filename.endswith('.otf'):
        filepath = os.path.join(all_dir, filename)
        if os.path.islink(filepath):
            os.remove(filepath)

# make new symlinks
for root, dirs, files in os.walk(font_dir):
    font_files = [os.path.join(root, filename) for filename in files
                  if filename.endswith('.ttf') or filename.endswith('.otf')]
    font_files = [font_file for font_file in font_files if not os.path.islink(font_file)]
    for font_file in font_files:
        font_link = os.path.join(all_dir, os.path.basename(font_file))
        os.symlink(font_file, font_link)
