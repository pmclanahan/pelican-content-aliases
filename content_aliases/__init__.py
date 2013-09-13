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

from .aliases_plugin import register
