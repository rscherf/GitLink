import sublime
import subprocess

from unittest import TestCase


class GitLinkTestCase(TestCase):

    def setUp(self):
        subprocess.getoutput('git clone https://github.com/rscherf/Switcher.git')
        self.view = sublime.active_window().open_file('Switcher/README.md')

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")
        subprocess.getoutput('rm -r Switcher/')

    def test_repo_file_view(self):
        self.assertTrue(self.view.is_valid())
        self.assertTrue(self.view.file_name().replace('\\', '/').endswith('Switcher/README.md'))

    def test_copy_url(self):
        self.view.run_command('gitlink', {'web': False, 'line': False})
        yield lambda: sublime.get_clipboard() != ""
        self.assertEqual('https://github.com/rscherf/Switcher/blob/master/README.md', sublime.get_clipboard())

    def test_copy_blame(self):
        self.view.run_command('gitlink', {'web': False, 'line': False, 'blame': True})
        yield lambda: sublime.get_clipboard() != ""
        self.assertEqual('https://github.com/rscherf/Switcher/blame/master/README.md', sublime.get_clipboard())

    def test_copy_url_line(self):
        self.view.run_command('gitlink', {'web': False, 'line': True})
        yield lambda: sublime.get_clipboard() != ""
        self.assertEqual('https://github.com/rscherf/Switcher/blob/master/README.md#L1-L1', sublime.get_clipboard())

    def test_copy_blame_line(self):
        self.view.run_command('gitlink', {'web': False, 'line': True, 'blame': True})
        yield lambda: sublime.get_clipboard() != ""
        self.assertEqual('https://github.com/rscherf/Switcher/blame/master/README.md#L1-L1', sublime.get_clipboard())
