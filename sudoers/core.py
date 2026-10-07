"""解析 sudoers 规则。"""


class Counter:
    """记录比较次数。"""

    def __init__(self):
        self.scanned = 0


class Rule:
    def __init__(self, users, hosts, command, negate):
        self.users = users
        self.hosts = hosts
        self.command = command
        self.negate = negate


def parse(text, counter):
    aliases = {}
    rules = []
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        counter.scanned += 1
        if "_Alias" in line and "=" in line:
            name, _, rest = line.partition("=")
            aliases[name.strip().split()[-1]] = [item.strip() for item in rest.split(",") if item.strip()]
            continue
        left, _, right = line.partition("=")
        fields = left.split()
        if len(fields) < 2:
            continue
        flattened = list(fields[:-1])
        command = right.strip()
        negate = command.startswith("!")
        if negate:
            command = command[1:].strip()
        rules.append(Rule(flattened, fields[-1], command, negate))
    return rules


def _user_matches(users, user, groups):
    for item in users:
        if item == user or item == "ALL":
            return True
    return False


def allowed(rules, user, groups, host, command, counter):
    for rule in rules:
        counter.scanned += 1
        if not _user_matches(rule.users, user, groups):
            continue
        if rule.hosts != host and rule.hosts != "ALL":
            continue
        if rule.command == command:
            return not rule.negate
    return False
