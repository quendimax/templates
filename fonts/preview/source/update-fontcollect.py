#!/usr/bin/env python3

import os
import re
import json

from datetime import datetime
from subprocess import check_call, check_output 

this_dir = os.path.normpath(os.path.join(os.path.dirname(__file__)))
all_dir = os.path.normpath(os.path.join(this_dir, '..', '..', 'all'))

extra_subfamilies = ['ExtraBold', 'SemiBold', 'ExtraLight', 'SemiLight', 'Light', 'Thin', 'Medium']

myclass_map = {}


def collect_fonts():
    font_map = {}
    family_regex = re.compile(r'Family:\s+([^\n]+)')
    subfamily_regex = re.compile(r'Subfamily:\s+([^\n]+)')
    for filename in os.listdir(all_dir):
        if not filename.endswith('.otf') and not filename.endswith('.ttf'):
            continue
        if 'wght' in filename.lower() or 'variable' in filename.lower():  # is a variable font
            continue
        if 'izhitsa' in filename:  # I have it only for compatibility with other documents
            continue

        filepath = os.path.join(all_dir, filename)

        otf_output = check_output(('otfinfo', '-i', filepath)).decode('utf8')
        family = family_regex.search(otf_output).group(1)
        subfamily = subfamily_regex.search(otf_output).group(1)

        # for extra_name in extra_subfamilies:
        #     if family.endswith(extra_name):
        #         subfamily = extra_name
        #         family = family[:-len(subfamily)-1]

        if family not in font_map:
            font_map[family] = {
                'family': family,
                'subfamilies': {},
                'fontswitch': '\\font' + family.lower().replace(' ', ''),
                'textcommand': '\\text' + family.lower().replace(' ', '')
            }
        font_map[family]['subfamilies'][subfamily] = filename
        # font_map[family]['subfamilies'][subfamily] = os.path.relpath(filepath, os.path.join(this_dir, '..'))
    return font_map


def gen_font_delc(font_map):
    font_decls = []
    for family in font_map:
        font = font_map[family]
        subfamilies = font['subfamilies']
        tex_decl = \
        '\\newfontfamily{fontswitch}{{{family}}}[\n' \
        '  Path = \\allfontsdir/,\n'.format(fontswitch=font['fontswitch'], family=family)
        if 'Regular' in subfamilies:
            tex_decl += '  UprightFont = {regular_path},\n'.format(regular_path=subfamilies['Regular'])
        if 'Bold' in subfamilies:
            tex_decl += '  BoldFont = {bold_path},\n'.format(bold_path=subfamilies['Bold'])
        if 'Italic' in subfamilies:
            tex_decl += '  ItalicFont = {italic_path},\n'.format(italic_path=subfamilies['Italic'])
        if 'Bold Italic' in subfamilies:
            tex_decl += '  BoldItalicFont = {bolditalic_path}\n'.format(bolditalic_path=subfamilies['Bold Italic'])
        tex_decl += ']\n'
        tex_decl += '\\newcommand{textcommand}[1]{{{{{fontswitch} #1}}}}\n'\
                    .format(textcommand=font['textcommand'], fontswitch=font['fontswitch'])
        font['tex_decl'] = tex_decl
        font_decls.append(tex_decl)
        # print(family, ': ', ', '.join(["'%s'" % sub for sub in sorted(subfamilies)]))
    return font_decls


def write_sty_file(name, font_decls):
    text = \
    '\\NeedsTeXFormat{{LaTeX2e}}\n'\
    '\\ProvidesPackage{{{package_name}}}[{time} All font package is generated automatically.]\n'\
    '\n'\
    '\\RequirePackage[abspath]{{currfile}}\n'\
    '\\newcommand{{\\allfontsdir}}{{\\currfiledir ../../all/}}\n'\
    '\n'\
    '\\RequirePackage{{fontspec}}\n'\
    '\n'\
    .format(package_name=name, time=datetime.now().isoformat(sep=' ', timespec='seconds'))

    for font_decl in font_decls:
        text += '\n'
        text += font_decl

    with open(name + '.sty', 'w') as fd:
        fd.write(text)


def main():
    font_map = collect_fonts()
    font_decls = gen_font_delc(font_map)    
    write_sty_file('fontcollect', font_decls)

    # print(json.dumps(font_map, indent=2))


if __name__ == '__main__':
    main()
