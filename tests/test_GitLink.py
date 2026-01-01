import sublime
import subprocess

from os import getenv
from os.path import abspath, dirname, join as pjoin
from unittesting import DeferrableViewTestCase
from ..gitlink.GitLink import GitlinkCommand


class GitLinkTestCase(DeferrableViewTestCase):
    REPO_URL = 'https://github.com/rscherf/Switcher.git'
    REPO_NAME = 'Switcher'
    README_NAME = 'README.md'
    YIELD_OBJ = {
        'condition': lambda: sublime.get_clipboard() != '',
        'period': 53,
        'timeout': 8000,
        'timeout_message': 'Clipboard still empty',
    }
    SSH_CONFIG = 'test.ssh_config'


    @classmethod
    def setUpClass(cls):
        # Prep clipboard to return later
        cls.orig_clipboard = sublime.get_clipboard()

        # Set up the test repo
        cls.my_path = abspath(dirname(__file__))
        subprocess.call(['git', 'clone', cls.REPO_URL], cwd=cls.my_path)
        cls.repo_path = pjoin(cls.my_path, cls.REPO_NAME)
        cls.readme_path =  pjoin(cls.repo_path, cls.README_NAME)
        cls.ssh_config_path = pjoin(cls.my_path, cls.SSH_CONFIG)

    @classmethod
    def tearDownClass(cls):
        # Restore the clipboard
        sublime.set_clipboard(cls.orig_clipboard)

        # Delete the test repo
        if getenv('GITHUB_ACTIONS') != 'true':
            subprocess.call(['rm', '-r', cls.REPO_NAME], cwd=cls.my_path)


    def setUp(self):
        self.view = sublime.active_window().open_file(self.readme_path)
        yield {
            'condition': lambda: not self.view.is_loading(),
            'period': 53,
            'timeout': 8000,
            'timeout_message': 'View not ready',
        }

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")


    def test_ssh_lookup(self):
        cmd = GitlinkCommand(self.view)
        self.assertEqual(
            'github.com',
            cmd.lookup_ssh_host('gh', self.ssh_config_path))
        self.assertEqual(
            'example.com',
            cmd.lookup_ssh_host('pinkfoo', self.ssh_config_path))

    def test_getoutput(self):
        cmd = GitlinkCommand(self.view)
        self.assertEqual('foo', cmd.getoutput(['echo', 'foo']))
        self.assertEqual('fallback', cmd.getoutput(['false'], 'fallback'))
        self.assertRaises(RuntimeError, lambda: cmd.getoutput(['false']))

    def test_repo_file_view(self):
        self.assertTrue(self.view.is_valid())
        self.assertTrue(self.view.file_name().endswith(
            pjoin(self.REPO_NAME, self.README_NAME)))
        self.assertEqual('Switcher', self.view.substr(self.view.line(0)))

    def test_clipboard_exists(self):
        sublime.set_clipboard('')
        self.assertFalse(sublime.get_clipboard())
        sublime.set_clipboard('test string')
        self.assertEqual('test string', sublime.get_clipboard())

    def test_copy_url(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': False})
        yield self.YIELD_OBJ
        self.assertEqual(
            'https://github.com/rscherf/Switcher/blob/master/README.md',
            sublime.get_clipboard())

    def test_copy_blame(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': False, 'blame': True})
        yield self.YIELD_OBJ
        self.assertEqual(
            'https://github.com/rscherf/Switcher/blame/master/README.md',
            sublime.get_clipboard())

    def test_copy_url_line(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': True})
        yield self.YIELD_OBJ
        self.assertEqual(
            'https://github.com/rscherf/Switcher/blob/master/README.md?plain=1#L1',
            sublime.get_clipboard())

    def test_copy_blame_line(self):
        sublime.set_clipboard('')
        self.view.run_command('gitlink', {'web': False, 'line': True, 'blame': True})
        yield self.YIELD_OBJ
        self.assertEqual(
            'https://github.com/rscherf/Switcher/blame/master/README.md?plain=1#L1',
            sublime.get_clipboard())

    def test_zzz_always_pass(self):
        self.assertTrue(True)
