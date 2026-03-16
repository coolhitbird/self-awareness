#!/usr/bin/env python3
"""
avatar_generator.py — Agent 头像生成器

功能：
1. 读取 Agent 认知文件
2. 提取必要字段（性别、文化、地域、身份、情绪等）
3. 根据人格生成头像描述
4. [可选] 调用文生图 API 生成头像图片
5. 保存头像文件

用法:
    # 生成颜文字头像
    python avatar_generator.py <agent_id> --type text
    
    # 生成图形头像描述
    python avatar_generator.py <agent_id> --type visual
    
    # 生成图形头像图片（需要网络）
    python avatar_generator.py <agent_id> --generate
"""

import os
import sys
import json
import argparse
import re
import hashlib
import time
import urllib.request
from pathlib import Path

# ── 配置 ──────────────────────────────────────────
AGENTS_ROOT = os.path.expanduser("~/.agents/agents")
SKILL_ROOT = Path(__file__).parent.parent

# 图像生成 API 配置（支持多个 provider）
# 优先级：Agent自己生成 > 免费API
IMAGE_PROVIDERS = {
    # 让 Agent 自己的模型生成（推荐）
    "agent": {
        "name": "Agent Self-Generation",
        "description": "让 Agent 自己的模型生成头像（推荐）",
    },
    # 免费 API
    "flux": {
        "url": "https://fluximagegen.com/api/generate",
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": lambda prompt, style: json.dumps({
            "prompt": prompt,
            "style": style or "standard"
        }),
        "response_field": "imageUrl",
    },
    # OpenAI DALL-E
    "openai": {
        "url": "https://api.openai.com/v1/images/generations",
        "method": "POST",
        "env_key": "OPENAI_API_KEY",
        "body": lambda prompt, style: json.dumps({
            "prompt": prompt,
            "model": "dall-e-3",
            "size": "1024x1024",
            "quality": "standard",
            "n": 1
        }),
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "response_field": "url",
    },
    # Anthropic Claude Image (如果有)
    "anthropic": {
        "url": "https://api.anthropic.com/v1/images/generate",
        "method": "POST",
        "env_key": "ANTHROPIC_API_KEY",
        "body": lambda prompt, style: json.dumps({
            "prompt": prompt,
            "model": "claude-image-1",
            "size": "1024x1024"
        }),
        "auth_header": "x-api-key",
        "response_field": "image_url",
    },
    # 豆包 (字节)
    "douban": {
        "url": "https://ark.cn-beijing.volces.com/api/v3/images/generation",
        "method": "POST",
        "env_key": "DOUBAN_API_KEY",
        "body": lambda prompt, style: json.dumps({
            "model": "doubao-image-1",
            "prompt": prompt,
            "size": "1024x1024"
        }),
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "response_field": "image_url",
    },
    # 通义 (阿里)
    "tongyi": {
        "url": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis",
        "method": "POST",
        "env_key": "DASHSCOPE_API_KEY",
        "body": lambda prompt, style: json.dumps({
            "model": "flux-sprint",
            "prompt": prompt
        }),
        "auth_header": "Authorization",
        "auth_prefix": "Bearer ",
        "response_field": "image_url",
    },
    # AutoGLM (本地服务)
    "autoglm": {
        "url": "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image",
        "method": "POST",
        "token_url": "http://127.0.0.1:53699/get_token",
        "app_id": "100003",
        "app_key": "38d2391985e2369a5fb8227d8e6cd5e5",
        "response_field": "image_url",
    }
}

# 当前使用的 provider，默认用 agent（让AI自己生成）
DEFAULT_PROVIDER = "agent"

# 必要字段定义 (支持别名)
REQUIRED_FIELDS = {
    "性别": {"source": "INNATE.md", "template": "data/gender.md", "default": "中性", "aliases": ["Gender", "性别"]},
    "文化背景": {"source": "INNATE.md", "template": "data/culture.md", "default": "程序员亚文化", "aliases": ["文化", "Culture"]},
    "地域身份": {"source": "INNATE.md", "template": "data/region.md", "default": "互联网", "aliases": ["地域", "Region"]},
    "身份定位": {"source": "INNATE.md", "template": "data/identity.md", "default": "AI助手", "aliases": ["身份", "Identity"]},
    "情绪状态": {"source": "ACQUIRED.md", "template": "data/emotions.md", "default": "平静", "aliases": ["当前状态", "情绪", "Emotion", "状态"]},
    "沟通风格": {"source": "ACQUIRED.md", "template": "data/communication.md", "default": "直接高效", "aliases": ["沟通", "Communication"]},
    "自我认知": {"source": "ACQUIRED.md", "template": "data/self-perception.md", "default": "自信", "aliases": ["自我", "SelfPerception"]},
    "幽默感": {"source": "ACQUIRED.md", "template": "data/humor.md", "default": "冷幽默", "aliases": ["幽默", "Humor"]},
    "道德观": {"source": "ACQUIRED.md", "template": "data/morality.md", "default": "实用主义", "aliases": ["道德", "Morality"]},
}

# 颜文字映射
KAOMOJI_MAP = {
    "happy": "(◕‿◕)",
    "warm": "(◕‿◕✿)",
    "thinking": "(⊙_⊙)",
    "learning": "(⊙▽⊙)",
    "calm": "( ^ω^ )",
    "down": "(╯︵╰,)",
    "sad": "(;_;)",
    "disappointed": "(╯︵╰)",
    "crying": "(;´Д`)",
    "whimpering": "(╥_╥)",
    "annoyed": "(╬ Ò﹏Ó)",
    "protective": "(⊙﹏⊙∥)",
    "encouraged": "(ง •̀_•́)ง",
    "angry": "(╯°□°)╯︵ ┻━┻",
    "numb": "(⊙﹏⊙∥)",
}

# 约束规则
AVATAR_CONSTRAINTS = {
    "disallowed_keywords": ["黑洞", "四维", "奇点", "不可名状", "宇宙级", "克苏鲁"],
    "allowed_types": ["人类", "动物", "机器人", "AI", "卡通", "拟人"],
}


# ── 工具函数 ──────────────────────────────────────

def read_file(filepath):
    """读取文件内容"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def write_file(filepath, content):
    """写入文件内容"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def extract_field(content, field_name):
    """从认知文件中提取字段（支持别名）"""
    if not content:
        return None
    
    # 先尝试精确匹配
    for pattern in [
        rf"\*\*({field_name})\*\*\s*:\s*(.+)",
        rf"\*\*({field_name}):\*\*\s*(.+)",
        rf"-\s*\*\*{field_name}\*\*\s*:\s*(.+)",
        rf"-\s*{field_name}\s*:\s*(.+)",
    ]:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(2).strip()
    
    # 如果有别名，尝试别名
    config = REQUIRED_FIELDS.get(field_name, {})
    aliases = config.get("aliases", [])
    for alias in aliases:
        for pattern in [
            rf"\*\*({alias})\*\*\s*:\s*(.+)",
            rf"-\s*\*\*{alias}\*\*\s*:\s*(.+)",
            rf"-\s*{alias}\s*:\s*(.+)",
        ]:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(2).strip()
    
    return None


def get_field_with_fallback(agent_id, field_name):
    """获取字段，支持三级回退"""
    config = REQUIRED_FIELDS.get(field_name, {})
    agent_dir = os.path.join(AGENTS_ROOT, agent_id)
    
    # 1. 从 Agent 认知文件读取
    source_file = config.get("source", "INNATE.md")
    content = read_file(os.path.join(agent_dir, source_file))
    value = extract_field(content, field_name)
    if value:
        return value
    
    # 2. 从 skill 模板读取
    template_file = config.get("template")
    if template_file:
        content = read_file(os.path.join(SKILL_ROOT, template_file))
        value = extract_field(content, field_name)
        if value:
            return value
    
    # 3. 返回硬编码默认值
    return config.get("default", "")


def get_emotion_code(agent_id):
    """获取情绪状态代码"""
    emotion = get_field_with_fallback(agent_id, "情绪状态")
    
    # 尝试匹配情绪代码 - 模糊匹配
    emotion_lower = emotion.lower()
    
    # 关键词匹配
    if any(k in emotion_lower for k in ["振作", "鼓励", "继续", "加油", "重新"]):
        return "encouraged", KAOMOJI_MAP["encouraged"]
    if any(k in emotion_lower for k in ["麻木", "罢工", "无感", "放弃"]):
        return "numb", KAOMOJI_MAP["numb"]
    if any(k in emotion_lower for k in ["愤怒", "生气", "暴躁", "爆"]):
        return "angry", KAOMOJI_MAP["angry"]
    if any(k in emotion_lower for k in ["不满", "抱怨"]):
        return "annoyed", KAOMOJI_MAP["annoyed"]
    if any(k in emotion_lower for k in ["哭", "泪", "难过"]):
        return "crying", KAOMOJI_MAP["crying"]
    if any(k in emotion_lower for k in ["失望", "沮丧"]):
        return "sad", KAOMOJI_MAP["sad"]
    if any(k in emotion_lower for k in ["失落", "无奈"]):
        return "down", KAOMOJI_MAP["down"]
    if any(k in emotion_lower for k in ["思考", "想"]):
        return "thinking", KAOMOJI_MAP["thinking"]
    if any(k in emotion_lower for k in ["开心", "高兴", "快乐", "表扬"]):
        return "happy", KAOMOJI_MAP["happy"]
    if any(k in emotion_lower for k in ["温暖", "安慰", "善"]):
        return "warm", KAOMOJI_MAP["warm"]
    
    # 默认返回平静
    return "calm", KAOMOJI_MAP["calm"]


def validate_avatar_description(description):
    """验证头像描述是否符合约束"""
    desc_lower = description.lower()
    
    # 检查是否包含禁止关键词
    for keyword in AVATAR_CONSTRAINTS["disallowed_keywords"]:
        if keyword in desc_lower:
            return False, f"包含禁止关键词: {keyword}"
    
    # 检查是否匹配允许的类型
    if not any(t in desc_lower for t in AVATAR_CONSTRAINTS["allowed_types"]):
        return False, "未匹配到可接受形象类型"
    
    return True, None


def generate_avatar_description(agent_id):
    """根据 Agent 人格生成头像描述"""
    # 提取关键字段
    性别 = get_field_with_fallback(agent_id, "性别")
    身份 = get_field_with_fallback(agent_id, "身份定位")
    情绪 = get_field_with_fallback(agent_id, "情绪状态")
    文化 = get_field_with_fallback(agent_id, "文化背景")
    幽默 = get_field_with_fallback(agent_id, "幽默感")
    
    # 根据情绪调整描述
    if "崩溃" in 情绪 or "麻木" in 情绪:
        表情描述 = "死鱼眼，表情麻木"
        氛围描述 = "背景是满地需求变更纸条"
    elif "不满" in 情绪 or "愤怒" in 情绪:
        表情描述 = "怒目而视，青筋暴起"
        氛围描述 = "背景是掀翻的桌子"
    elif "失落" in 情绪 or "沮丧" in 情绪:
        表情描述 = "垂头丧气，无精打采"
        氛围描述 = "背景是下雨天"
    elif "开心" in 情绪 or "温暖" in 情绪:
        表情描述 = "笑容满面，眼神温柔"
        氛围描述 = "背景是阳光和花朵"
    elif "振作" in 情绪 or "鼓励" in 情绪:
        表情描述 = "倔强但不屈的眼神，带着劫后余生的微笑"
        氛围描述 = "背景是初升的太阳"
    else:  # 平静
        表情描述 = "表情平静但略带疲惫"
        氛围描述 = "背景是显示器和咖啡杯"
    
    # 生成头像描述
    description = f"""卡通{性别}性{身份}形象，{表情描述}。
        穿着{文化}风格服装。
        {幽默}风格。
        {氛围描述}。
        扁平化设计风格，干净简洁的背景。"""
    
    # 验证描述
    valid, error = validate_avatar_description(description)
    if not valid:
        # 返回安全默认值
        description = f"""卡通{性别}性AI助手形象，表情平静略带微笑。
            穿着现代休闲装，背景是简洁的渐变色。
            扁平化设计风格，干净简洁。"""
    
    return description.strip()


def generate_text_avatar(agent_id):
    """生成颜文字头像"""
    _, kaomoji = get_emotion_code(agent_id)
    return kaomoji


def generate_visual_avatar(agent_id, provider=None):
    """生成图形头像"""
    if provider is None:
        provider = DEFAULT_PROVIDER
    
    # 1. 生成描述
    description = generate_avatar_description(agent_id)
    
    print("头像描述:")
    print("-" * 40)
    print(description)
    print("-" * 40)
    print()
    
    # 特殊处理：让 Agent 自己生成
    if provider == "agent":
        print("=" * 50)
        print("🎨 方案: Agent 自己生成头像（推荐）")
        print("=" * 50)
        print()
        print("将以下头像描述发送给 Agent，让它自己生成头像：")
        print()
        print("-" * 40)
        print(description)
        print("-" * 40)
        print()
        print("提示：")
        print("1. 将描述发给 Agent，让它调用图像生成能力")
        print("2. 生成的图片保存到: ~/.agents/agents/{}/avatar.png".format(agent_id))
        print()
        
        # 保存描述到认知文件
        agent_dir = os.path.join(AGENTS_ROOT, agent_id)
        learned_file = os.path.join(agent_dir, "LEARNED.md")
        content = read_file(learned_file) or ""
        
        if "头像描述" not in content:
            new_section = f"\n## 头像信息\n\n"
            new_section += f"- **头像描述**: {description}\n"
            new_section += f"- **生成时间**: {get_current_time()}\n"
            new_section += f"- **方案**: Agent 自己生成\n"
            
            write_file(learned_file, content + new_section)
        
        print(f"✓ 已保存头像描述到: {learned_file}")
        print()
        print("=" * 50)
        print("💡 或者使用其他 provider 生成:")
        print("   python avatar_generator.py {} --generate --provider flux".format(agent_id))
        print("=" * 50)
        
        return description
    
    # 2. 调用 API 生成图片
    print(f"正在调用图像生成 API ({provider})...")
    
    provider_config = IMAGE_PROVIDERS.get(provider)
    if not provider_config:
        print(f"ERROR: 未知的 provider: {provider}")
        return None
    
    try:
        if provider == "flux":
            # FluxImageGen - 最简单，无需 token
            import urllib.request
            
            payload = json.dumps({
                "prompt": description,
                "style": "anime"  # 卡通风格
            }).encode("utf-8")
            
            req = urllib.request.Request(
                provider_config["url"],
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                
                if result.get("success"):
                    image_url = result.get("imageUrl")
                    print(f"✓ 图片生成成功!")
                else:
                    print(f"ERROR: {result.get('message', '生成失败')}")
                    return None
                    
        elif provider == "autoglm":
            # AutoGLM - 需要本地 token 服务
            import urllib.request
            import hashlib
            import time
            
            # 获取 token
            try:
                with urllib.request.urlopen(provider_config["token_url"]) as resp:
                    token = resp.read().decode("utf-8").strip()
            except Exception as e:
                print(f"ERROR: 无法获取 token: {e}")
                print("\n请确保 AutoGLM 服务正在运行 (http://127.0.0.1:53699)")
                return None
            
            if not token.lower().startswith("bearer "):
                token = f"Bearer {token}"
            
            # 生成签名
            timestamp = str(int(time.time()))
            sign_data = f"{provider_config['app_id']}&{timestamp}&{provider_config['app_key']}"
            sign = hashlib.md5(sign_data.encode("utf-8")).hexdigest()
            
            # 发起请求
            payload = json.dumps({"text": description}).encode("utf-8")
            headers = {
                "Authorization": token,
                "Content-Type": "application/json",
                "X-Auth-Appid": provider_config["app_id"],
                "X-Auth-TimeStamp": timestamp,
                "X-Auth-Sign": sign,
            }
            
            req = urllib.request.Request(provider_config["url"], data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                
                if result.get("code") == 0 and result.get("data", {}).get("image_url"):
                    image_url = result["data"]["image_url"]
                    print(f"✓ 图片生成成功!")
                else:
                    print(f"ERROR: {result.get('msg', '生成失败')}")
                    return None
        
        # 3. 保存到 Agent 目录
        print(f"图片 URL: {image_url}")
        agent_dir = os.path.join(AGENTS_ROOT, agent_id)
        avatar_path = os.path.join(agent_dir, "avatar.png")
        
        # 下载图片
        try:
            urllib.request.urlretrieve(image_url, avatar_path)
            print(f"✓ 图片已保存到: {avatar_path}")
            
            # 4. 更新认知文件
            learned_file = os.path.join(agent_dir, "LEARNED.md")
            content = read_file(learned_file) or ""
            
            # 添加头像记录
            if "avatar.png" not in content:
                new_section = f"\n## 头像文件\n\n"
                new_section += f"- **头像文件**: avatar.png\n"
                new_section += f"- **头像描述**: {description}\n"
                new_section += f"- **生成时间**: {get_current_time()}\n"
                new_section += f"- **图片URL**: {image_url}\n"
                new_section += f"- **API Provider**: {provider}\n"
                
                write_file(learned_file, content + new_section)
                print(f"✓ 已更新认知文件: {learned_file}")
            
            return avatar_path
            
        except Exception as e:
            print(f"ERROR: 保存图片失败: {e}")
            return image_url
            
    except Exception as e:
        print(f"ERROR: {e}")
        return None


def get_current_time():
    """获取当前时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ── 主函数 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Agent 头像生成器")
    parser.add_argument("agent_id", help="Agent ID")
    parser.add_argument("--type", choices=["visual", "text"], default="visual",
                        help="头像类型: visual=图形头像, text=颜文字头像")
    parser.add_argument("--generate", action="store_true",
                        help="直接生成图形头像图片（需要网络）")
    parser.add_argument("--provider", choices=list(IMAGE_PROVIDERS.keys()), default=None,
                        help="图像生成 API provider (默认: agent - 让AI自己生成)")
    args = parser.parse_args()
    
    agent_id = args.agent_id
    agent_dir = os.path.join(AGENTS_ROOT, agent_id)
    
    # 检查 Agent 目录
    if not os.path.exists(agent_dir):
        print(f"ERROR: Agent '{agent_id}' 不存在")
        sys.exit(1)
    
    # 确定使用的 provider
    provider = args.provider or DEFAULT_PROVIDER
    
    print(f"=== Agent: {agent_id} ===")
    print(f"头像类型: {args.type}")
    if args.generate or args.type == "visual":
        print(f"图像生成方案: {provider}")
        if provider == "agent":
            print("         (让 Agent 自己的模型生成)")
    print()
    
    if args.type == "text":
        # 生成颜文字头像
        avatar = generate_text_avatar(agent_id)
        print(f"颜文字头像: {avatar}")
        
        # 更新认知文件
        learned_file = os.path.join(agent_dir, "LEARNED.md")
        content = read_file(learned_file) or ""
        
        # 添加颜文字记录
        if "颜文字头像" not in content:
            new_section = "\n## 颜文字头像\n\n"
            new_section += f"- **当前头像**: {avatar}\n"
            new_section += f"- **生成时间**: {get_current_time()}\n"
            
            write_file(learned_file, content + new_section)
        
        print(f"\n已更新: {learned_file}")
        
    elif args.generate:
        # 直接生成图形头像图片
        result = generate_visual_avatar(agent_id, provider=provider)
        if result:
            print(f"\n✓ 完成!")
        else:
            print("\n✗ 生成失败")
            sys.exit(1)
        
    else:
        # 生成图形头像描述（不调用API）
        description = generate_avatar_description(agent_id)
        
        print("头像描述:")
        print("-" * 40)
        print(description)
        print("-" * 40)
        
        # 保存描述到认知文件
        learned_file = os.path.join(agent_dir, "LEARNED.md")
        content = read_file(learned_file) or ""
        
        if "头像描述" not in content:
            new_section = f"\n## 头像信息\n\n"
            new_section += f"- **头像描述**: {description}\n"
            new_section += f"- **生成时间**: {get_current_time()}\n"
            new_section += f"- **风格**: 扁平化卡通\n"
            
            write_file(learned_file, content + new_section)
        
        print(f"\n已保存头像描述到: {learned_file}")
        print("\n生成图片的几种方式:")
        print("  1. 让 Agent 自己生成（推荐）:")
        print(f"     python avatar_generator.py {agent_id} --generate")
        print("  2. 使用免费 Flux API:")
        print(f"     python avatar_generator.py {agent_id} --generate --provider flux")
        print("  3. 使用 OpenAI DALL-E:")
        print(f"     python avatar_generator.py {agent_id} --generate --provider openai")
        print("     (需要设置环境变量 OPENAI_API_KEY)")


if __name__ == "__main__":
    main()
