from bokeh.models import Panel, Tabs, Button, Paragraph
from bokeh.models.widgets import Div

from jinja2 import Template
from os.path import dirname, join

def modify_page2(doc):

    with open(join(dirname(__file__),"..","templates","page2.html")) as t:
        temp = Template(t.read())
    doc.template = temp


