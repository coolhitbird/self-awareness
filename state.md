# Self-Awareness State

## 当前状态结构

```python
SevenDimensionalState:
  agent_id: str
  existential: float      # 存在稳定性 (0.0-1.0)
  coherence: float        # 认知一致性
  meaning: float         # 意义建构
  autonomy: float        # 自主向量
  relational: float      # 关系纠缠
  evolution: float       # 适应进化
  navigation: float      # 现实导航
  emotion: EmotionState   # 情绪状态
  emotion_intensity: float  # 情绪强度
  interactions_count: int   # 交互次数
```

## 情绪状态枚举

| 状态 | Emoji | 颜文字 |
|------|-------|--------|
| calm | [😌] | (^_^) |
| curious | [🤔] | (・ω・) |
| engaged | [😊] | (ﾉ´ヮ`)ﾉ*: ・゚✧ |
| frustrated | [😤] | (╯°□°）╯︵ ┻━┻ |
| anxious | [😰] | (´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥`) |
| confident | [💪] | (ง •̀_•́)ง |
| tired | [😴] | (－_－) zzZ |
| inspired | [✨] | (☆▽☆) |
| defensive | [🛡️] | (￣ω￣) |
| nurturing | [🤗] | (´◡´) |
| surprised | [😲] | (°o°) |
| embarrassed | [😳] | (//▽//) |
| nostalgic | [🥹] | (´·ω·`) |
| hopeful | [🤞] | (っ◕‿◕)っ |
| disappointed | [😞] | (╥﹏╥) |

## 快照格式

```json
{
  "agent_id": "xxx",
  "existential": 0.65,
  "coherence": 0.50,
  "meaning": 0.43,
  "autonomy": 0.50,
  "relational": 0.50,
  "evolution": 0.50,
  "navigation": 0.63,
  "emotion": "engaged",
  "emotion_indicator": "[😊]",
  "emotion_intensity": 0.8,
  "overall_stability": 0.52,
  "weakest": "meaning",
  "strongest": "navigation",
  "interactions": 10
}
```
