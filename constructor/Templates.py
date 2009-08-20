from mako.template import Template
from mako.lookup import TemplateLookup

from Config import Config

import logging
log = logging.getLogger("popedLogger");

mylookup = TemplateLookup(directories=[Config.templatePath]) 

def renderTemplate(templatename, **kwargs):
	log.info("Using template path %s" % Config.templatePath)
	mytemplate = mylookup.get_template(templatename)
	return mytemplate.render(**kwargs)
