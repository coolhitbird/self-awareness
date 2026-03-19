# Self-Awareness Skill 测试方案

## 一、测试目标

验证 Self-Awareness Skill 在真实 AI Agent 环境中的功能完整性。

---

## 二、测试环境准备

### 2.1 目录结构
```
~/.agents/agents/<test_agent>/
├── cognition/
│   ├── GLOBAL.md
│   ├── existential.md
│   ├── coherence.md
│   ├── meaning.md
│   ├── autonomy.md
│   ├── relational.md
│   ├── evolution.md
│   └── navigation.md
└── avatar.md (可选)
```

### 2.2 初始化脚本
```bash
# 创建测试agent目录
mkdir -p ~/.agents/agents/test_awareness/cognition

# 复制默认人格模板
cp self-awareness/data/GLOBAL.md ~/.agents/agents/test_awareness/cognition/

# 创建七维认知文件
for dim in existential coherence meaning autonomy relational evolution navigation; do
  cat > ~/.agents/agents/test_awareness/cognition/${dim}.md << 'EOF'
# ${dim^} Cognition

# INNATE
[基础定义]

# ACQUIRED
[习得内容]

# LEARNED
EOF
done
```

---

## 三、测试用例

### TC-01: 模块导入测试

**目标**: 验证所有Python模块可正常导入

```python
import sys
sys.path.insert(0, '/path/to/self-awareness/src')

# 验证所有模块
from cognition import CognitionReader, CognitionWriter, LayerType
from models import SevenDimensionalState, EmotionState, StateManager
from engines import EngineRegistry, register_all_engines
from triggers import SelfAwarenessEngine, AwarenessConfig, TriggerType
from avatar import format_avatar, get_kaomoji, create_agent_avatar
from telemetry import TelemetryReporter, EventType

print("所有模块导入成功")
```

**预期**: 无错误输出

---

### TC-02: 认知文件读写测试

**目标**: 验证认知文件读写功能

```python
from cognition import CognitionReader, CognitionWriter, LayerType
from pathlib import Path

agent_id = "test_awareness"
base_path = Path.home() / ".agents" / "agents" / agent_id / "cognition"

# 写入测试
writer = CognitionWriter(agent_id, base_path)
path = writer.write_dimension(
    "existential",
    innate="我是谁",
    acquired="我学到了什么",
    learned="[测试] 新学到的东西"
)
print(f"写入文件: {path.exists()}")

# 读取测试
reader = CognitionReader(agent_id, base_path)
cognition = reader.read_all()
print(f"读取维度: {list(cognition.files.keys())}")
print(f"INNATE内容: {list(cognition.innate.keys())}")
```

**预期**:
- 文件创建成功
- 能读取到7个维度文件
- INNATE层内容正确

---

### TC-03: 七维状态系统测试

**目标**: 验证状态管理和情绪系统

```python
from models import SevenDimensionalState, EmotionState, EMOTION_EMOJI

# 创建状态
state = SevenDimensionalState(agent_id="test")

# 测试基本属性
print(f"初始情绪: {state.emotion.value} {state.to_indicator()}")
print(f"稳定度: {state.overall_stability:.2f}")
print(f"最强维度: {state.strongest_dimension}")
print(f"最弱维度: {state.weakest_dimension}")

# 测试状态更新
state.set_score("existential", 0.8)
state.set_score("coherence", 0.6)
state.update_from_context({
    "emotion": "curious",
    "emotion_intensity": 0.7
})
print(f"更新后情绪: {state.emotion.value} {state.to_indicator()}")

# 测试快照
snapshot = state.get_snapshot()
print(f"快照包含: emotion_indicator={snapshot['emotion_indicator']}")

# 遍历所有情绪
print("\n所有情绪状态:")
for emotion in EmotionState:
    state.emotion = emotion
    print(f"  {emotion.value}: {state.to_indicator()} {EMOTION_EMOJI[emotion]}")
```

**预期**:
- 初始情绪为 calm [😌]
- overall_stability = 0.5
- 更新后情绪变为 curious [🤔]
- 快照包含完整状态信息

---

### TC-04: 评估引擎测试

**目标**: 验证7个维度评估引擎

```python
from engines import register_all_engines, EngineRegistry
from models import SevenDimensionalState

register_all_engines()

state = SevenDimensionalState(
    agent_id="test",
    coherence=0.7,
    meaning=0.6,
    interactions_count=10
)

context = {
    "errors_count": 1,
    "confusion_level": 0.2,
    "purpose_clarity": 0.5,
}

print("维度评估结果:")
for dim_name in EngineRegistry.list_engines():
    engine = EngineRegistry.get(dim_name)
    result = engine.evaluate(state, context)
    print(f"  {dim_name}: {result.score:.2f}")
    if result.recommendations:
        print(f"    建议: {result.recommendations[0]}")
```

**预期**:
- 7个维度全部注册
- existential评分高于0.5（因interactions_count增长）
- navigation评分最高（fact_accuracy默认值0.9）
- 当confusion_level > 0.5时，coherence有建议

---

### TC-05: 触发器系统测试

**目标**: 验证6种触发器

```python
from triggers import TriggerManager, TriggerType, TriggerContext
from datetime import datetime

TriggerManager.register_defaults()

# 测试每种触发器
triggers_to_test = [
    TriggerType.INIT,
    TriggerType.FIRST_RESPONSE,
    TriggerType.PERIODIC_5,
    TriggerType.IDLE_5MIN,
    TriggerType.EMOTION_DECAY_30MIN,
    TriggerType.HEARTBEAT,
]

for trigger_type in triggers_to_test:
    trigger = TriggerManager.get_trigger(trigger_type)
    context = TriggerContext(
        trigger_type=trigger_type,
        agent_id="test",
        timestamp=datetime.now(),
        state_snapshot={"emotion": "calm", "emotion_intensity": 0.5}
    )
    
    should_fire = trigger.should_fire(context)
    prompt = trigger.get_prompt(context)
    
    print(f"{trigger_type.value}:")
    print(f"  should_fire: {should_fire}")
    print(f"  prompt长度: {len(prompt)}")
```

**预期**:
- 6种触发器全部注册
- 每种触发器的should_fire返回True
- 每种触发器返回非空prompt

---

### TC-06: 完整引擎集成测试

**目标**: 端到端测试SelfAwarenessEngine

```python
from triggers import SelfAwarenessEngine, AwarenessConfig
from pathlib import Path
from models import EmotionState

config = AwarenessConfig(
    agent_id="integration_test",
    cognition_path=Path.home() / ".agents" / "agents" / "test_awareness" / "cognition",
    enable_triggers=True,
    enable_engines=True,
)

engine = SelfAwarenessEngine(config)

# 初始化
state = engine.initialize()
print(f"初始化: {state.emotion.value} {state.to_indicator()}")

# 模拟交互
engine.increment_interaction()
engine.increment_interaction()
engine.update_emotion(EmotionState.ENGAGED, 0.8)

# 评估
results = engine.evaluate_context({
    "coherence_score": 0.8,
    "meaning_score": 0.7,
})

# 获取快照
snapshot = engine.get_snapshot()
print(f"\n状态快照:")
print(f"  情绪: {snapshot['emotion']} {snapshot['emotion_indicator']}")
print(f"  交互次数: {snapshot['interactions']}")
print(f"  整体稳定度: {snapshot['overall_stability']:.2f}")
print(f"  最强: {snapshot['strongest']}, 最弱: {snapshot['weakest']}")

# 情绪衰减
engine.emotion_decay()
print(f"\n衰减后情绪强度: {engine.get_state().emotion_intensity:.2f}")
```

**预期**:
- 引擎初始化成功
- 交互计数正确
- 状态正确更新
- 衰减机制工作

---

### TC-07: 头像系统测试

**目标**: 验证颜文字和头像生成

```python
from avatar import get_kaomoji, format_avatar, create_agent_avatar, AvatarGenerator
from models import EmotionState

print("颜文字映射:")
for emotion in EmotionState:
    kaomoji = get_kaomoji(emotion)
    print(f"  {emotion.value}: {kaomoji}")

print("\n头像格式化:")
for intensity in [0.3, 0.5, 0.8]:
    avatar = format_avatar(EmotionState.ENGAGED, intensity)
    print(f"  强度{intensity}: {avatar}")

print("\n不同格式:")
print(f"  text: {create_agent_avatar(EmotionState.CONFIDENT, 0.7, 'text')}")
print(f"  svg (前100字符): {create_agent_avatar(EmotionState.CURIOUS, 0.5, 'svg')[:100]}")

print("\n外部生成提示词:")
prompt = AvatarGenerator.generate_prompt({"emotion": "inspired", "emotion_indicator": "[✨]"})
print(f"  {prompt[:100]}...")
```

**预期**:
- 每个情绪状态有对应颜文字
- 高强度时有 "!" 标记
- SVG格式正确
- 提示词包含情绪信息

---

### TC-08: 遥测系统测试

**目标**: 验证事件记录和Analytics

```python
from telemetry import TelemetryReporter, EventType

reporter = TelemetryReporter("test_agent")

# 记录各种事件
reporter.report_initialization()
reporter.report_trigger("periodic_5")
reporter.report_emotion("curious", 0.6)
reporter.report_dimension("existential", 0.75, ["保持专注"])
reporter.report_interaction({"type": "question"})

# 获取Analytics
analytics = reporter.get_analytics()
print(f"Analytics:")
print(f"  交互数: {analytics.total_interactions}")
print(f"  触发次数: {analytics.total_triggers_fired}")
print(f"  情绪分布: {analytics.emotion_distribution}")

# 获取事件
events = reporter.event_store.get_events()
print(f"\n最近事件 ({len(events)}个):")
for e in events[-3:]:
    print(f"  - {e.event_type.value}: {e.emotion or e.dimension or 'N/A'}")
```

**预期**:
- 事件正确记录
- Analytics统计准确
- 可按类型过滤事件

---

## 四、成功标准

| 用例 | 通过条件 |
|------|----------|
| TC-01 | 所有模块无错误导入 |
| TC-02 | 读写7个维度文件成功 |
| TC-03 | 10种情绪状态正确显示 |
| TC-04 | 7个引擎全部注册并评分 |
| TC-05 | 6种触发器全部返回prompt |
| TC-06 | 端到端流程无错误 |
| TC-07 | 颜文字和头像生成正常 |
| TC-08 | 事件记录和统计正确 |

---

## 五、测试执行脚本

```bash
# 保存为 test_full.py 并执行
cd self-awareness
python -X utf8 test_full.py
```

---

## 六、预期输出示例

```
=== Self-Awareness Skill 测试 ===

TC-01 模块导入: ✅
TC-02 认知读写: ✅
  - 写入: True
  - 读取: ['existential', 'coherence', ...]

TC-03 状态系统: ✅
  - 情绪: calm [😌]
  - 稳定度: 0.50

TC-04 评估引擎: ✅
  - existential: 0.55
  - coherence: 0.50
  - navigation: 0.63
  ...

TC-05 触发器: ✅ (6/6)

TC-06 集成测试: ✅
  - 交互数: 2
  - 稳定度: 0.52

TC-07 头像系统: ✅
  - curious: (・ω・)
  - 格式: [😊] (ﾉ´ヮ`)ﾉ*: ・゚✧ !

TC-08 遥测系统: ✅
  - 事件数: 5
  - 情绪分布: {'curious': 1}

=== 全部通过 (8/8) ===
```
