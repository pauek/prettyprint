#!/usr/bin/env python

import sys
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import HtmlFormatter, LatexFormatter
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

latex_preamble = """
\\documentclass[10pt]{article}
\\usepackage{fancyvrb}
\\usepackage{color}
\\usepackage{bera}
\\usepackage{vmargin}
\\setpapersize{A4}
\\setmarginsrb{1.2cm}{1.2cm}{1.2cm}{1.2cm}{0cm}{0cm}{.75cm}{0cm}
\\begin{document}
"""

options = [
   ('s', 'style',  'default',     'Pygments style used'),
   ('o', 'output', None,          'Output file'),
   ('w', 'width',  100,           'Text width'),
   ('l', 'latex',  False,         'Produce LaTeX output')
]

def html_output(filenames, outfile, width, style):
   if not outfile:
      outfile = "output.html"
   lines_wrapped = 0
   formatter = HtmlFormatter(linenos=False, cssclass="source", style=style)
   output = open(outfile, "w")
   output.write('<html><head><style type="text/css">')
   output.write(css_styles)
   output.write(formatter.get_style_defs())
   output.write('\n</style></head><body>')
   W = width
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

def latex_output(filenames, outfile, style):
   if not outfile:
      outfile = "output.tex"
   lines_wrapped = 0
   formatter = LatexFormatter(linenos=False, style=style)
   output = open(outfile, "w")
   output.write(latex_preamble)
   output.write(formatter.get_style_defs())
   for filename in filenames:
      output.write('\\hrule\n')
      output.write('\\section*{' + filename + '}\n')

      lexer = get_lexer_for_filename(filename)
      F = open(filename, "r")
      result = highlight(F.read(), lexer, formatter, output)
      F.close()

   output.write('\end{document}')
   if lines_wrapped > 0:
      print "(wrapped " + str(lines_wrapped) + " lines)"
   output.close()
   

@command(options, usage="%name [options] file...")
def main(*filenames, **opts):
   "Pretty print source code using Pygments to an HTML file (output.html)"
   if len(filenames) == 0:
      print "No input files"
      sys.exit(0)
   if opts['latex']:
      latex_output(filenames, opts['output'], opts['style'])
   else:
      html_output(filenames, opts['output'], opts['width'], opts['style'])

if __name__ == '__main__':
   main() 
   


