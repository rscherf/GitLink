import re
from urllib.parse import urlparse


class RepositoryParser(object):

    REPO_HOSTS = {
        'github': {
            'url': 'https://github.com/{owner}/{repo}/blob/{revision}/{file}',
            'blame_url': 'https://github.com/{owner}/{repo}/blame/{revision}/{file}',
            'line_param': '#L',
            'line_param_sep': '-L',
        },
        'bitbucket': {
            'url': 'https://bitbucket.org/{owner}/{repo}/src/{revision}/{file}',
            'blame_url': 'https://bitbucket.org/{owner}/{repo}/annotate/{revision}/{file}',
            'line_param': '#cl-',
            'line_param_sep': ':',
        },
        'codebasehq': {
            'url': 'https://{owner}.{domain}/projects/{project}/repositories/{repo}/blob/{revision}/{file}',
            'blame_url': 'https://{owner}.{domain}/projects/{project}/repositories/{repo}/blame/{revision}/{file}',
            'line_param': '#L',
            'line_param_sep': ':',
        },
        'gitlab': {
            'url': 'https://{domain}/{owner}/{repo}/-/blob/{revision}/{file}',
            'blame_url': 'https://{domain}/{owner}/{repo}/-/blame/{revision}/{file}',
            'line_param': '#L',
            'line_param_sep': '-',
        },
    }

    def __init__(self, git_url):
        self.git_url = git_url

        if re.match(r'^git@', git_url):
            git_url = 'ssh://' + git_url
            git_url = re.sub(r'\b:\b', '/', git_url, count=1)
        parsed_url = urlparse(git_url)
        self._pr = parsed_url

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

        # Extra rules for specific hosts
        if 'codebasehq.com' in self.domain:
            self.project = split_path[2]
            if 'http' in self.scheme:
                self.owner = self.domain.split('.')[0]
                self.project = split_path[1]
            self.domain = re.sub(r'^{}\.'.format(self.owner), '', self.domain)

        elif 'gitlab' in self.domain and len(split_path) > 3:
            self.owner = '/'.join(split_path[1:-1])

    def _get_hosting_rule(self):
        # Select the right hosting configuration
        for hosting_name, hosting in self.REPO_HOSTS.items():
            if hosting_name in self.domain:
                # We found a match, so keep these variable assignments
                break
        if not hosting_name or not hosting:
            raise NotImplementedError('"{}" not in known Git hosts'.format(self.domain))
        return hosting_name, hosting

    def _get_formatted_url(self, fmt_id, file, revision, line_start=0, line_end=0):
        _, hosting = self._get_hosting_rule()

        url = hosting[fmt_id].format(
            domain=self.domain,
            owner=self.owner,
            project=self.project,
            repo=self.repo_name,
            revision=revision,
            file=file)

        if line_start:
            url += hosting['line_param'] + str(line_start)
            if line_end:
                url += hosting['line_param_sep'] + str(line_end)

        return url

    def get_source_url(self, file, revision, line_start=0, line_end=0):
        return self._get_formatted_url('url', file, revision, line_start, line_end)

    def get_blame_url(self, file, revision, line_start=0, line_end=0):
        return self._get_formatted_url('blame_url', file, revision, line_start, line_end)
