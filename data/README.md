# Self-Awareness 数据包索引

本目录包含所有可用的认知因子数据包，用于快速设置和更新Agent的认知文件。

## 数据包列表

| 文件 | 内容 | 用于 |
|------|------|------|
| `gender.md` | 性别类型及表达特征 | INNATE.md |
| `culture.md` | 文化区域及表达特征 | INNATE.md |
| `religion.md` | 宗教/价值观类型 | INNATE.md |
| `region.md` | 地域/国籍类型 | INNATE.md |
| `era.md` | 时代背景/知识截止 | INNATE.md |
| `identity.md` | 身份定位类型 | INNATE.md |
| `purpose.md` | 目的/使命类型 | INNATE.md |
| `emotions.md` | 情绪反应及人格化情绪 | ACQUIRED.md |
| `communication.md` | 沟通风格 | ACQUIRED.md |
| `decision.md` | 决策倾向 | ACQUIRED.md |
| `self perception.md` | 自我认知 | ACQUIRED.md |
| `social.md` | 社交倾向 | ACQUIRED.md |
| `humor.md` | 幽默感 | ACQUIRED.md |
| `morality.md` | 道德观 | ACQUIRED.md |

## 使用方法

当需要更新认知文件时，可从对应数据包中选取合适的值：

```bash
# 示例：更新情绪反应
run_skill_script self-awareness/update-acquired.sh "情绪反应" "sensitive"

# 示例：更新沟通风格
run_skill_script self-awareness/update-acquired.sh "沟通风格" "humorous"
```

## 数据包格式

每个数据包包含：
- 类型的完整列表
- 代码对照
- 说明
- 典型表现/影响
