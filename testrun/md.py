"""
Regular expression based markdown parser.
"""


with open('test.md') as fp:
    content = fp.read()

import re

content = """

# hey

ABsatz

ABsatz

YOHO

kein
neuer Absatz

ha_ll_l **bold**
[php markdown project](http://michelf.ca/projects/php-markdown/extra/#table)
    bla
## hea

"""

def process_indent(line):
    print(len(line.group(1)), line.group(2), 'test')
    print(repr(line.group(1)))
    return line.group(2)

subs = [
    # indent
    (re.compile('\r'), ''), # \r messes up MULTILINE mode.
    (re.compile('^([\s]+)(.*)', re.MULTILINE), process_indent), # \r messes up MULTILINE mode.
    # (re.compile('&'), '&amp;'),
    # (re.compile('^(\w.*?)$', re.MULTILINE), r'<p>\1</p>'),
    # bold
    (re.compile('\*\*([\w ]+?)\*\*'), r'<strong>\1</strong>'),
    (re.compile('\_\_([\w ]+?)\_\_'), r'<strong>\1</strong>'),
    # italic
    (re.compile('\*([\w ]+?)\*'), r'<em>\1</em>'),
    (re.compile('\_([\w ]+?)\_'), r'<em>\1</em>'),
    # code
    (re.compile(r'\`(.+)\`'), r'<code>\1</code>'),
    
    # headers
    (re.compile(r'(.*?)\n=+\n', re.MULTILINE), r'<h1>\1</h1>'),
    (re.compile(r'(.*?)\n-+\n', re.MULTILINE), r'<h2>\1</h2>'),
    (re.compile('^# (\w*?)\n', re.MULTILINE), r'<h1>\1</h1>'),
    (re.compile('^## (.*?)\n', re.MULTILINE), r'<h2>\1</h2>'),
    (re.compile('^### (.*?)\n', re.MULTILINE), r'<h3>\1</h3>'),
    (re.compile('^#### (.*?)\n', re.MULTILINE), r'<h4>\1</h4>'),
    # hyperlink
    (re.compile(r'\[(.+?)\]\((\S+?)\)', re.MULTILINE), r'<a href="\2">\1</a>'),
    # image
    (re.compile(r'\!\[(.+?)\]\((\S+?)\)', re.MULTILINE), r'<img src="\2">\1</a>'),
    # link
    (re.compile(r'\[(.+?)\]\[(.+?)\]', re.MULTILINE), r'<a href="#\2">\1</a>'), 
    # reference
    (re.compile(r'\[(.+?)\]\:[^\S\r\n]*([^\n]*?)', re.MULTILINE), r'<a href="#\2">\1</a>'), 
    # (re.compile('\n'), ''),
    # list
    (re.compile(r'^-\s*(.*)'), r'<li>\1</li>'),

  ]

def md(orig):
  new = orig
  for sub in subs:
    new = sub[0].sub(sub[1], new)
  return new

print('#'*80 + '\n' + md(content))

# remove single line breaks
