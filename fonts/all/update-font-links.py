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
        font_path = os.path.relpath(font_file, all_dir)
        ok = True
        if os.path.exists(font_link):
            msg = 'A link of the following font already exists:\n  %s\n'\
                  'Do you want to replace it with this one?\n  %s\n[Y/n]: '
            prev_orig_path = os.path.relpath(os.path.realpath(font_link), all_dir)
            while True:
                answer = input(msg % (prev_orig_path, font_path))
                if answer.lower() in {'yes', 'y', ''}:
                    os.remove(font_link)
                    ok = True
                    break
                elif answer.lower() in {'no', 'n'}:
                    ok = False
                    break
        if ok:
            os.symlink(font_path, font_link)
