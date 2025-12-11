import re
from urllib.parse import urlparse


class RepositoryParser(object):

    def __init__(self, git_url):
        self.git_url = git_url

        if re.match(r'^git@', git_url):
            git_url = 'ssh://' + git_url
            git_url = re.sub(r'\b:\b', '/', git_url, count=1)
        parsed_url = urlparse(git_url)
        self._pr = parsed_url
        print(parsed_url)

        self.scheme = parsed_url.scheme
        try:
            self.ssh_user, self.domain = parsed_url.netloc.split('@')
        except:
            self.ssh_user = None
            self.domain = parsed_url.netloc

        path = re.sub(r'\.git$', '', parsed_url.path)
        split_path = path.split('/')
        self.owner = split_path[1]
        self.repo_name = split_path[-1]
        self.project = None

        if 'codebasehq.com' in self.domain:
            self.project = split_path[2]
            if 'http' in self.scheme:
                self.owner = self.domain.split('.')[0]
                self.project = split_path[1]
        if 'gitlab' in self.domain and len(split_path) > 3:
            self.owner = '/'.join(split_path[1:-1])
