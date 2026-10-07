"""固定场景，用来复现题面里的锚点。"""

import json

from . import core


def _line(obj):
    print(json.dumps(obj, ensure_ascii=False))


def run(name):
    if name == "alias":
        rules = core.parse("User_Alias ADMINS = alice\nADMINS ALL = /bin/ls\n", core.Counter())
        _line({"allowed": core.allowed(rules, "alice", set(), "h", "/bin/ls", core.Counter())})
        return 0
    if name == "group":
        rules = core.parse("%wheel ALL = /bin/ls\n", core.Counter())
        _line({"allowed": core.allowed(rules, "alice", {"wheel"}, "h", "/bin/ls", core.Counter())})
        return 0
    if name == "last":
        rules = core.parse("alice ALL = /bin/ls\nalice ALL = !/bin/ls\n", core.Counter())
        _line({"allowed": core.allowed(rules, "alice", set(), "h", "/bin/ls", core.Counter())})
        return 0
    if name == "tag":
        rules = core.parse("alice ALL = NOPASSWD: /bin/ls\n", core.Counter())
        rules_ok = core.allowed(rules, "alice", set(), "h", "/bin/ls", core.Counter())
        _line({"allowed": rules_ok})
        return 0
    if name == "work":
        lines = []
        for i in range(800):
            lines.append("u%04d ALL = /bin/c%04d" % (i, i))
        rules = core.parse("\n".join(lines) + "\n", core.Counter())
        counter = core.Counter()
        for i in range(800):
            core.allowed(rules, "u%04d" % i, set(), "h", "/bin/c%04d" % i, counter)
        _line({"rules": 800, "scanned": counter.scanned})
        return 0
    raise SystemExit("未知场景：" + name)
