#-------------------------------------------------------------------------------
# Name:        Create HTML file of static analyse
# Purpose:
#
# Author:      U560764
#
# Created:     03/05/2019
# Copyright:   (c) U560764 2019
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import glob
from collections import defaultdict

# fill sorted list of tables based on svg filenames
svgFiles = sorted(glob.glob('*.svg'))
for s in svgFiles:
    fileNames[s.split('.', 1)[0]].append(s)

# write to html
d = {'kiwi': ['kiwi.good.svg', 'kiwi_medium_bad.svg'], 'apple': ['apple.good.2.svg', 'apple.good.1.svg'], 'banana': ['banana.1.ugly.svg', 'banana.bad.2.svg']}
states = ['good', 'bad', 'medium_bad', 'ugly']

html = """<html><table border="1">
<tr><th>Object</th><th>{}</th></tr>""".format("</th><th>".join(states))
for fruit in d:
    html += "<tr><td>{}</td>".format(fruit)
    by_state = {f: re.search(r"[._]({})[._]".format('|'.join(states)), f).group(1) for f in d[fruit]}
    for state in states:
        html += "<td>{}</td>".format('<br>'.join(f for f in d[fruit] if by_state[f] == state))
    html += "</tr>"
html += "</table></html>"

file_ = open('result.html', 'w')
file_.write(html)
file_.close()