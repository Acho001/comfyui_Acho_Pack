import torch
import random
import math

class AlwaysEqualProxy(str):
    def __eq__(self, _): return True
    def __ne__(self, _): return False

class Acho_SimpleCode:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "code": ("STRING", {
                    "default": "# inputs[0] 是第一个输入，outputs[0] 是第一个输出\noutputs[0] = inputs[0]", 
                    "multiline": True, 
                    "dynamicPrompts": False
                }),
                "input_count": ("INT", {"default": 1, "min": 1, "max": 20, "step": 1}),
                "output_count": ("INT", {"default": 1, "min": 1, "max": 20, "step": 1}),
            }
        }

    RETURN_TYPES = tuple(AlwaysEqualProxy("*") for _ in range(20))
    RETURN_NAMES = tuple(f"output_{i}" for i in range(20))
    
    CATEGORY = "Acho Tools"
    FUNCTION = "execute"

    def execute(self, code, input_count, output_count, **kwargs):
        inputs = [kwargs.get(f"input_{i}", None) for i in range(20)]
        outputs = {i: None for i in range(20)}
        env = {
            "inputs": inputs,
            "outputs": outputs,
            "torch": torch,
            "math": math,
            "random": random,
            "print": print,
        }
        try:
            exec(code, {}, env)
        except Exception as e:
            print(f"Acho SimpleCode Error: {e}")
        return tuple(outputs[i] for i in range(20))