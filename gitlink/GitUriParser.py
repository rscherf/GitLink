from re import match
from urllib.parse import urlparse


def uriparse(git_remote_uri):
    """Normalizer for various kinds of Git URI, notably scp-like"""

    # Test for scp-like URIs
    if ':' in git_remote_uri and not match(r'^[\w+]+://', git_remote_uri):
        git_remote_uri = git_remote_uri.replace(':', '/')
        git_remote_uri = 'ssh://' + git_remote_uri

    return urlparse(git_remote_uri)
