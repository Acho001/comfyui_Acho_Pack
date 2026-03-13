import random

# 【必须保留】通配符类型定义，必须继承 str
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
    def __eq__(self, __value: object) -> bool:
        return True

any_type = AnyType("*")

class AnyInputSwitch:
    # 静态变量，用于记录顺序索引
    _sequence_index = 0

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "mode": (["First Active", "Random", "Sequential"], {"default": "First Active"}),
            },
            "optional": {
                "input0": (any_type,),
                "input1": (any_type,),
                "input2": (any_type,),
                "input3": (any_type,),
                "input4": (any_type,),
                "input5": (any_type,),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("output0",)
    FUNCTION = "switch_logic"
    CATEGORY = "Acho Tools"

    @classmethod
    def IS_CHANGED(s, mode, **kwargs):
        # 随机和顺序模式需要强制每次重跑
        if mode in ["Random", "Sequential"]:
            return float("nan")
        return None

    def switch_logic(self, mode, input0=None, input1=None, input2=None, input3=None, input4=None, input5=None):
        # 1. 收集所有输入
        inputs = [input0, input1, input2, input3, input4, input5]
        
        # 2. 筛选出所有“已连接且非空”的有效输入
        # 这样会自动跳过没连线的端口
        valid_inputs = [x for x in inputs if x is not None]

        # 保护：如果连一根线都没接，只能返回 None
        if not valid_inputs:
            return (None,)

        selected_value = None

        # --- 模式处理 ---
        if mode == "First Active":
            # 取第一个有效值
            selected_value = valid_inputs[0]

        elif mode == "Random":
            # 在有效值里随机挑一个
            selected_value = random.choice(valid_inputs)

        elif mode == "Sequential":
            # 【核心逻辑修正】
            # 对“有效输入的数量”取余，而不是对 6 取余
            # 比如只连了 input0 和 input2，长度是 2
            # index 0 -> input0, index 1 -> input2, index 2 -> input0 ...
            count = len(valid_inputs)
            idx = AnyInputSwitch._sequence_index % count
            
            selected_value = valid_inputs[idx]
            
            # 计数器 +1
            AnyInputSwitch._sequence_index += 1
        
        return (selected_value,)
