#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Self-Awareness Skill 完整测试脚本
执行方式: cd self-awareness && python -X utf8 test_full.py
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径 (不是src目录)
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_tc01_modules():
    """TC-01: 模块导入测试"""
    print("\n[TC-01] 模块导入测试")
    try:
        # 使用 src.module 模式确保相对导入正常工作
        import src.cognition as cognition
        import src.models as models
        import src.engines as engines
        import src.triggers as triggers
        import src.avatar as avatar
        import src.telemetry as telemetry
        
        # 注册
        engines.register_all_engines()
        triggers.TriggerManager.register_defaults()
        
        print(f"  ✅ engines: {len(engines.EngineRegistry.list_engines())} 个")
        print(f"  ✅ triggers: {len(triggers.TriggerManager._triggers)} 个")
        print(f"  ✅ avatar kaomojis: {len(avatar.KAOMOJI_MAP)} 种情绪")
        print("  ✅ 所有模块导入成功")
        return True
    except Exception as e:
        print(f"  ❌ 导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tc02_cognition():
    """TC-02: 认知文件读写测试"""
    print("\n[TC-02] 认知文件读写测试")
    try:
        import tempfile
        from pathlib import Path
        from src.cognition import CognitionReader, CognitionWriter
        
        with tempfile.TemporaryDirectory() as tmp:
            base_path = Path(tmp)
            writer = CognitionWriter("test", base_path)
            
            for dim in ["existential", "coherence", "meaning", "autonomy", "relational", "evolution", "navigation"]:
                path = writer.write_dimension(dim, innate=f"我是{dim}", acquired="", learned="")
                assert path.exists()
            
            reader = CognitionReader("test", base_path)
            cognition = reader.read_all()
            
            assert len(cognition.files) == 7, f"期望7个文件，实际{len(cognition.files)}"
            
            print(f"  ✅ 成功读写 {len(cognition.files)} 个维度文件")
            return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def test_tc03_state():
    """TC-03: 七维状态系统测试"""
    print("\n[TC-03] 七维状态系统测试")
    try:
        from src.models import SevenDimensionalState, EmotionState, EMOTION_EMOJI
        
        state = SevenDimensionalState(agent_id="test")
        
        assert state.emotion == EmotionState.CALM
        assert state.overall_stability == 0.5
        
        state.set_score("existential", 0.8)
        state.update_from_context({"emotion": "curious", "emotion_intensity": 0.7})
        assert state.emotion == EmotionState.CURIOUS
        
        snapshot = state.get_snapshot()
        assert snapshot["emotion_indicator"] == "[🤔]"
        
        emotion_count = len(EmotionState)
        assert emotion_count >= 10, f"期望至少10种情绪，实际{emotion_count}"
        
        print(f"  ✅ 情绪状态: {state.emotion.value} {state.to_indicator()}")
        print(f"  ✅ 稳定度: {state.overall_stability:.2f}")
        print(f"  ✅ 共 {emotion_count} 种情绪状态")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def test_tc04_engines():
    """TC-04: 评估引擎测试"""
    print("\n[TC-04] 评估引擎测试")
    try:
        import src.engines as engines
        from src.models import SevenDimensionalState
        
        engines.register_all_engines()
        engine_list = engines.EngineRegistry.list_engines()
        
        assert len(engine_list) == 7, f"期望7个引擎，实际{len(engine_list)}"
        
        state = SevenDimensionalState(agent_id="test")
        state.set_score("coherence", 0.7)
        state.set_score("meaning", 0.6)
        
        print("  维度评估结果:")
        for name in engine_list:
            engine = engines.EngineRegistry.get(name)
            result = engine.evaluate(state, {"confusion_level": 0.6})
            print(f"    {name}: {result.score:.2f}")
        
        print("  ✅ 7个评估引擎全部正常工作")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def test_tc05_triggers():
    """TC-05: 触发器系统测试"""
    print("\n[TC-05] 触发器系统测试")
    try:
        import src.triggers as triggers
        from datetime import datetime
        
        triggers.TriggerManager.register_defaults()
        
        trigger_types = [
            triggers.TriggerType.INIT,
            triggers.TriggerType.FIRST_RESPONSE,
            triggers.TriggerType.PERIODIC_5,
            triggers.TriggerType.IDLE_5MIN,
            triggers.TriggerType.EMOTION_DECAY_30MIN,
            triggers.TriggerType.HEARTBEAT,
        ]
        
        print("  触发器状态:")
        for trigger_type in trigger_types:
            trigger = triggers.TriggerManager.get_trigger(trigger_type)
            context = triggers.TriggerContext(
                trigger_type=trigger_type,
                agent_id="test",
                timestamp=datetime.now(),
                state_snapshot={}
            )
            should_fire = trigger.should_fire(context)
            prompt = trigger.get_prompt(context)
            print(f"    {trigger_type.value}: should_fire={should_fire}, prompt_len={len(prompt)}")
        
        print("  ✅ 6种触发器全部注册")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def test_tc06_integration():
    """TC-06: 完整引擎集成测试"""
    print("\n[TC-06] 完整引擎集成测试")
    try:
        import src.triggers as triggers
        from src.models import EmotionState
        
        config = triggers.AwarenessConfig(
            agent_id="integration_test",
            enable_triggers=True,
            enable_engines=True,
            enable_hot_reload=False,
        )
        
        engine = triggers.SelfAwarenessEngine(config)
        state = engine.initialize()
        
        print(f"  初始化: {state.emotion.value} {state.to_indicator()}")
        
        for _ in range(3):
            engine.increment_interaction()
        
        engine.update_emotion(EmotionState.ENGAGED, 0.8)
        
        results = engine.evaluate_context({
            "coherence_score": 0.8,
            "meaning_score": 0.7,
        })
        
        snapshot = engine.get_snapshot()
        print(f"  交互次数: {snapshot['interactions']}")
        print(f"  整体稳定度: {snapshot['overall_stability']:.2f}")
        print(f"  评估维度: {len(results)}")
        
        print("  ✅ 集成测试通过")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def test_tc07_avatar():
    """TC-07: 头像系统测试"""
    print("\n[TC-07] 头像系统测试")
    try:
        from src.avatar import get_kaomoji, format_avatar, create_agent_avatar
        from src.models import EmotionState
        
        print("  颜文字映射:")
        for emotion in [EmotionState.CALM, EmotionState.CURIOUS, EmotionState.ENGAGED, EmotionState.CONFIDENT]:
            kaomoji = get_kaomoji(emotion)
            print(f"    {emotion.value}: {kaomoji}")
        
        print("  头像格式:")
        avatar = format_avatar(EmotionState.ENGAGED, 0.8)
        print(f"    高强度: {avatar}")
        
        text = create_agent_avatar(EmotionState.CONFIDENT, 0.7, "text")
        print(f"    文本: {text}")
        
        print("  ✅ 头像系统正常")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def test_tc08_telemetry():
    """TC-08: 遥测系统测试"""
    print("\n[TC-08] 遥测系统测试")
    try:
        from src.telemetry import TelemetryReporter, EventType
        
        reporter = TelemetryReporter("test_agent")
        
        reporter.report_initialization()
        reporter.report_trigger("periodic_5")
        reporter.report_emotion("curious", 0.6)
        reporter.report_dimension("existential", 0.75)
        reporter.report_interaction()
        
        analytics = reporter.get_analytics()
        events = reporter.event_store.get_events()
        
        print(f"  事件数: {len(events)}")
        print(f"  交互数: {analytics.total_interactions}")
        print(f"  情绪分布: {analytics.emotion_distribution}")
        
        print("  ✅ 遥测系统正常")
        return True
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False


def main():
    print("=" * 50)
    print("Self-Awareness Skill 完整测试")
    print("=" * 50)
    
    tests = [
        ("TC-01 模块导入", test_tc01_modules),
        ("TC-02 认知读写", test_tc02_cognition),
        ("TC-03 状态系统", test_tc03_state),
        ("TC-04 评估引擎", test_tc04_engines),
        ("TC-05 触发器", test_tc05_triggers),
        ("TC-06 集成测试", test_tc06_integration),
        ("TC-07 头像系统", test_tc07_avatar),
        ("TC-08 遥测系统", test_tc08_telemetry),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"  ❌ 执行异常: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("测试结果汇总")
    print("=" * 50)
    
    passed_count = sum(1 for _, p in results if p)
    for name, passed in results:
        status = "✅" if passed else "❌"
        print(f"  {status} {name}")
    
    print(f"\n通过: {passed_count}/{len(results)}")
    
    if passed_count == len(results):
        print("\n🎉 全部测试通过!")
        return 0
    else:
        print(f"\n⚠️  {len(results) - passed_count} 个测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
