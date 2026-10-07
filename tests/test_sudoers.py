import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoers import core

TEXT = "alice ALL = /bin/ls\n"


class SudoersTest(unittest.TestCase):
    def test_rule_count(self):
        self.assertEqual(len(core.parse(TEXT, core.Counter())), 1)

    def test_plain_user_allowed(self):
        rules = core.parse(TEXT, core.Counter())
        self.assertTrue(core.allowed(rules, "alice", set(), "h", "/bin/ls", core.Counter()))

    def test_other_user_denied(self):
        rules = core.parse(TEXT, core.Counter())
        self.assertFalse(core.allowed(rules, "bob", set(), "h", "/bin/ls", core.Counter()))

    def test_other_command_denied(self):
        rules = core.parse(TEXT, core.Counter())
        self.assertFalse(core.allowed(rules, "alice", set(), "h", "/bin/cat", core.Counter()))

    def test_command_stored(self):
        rules = core.parse(TEXT, core.Counter())
        self.assertEqual(rules[0].command, "/bin/ls")

    def test_counter_counts(self):
        counter = core.Counter()
        core.parse(TEXT, counter)
        self.assertGreater(counter.scanned, 0)


if __name__ == "__main__":
    unittest.main()
