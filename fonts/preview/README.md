PREVIEW generator of this font collection
=========================================

The `source/update-fontcollect.py` script generates the `fontcollect.sty`
package that contains the following macros.

`\allfontsdir` contains the absolute path to the `templates/fonts/all` folder.

For every font family is generated the two commands:

- `\font<family-name>` is a font-switch turning on the corresponding font;
- `\text<family-name>{<text>}` is a function, which uses the corresponding font
  for its parameter `<text>`.

In both cases the `<family-name>` is the family name without spaces and in lower
case.

The script tries to ignore variable fonts.
