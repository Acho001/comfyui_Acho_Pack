#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON格式测试脚本
用于测试和验证JSON字符串的格式是否正确
"""

import json

def test_json_string(json_str):
    """测试JSON字符串是否有效"""
    print("=" * 60)
    print("测试JSON字符串")
    print("=" * 60)
    
    print(f"\n原始内容（repr）:")
    print(repr(json_str))
    
    print(f"\n原始内容（str）:")
    print(json_str)
    
    print(f"\n内容长度: {len(json_str)} 字符")
    
    try:
        data = json.loads(json_str)
        print("\n✅ JSON格式正确!")
        print("\n解析后的数据:")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    except json.JSONDecodeError as e:
        print(f"\n❌ JSON格式错误!")
        print(f"错误信息: {e}")
        print(f"错误位置: 第{e.lineno}行 第{e.colno}列")
        print(f"错误内容: {repr(json_str[max(0, e.pos-20):e.pos+20])}")
        return False

if __name__ == "__main__":
    print("JSON格式测试工具\n")
    
    # 测试案例
    test_cases = [
        # 正确的格式
        ('{"name": "test"}', "正确格式 - 简单对象"),
        ('{"name": "测试", "value": 123}', "正确格式 - 中文字符"),
        ('{"list": [1, 2, 3]}', "正确格式 - 数组"),
        
        # 错误的格式
        ("{'name': 'test'}", "错误格式 - 单引号"),
        ('{name: "test"}', "错误格式 - 键名无引号"),
        ('{"name": "test",}', "错误格式 - 尾随逗号"),
    ]
    
    for json_str, description in test_cases:
        print(f"\n\n【{description}】")
        test_json_string(json_str)
    
    # 交互式测试
    print("\n\n" + "=" * 60)
    print("交互式测试 - 请输入你的JSON字符串")
    print("=" * 60)
    print("提示: 直接粘贴你在ComfyUI中使用的内容")
    print("提示: 输入 'quit' 退出\n")
    
    while True:
        try:
            user_input = input("\n请输入JSON字符串: ")
            if user_input.lower() == 'quit':
                break
            test_json_string(user_input)
        except KeyboardInterrupt:
            print("\n\n退出测试")
            break
        except Exception as e:
            print(f"\n发生错误: {e}")
