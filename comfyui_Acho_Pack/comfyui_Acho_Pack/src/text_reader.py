import os
import random

class Acho_TextReader:
    """
    通用文本文件读取节点
    每次运行都可以重新读取文件内容，支持任意文本格式
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": "data.txt",
                    "multiline": False,
                }),
                "random_seed": ("BOOLEAN", {
                    "default": True,
                }),
                "seed": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 0xffffffffffffffff,
                }),
            },
            "optional": {
                "default_content": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("content", "file_path", "seed")
    FUNCTION = "read_text"
    CATEGORY = "Acho Tools/File IO"
    
    @classmethod
    def IS_CHANGED(s, file_path, random_seed, seed, default_content=""):
        # 如果开启随机seed，每次都返回随机数强制重新执行
        if random_seed:
            return float("nan")
        # 如果是固定seed，返回seed值和文件路径的组合
        return (seed, file_path)
    
    def read_text(self, file_path, random_seed, seed, default_content=""):
        """
        读取文本文件并返回内容
        
        Args:
            file_path: 文件路径（相对或绝对路径）
            random_seed: 是否使用随机seed
            seed: 固定seed值
            default_content: 文件不存在时的默认内容
            
        Returns:
            (content, file_path, seed): 文件内容、实际文件路径、实际使用的seed
        """
        # 如果是随机模式，生成新的seed
        if random_seed:
            actual_seed = random.randint(0, 0xffffffffffffffff)
            print(f"[Acho_TextReader] 随机模式 - seed: {actual_seed}")
        else:
            actual_seed = seed
            print(f"[Acho_TextReader] 固定模式 - seed: {actual_seed}")
        
        try:
            # 获取当前工作目录
            current_dir = os.getcwd()
            print(f"[Acho_TextReader] 当前工作目录: {current_dir}")
            print(f"[Acho_TextReader] 输入文件路径: {file_path}")
            
            # 处理相对路径
            if not os.path.isabs(file_path):
                abs_path = os.path.abspath(file_path)
            else:
                abs_path = file_path
            
            print(f"[Acho_TextReader] 完整路径: {abs_path}")
            
            # 检查文件是否存在
            if not os.path.exists(abs_path):
                print(f"[Acho_TextReader] 文件不存在，使用默认内容")
                return (default_content, abs_path, actual_seed)
            
            # 读取文件内容
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"[Acho_TextReader] 成功读取文件，大小: {len(content)} 字符")
            return (content, abs_path, actual_seed)
                
        except Exception as e:
            print(f"[Acho_TextReader] 读取文件时出错: {e}")
            print(f"[Acho_TextReader] 使用默认内容")
            return (default_content, file_path, actual_seed)
