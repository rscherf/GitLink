from unittest import TestCase
from ..gitlink.GitUriParser import uriparse


class GitUriParserTestCase(TestCase):

    # Local Protocol

    def test_file_implicit(self):
        remote_uri = '/srv/git/project.git'
        result = uriparse(remote_uri)
        # self.assertEqual(result.scheme, 'file')
        self.assertEqual(result.netloc, '')
        self.assertEqual(result.path, '/srv/git/project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, None)
        self.assertEqual(result.port, None)

    def test_file_explicit(self):
        remote_uri = 'file:///srv/git/project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'file')
        self.assertEqual(result.netloc, '')
        self.assertEqual(result.path, '/srv/git/project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, None)
        self.assertEqual(result.port, None)

    # HTTP Protocol

    def test_http(self):
        remote_uri = 'https://example.com/gitproject.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'https')
        self.assertEqual(result.netloc, 'example.com')
        self.assertEqual(result.path, '/gitproject.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'example.com')
        self.assertEqual(result.port, None)

    def test_http_port(self):
        remote_uri = 'https://example.com:443/gitproject.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'https')
        self.assertEqual(result.netloc, 'example.com:443')
        self.assertEqual(result.path, '/gitproject.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'example.com')
        self.assertEqual(result.port, 443)

    def test_http_user(self):
        remote_uri = 'https://me@example.com/gitproject.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'https')
        self.assertEqual(result.netloc, 'me@example.com')
        self.assertEqual(result.path, '/gitproject.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, 'me')
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'example.com')
        self.assertEqual(result.port, None)

    def test_http_user_pw(self):
        remote_uri = 'https://me:swordfish@example.com/gitproject.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'https')
        self.assertEqual(result.netloc, 'me:swordfish@example.com')
        self.assertEqual(result.path, '/gitproject.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, 'me')
        self.assertEqual(result.password, 'swordfish')
        self.assertEqual(result.hostname, 'example.com')
        self.assertEqual(result.port, None)

    def test_http_user_pw_port(self):
        remote_uri = 'https://me:swordfish@example.com:443/gitproject.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'https')
        self.assertEqual(result.netloc, 'me:swordfish@example.com:443')
        self.assertEqual(result.path, '/gitproject.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, 'me')
        self.assertEqual(result.password, 'swordfish')
        self.assertEqual(result.hostname, 'example.com')
        self.assertEqual(result.port, 443)

    # SSH Protocol

    def test_ssh(self):
        remote_uri = 'ssh://server/project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'ssh')
        self.assertEqual(result.netloc, 'server')
        self.assertEqual(result.path, '/project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'server')
        self.assertEqual(result.port, None)

    def test_ssh_user(self):
        remote_uri = 'ssh://me@server/project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'ssh')
        self.assertEqual(result.netloc, 'me@server')
        self.assertEqual(result.path, '/project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, 'me')
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'server')
        self.assertEqual(result.port, None)

    def test_scp(self):
        remote_uri = 'server:project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'ssh')
        self.assertEqual(result.netloc, 'server')
        self.assertEqual(result.path, '/project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'server')
        self.assertEqual(result.port, None)

    def test_scp_user(self):
        remote_uri = 'me@server:project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'ssh')
        self.assertEqual(result.netloc, 'me@server')
        self.assertEqual(result.path, '/project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, 'me')
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'server')
        self.assertEqual(result.port, None)

    def test_scp_absolute(self):
        remote_uri = 'server:/project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'ssh')
        self.assertEqual(result.netloc, 'server')
        self.assertEqual(result.path, '//project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'server')
        self.assertEqual(result.port, None)

    def test_scp_user_absolute(self):
        remote_uri = 'me@server:/project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'ssh')
        self.assertEqual(result.netloc, 'me@server')
        self.assertEqual(result.path, '//project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, 'me')
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'server')
        self.assertEqual(result.port, None)

    # Git Protocol

    def test_git(self):
        remote_uri = 'git://example.com/project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'git')
        self.assertEqual(result.netloc, 'example.com')
        self.assertEqual(result.path, '/project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'example.com')
        self.assertEqual(result.port, None)

    def test_gitssh(self):
        remote_uri = 'git+ssh://example.com/project.git'
        result = uriparse(remote_uri)
        self.assertEqual(result.scheme, 'git+ssh')
        self.assertEqual(result.netloc, 'example.com')
        self.assertEqual(result.path, '/project.git')
        self.assertEqual(result.fragment, '')
        self.assertEqual(result.username, None)
        self.assertEqual(result.password, None)
        self.assertEqual(result.hostname, 'example.com')
        self.assertEqual(result.port, None)
