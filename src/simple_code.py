import torch
import random
import math

# 修复转圈 Bug 的关键类
class AlwaysEqualProxy(str):
    def __eq__(self, _): return True
    def __ne__(self, _): return False

class Acho_SimpleCode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 更新了默认代码提示，使用全称
                "code": ("STRING", {
                    "default": "# 标准写法：\n# outputs[0] = inputs[0]\n\n# 运算示例：\n# outputs[1] = inputs[1] * 2", 
                    "multiline": True, 
                    "dynamicPrompts": False
                })
            },
            "optional": {
                "input0": (AlwaysEqualProxy("*"),),
                "input1": (AlwaysEqualProxy("*"),),
                "input2": (AlwaysEqualProxy("*"),),
                "input3": (AlwaysEqualProxy("*"),),
                "input4": (AlwaysEqualProxy("*"),),
                "input5": (AlwaysEqualProxy("*"),),
            }
        }

    CATEGORY = "Acho Tools"
    RETURN_TYPES = tuple(AlwaysEqualProxy("*") for _ in range(6))
    RETURN_NAMES = tuple(f"output_{i}" for i in range(6))
    FUNCTION = "execute"

    def execute(self, code, input0=None, input1=None, input2=None, input3=None, input4=None, input5=None):
        # 1. 整理原始输入
        raw_inputs = [input0, input1, input2, input3, input4, input5]
        
        # 2. 智能计算默认值 (保持这个好用的功能)
        # 找到第一个非空的输入作为参考
        ref = next((x for x in raw_inputs if x is not None), None)
        
        def get_zero(val):
            if val is None: return 0
            if isinstance(val, torch.Tensor): return torch.zeros_like(val)
            if isinstance(val, (int, float)): return 0
            if isinstance(val, str): return ""
            if isinstance(val, list): return []
            return None

        default_val = get_zero(ref)

        # 3. 准备执行环境 (取消缩写，使用全称)
        
        # inputs: 是一个列表 (List)。使用 inputs[0] 访问 input0
        inputs = [x if x is not None else default_val for x in raw_inputs]
        
        # outputs: 是一个字典 (Dict)。使用 outputs[0] = ... 赋值
        outputs = {i: default_val for i in range(6)}

        # 4. 注入环境变量
        env = {
            "inputs": inputs,   # 核心输入列表
            "outputs": outputs, # 核心输出字典
            
            # 内置常用库，方便调用
            "print": print, "len": len, "range": range, "int": int, "float": float, "str": str,
            "torch": torch,
            "math": math,
            "random": random,
        }

        # 5. 执行代码
        try:
            exec(code, {}, env)
        except Exception as e:
            raise RuntimeError(f"代码执行错误:\n{str(e)}\n\n请检查是否使用了 inputs[0] 和 outputs[0]")

        # 6. 返回结果
        return tuple(outputs.get(i, default_val) for i in range(6))
