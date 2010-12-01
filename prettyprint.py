#!/usr/bin/env python

import sys
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter
from opster import command

css_styles = """
h1 {
  font-family: Cousine, monospace; 
  font-size: 18pt;
  background: #bbb;
  padding: .5em .3em;
  border: 1px solid black;
}
.source { 
  font-family: Cousine, monospace;
  font-size: 12pt; 
}
"""

options = [
   ('s', 'style',  'default',     'Pygments style used'),
   ('o', 'output', 'output.html', 'Output file'),
   ('w', 'width',  100,           'Text width')
]

@command(options, usage="%name [options] file...")
def main(*filenames, **opts):
   "Pretty print source code using Pygments to an HTML file (output.html)"
   lines_wrapped = 0
   formatter = HtmlFormatter(linenos=False, cssclass="source", style="bw")
   output = open(opts['output'], "w")
   output.write('<html><head><style type="text/css">')
   output.write(css_styles)
   output.write(formatter.get_style_defs())
   output.write('</style></head><body>')
   W = opts['width']
   for filename in filenames:
      output.write('<h1>' + filename + '</h1>\n')

      lexer = get_lexer_for_filename(filename)
      F = open(filename, "r")
      code = ""
      for line in F:
         while len(line) > W:
            lines_wrapped += 1
            code += line[:W] + '\n'
            line = line[W:]
         code += line[:W]

      result = highlight(code, lexer, formatter, output)
      F.close()

   output.write('</body></html>')
   if lines_wrapped > 0:
      print "(wrapped " + str(lines_wrapped) + " lines)"
   output.close()

if __name__ == '__main__':
   main() 
   


