"""A Pelican plugin for outputting redirects.

Say you're porting a Tumblr blog. You'll have post
URLs you'll likely not want to keep. This will let
you set an "alias" URL in the post metadata, and
a file will be output there with a meta refresh
tag that will send visitors to the new url of the
post.

This is mostly useful when deploying to completely
static environments like Github pages, but can also
help at Amazon S3 since you need a file at a url
before you can setup the server-side 301.
"""

import logging
import os
import sys

from jinja2 import Environment, FileSystemLoader
from pelican import signals

logger = logging.getLogger(__name__)

this_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(this_dir))
TEMPLATE = env.get_template('alias.html')

ALIASES = []


def find_alias(content):
    if hasattr(content, 'alias'):
        ALIASES.append(content)


def write_aliases(pelican):
    for content in ALIASES:
        url = '/'.join([content.settings['SITEURL'], content.url])
        html = TEMPLATE.render(content_url=url)
        path = os.path.join(pelican.output_path, content.alias)
        try:
            os.makedirs(os.path.dirname(path))
        except OSError:
            # likely the dir already exists
            pass
        try:
            with open(path, 'w') as f:
                f.write(html)
        except IOError as e:
            logger.exception('Could not write alias: %s' % content.alias)


def register():
    signals.content_object_init.connect(find_alias)
    signals.finalized.connect(write_aliases)
