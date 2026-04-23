from enum import Enum


class RevType(Enum):
    """Setting options for revision type"""

    ABBREV = ('abbrev', ['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    COMMIT_HASH = ('commithash', ['git', 'rev-parse', 'HEAD'])

    def __init__(self, stg_value, git_args):
        self.setting_value = stg_value
        self.git_args = git_args

    @staticmethod
    def from_setting(stg_value):
        for rev_type in RevType:
            if rev_type.setting_value == stg_value:
                return rev_type
        raise KeyError(stg_value + ' not found in RevType')
