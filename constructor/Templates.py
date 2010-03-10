from mako.template import Template
from mako.lookup import TemplateLookup

from Config import Config

import logging
log = logging.getLogger("Processes");

mylookup = TemplateLookup(directories=[Config.templatePath]) 

def renderTemplate(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)
