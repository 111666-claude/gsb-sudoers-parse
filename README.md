# sudoers-parse

解析 sudoers：别名表、用户与组说明、主机与命令说明，按最后一条命中规则判定。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m sudoers --sample=alias
python3 -m sudoers --sample=group
python3 -m sudoers --sample=last
python3 -m sudoers --sample=tag
python3 -m sudoers --sample=work
```

## 口径

- **别名**：`User_Alias 名字 = 项, 项` 等定义别名；使用处先把别名展开成项列表。
- **用户说明**：项是用户名、`%组名` 或 `ALL`；`%组` 匹配用户的组集合，`ALL` 匹配任何人。
- **命令**：`(runas)` 部分与 `NOPASSWD:` / `PASSWD:` 标签要去掉再比较；`!命令` 表示拒绝。
- **判定**：多条规则命中时以最后一条为准；没有任何命令命中就是不允许。
- **查找**：判定时只扫命中的规则。

## 不变量

- 别名在使用处已展开；组项按用户组集合匹配。
- 最后一条命中规则决定结果；`NOPASSWD:` 不出现在命令串里。
- `scanned` 不随规则数平方级放大：八百条规则的 `scanned` 不超过 6000。

## 输出契约

`allowed(rules, user, groups, host, command)` 返回布尔；场景打印一行 JSON。
`--sample=work` 打印 `{"rules": N, "scanned": N}`。
