#!/usr/bin/env python3
"""
测试自定义输入输出代码节点的功能
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from simple_code import Acho_SimpleCode

def test_basic_functionality():
    """测试基本功能"""
    print("=== 测试基本功能 ===")
    
    node = Acho_SimpleCode()
    
    # 测试代码：简单传递
    code = """
outputs[0] = inputs[0]
outputs[1] = inputs[1] * 2
"""
    
    # 模拟输入参数
    kwargs = {
        'input_0': 10,
        'input_1': 5
    }
    
    result = node.execute(
        code=code,
        add_input=False,
        add_output=False,
        remove_input=False,
        remove_output=False,
        current_inputs=2,
        current_outputs=2,
        **kwargs
    )
    
    print(f"输入: input_0=10, input_1=5")
    print(f"输出: {result['result']}")
    print(f"预期: (10, 10)")
    print()

def test_button_functionality():
    """测试按钮功能"""
    print("=== 测试按钮功能 ===")
    
    node = Acho_SimpleCode()
    
    # 测试添加输入按钮
    result = node.execute(
        code="outputs[0] = len(inputs)",
        add_input=True,
        add_output=False,
        remove_input=False,
        remove_output=False,
        current_inputs=2,
        current_outputs=1,
        input_0=1,
        input_1=2
    )
    
    print(f"添加输入按钮测试:")
    print(f"原输入数量: 2, 新输入数量: {result['input_count']}")
    print(f"输出: {result['result']}")
    print()

def test_math_operations():
    """测试数学运算"""
    print("=== 测试数学运算 ===")
    
    node = Acho_SimpleCode()
    
    code = """
import math
if len(inputs) >= 2:
    outputs[0] = inputs[0] + inputs[1]
    outputs[1] = inputs[0] * inputs[1]
    outputs[2] = math.sqrt(inputs[0]) if inputs[0] >= 0 else 0
"""
    
    kwargs = {
        'input_0': 16,
        'input_1': 4
    }
    
    result = node.execute(
        code=code,
        add_input=False,
        add_output=False,
        remove_input=False,
        remove_output=False,
        current_inputs=2,
        current_outputs=3,
        **kwargs
    )
    
    print(f"数学运算测试:")
    print(f"输入: 16, 4")
    print(f"输出: {result['result']}")
    print(f"预期: (20, 64, 4.0)")
    print()

def test_tensor_operations():
    """测试张量运算"""
    print("=== 测试张量运算 ===")
    
    import torch
    
    node = Acho_SimpleCode()
    
    code = """
if len(inputs) > 0 and hasattr(inputs[0], 'mean'):
    outputs[0] = inputs[0].mean()
    outputs[1] = inputs[0].std()
"""
    
    # 创建测试张量
    tensor_input = torch.tensor([1.0, 2.0, 3.0, 4.0, 5.0])
    
    kwargs = {
        'input_0': tensor_input
    }
    
    result = node.execute(
        code=code,
        add_input=False,
        add_output=False,
        remove_input=False,
        remove_output=False,
        current_inputs=1,
        current_outputs=2,
        **kwargs
    )
    
    print(f"张量运算测试:")
    print(f"输入: {tensor_input}")
    print(f"输出: {result['result']}")
    print()

if __name__ == "__main__":
    print("开始测试自定义输入输出代码节点...")
    print()
    
    try:
        test_basic_functionality()
        test_button_functionality()
        test_math_operations()
        test_tensor_operations()
        
        print("✅ 所有测试通过!")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()