from unittest import TestCase
from ..gitlink.RevisionType import RevType


class RevTypeTestCase(TestCase):

    def test_revtype_abbrev(self):
        rev_type = RevType.from_setting('abbrev')
        self.assertEqual('abbrev', rev_type.setting_value)
        self.assertEqual(('git', 'rev-parse', '--abbrev-ref', 'HEAD'), tuple(rev_type.git_args))

    def test_revtype_commithash(self):
        rev_type = RevType.from_setting('commithash')
        self.assertEqual('commithash', rev_type.setting_value)
        self.assertEqual(('git', 'rev-parse', 'HEAD'), tuple(rev_type.git_args))

    def test_revtype_unknown(self):
        self.assertRaises(KeyError, lambda: RevType.from_setting('foo'))
