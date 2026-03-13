import json
import os
import random

class Acho_JSONReader:
    """
    每次运行都重新读取JSON文档的节点
    支持指定路径或自动查找项目根目录下的JSON文件
    带有seed控制，可以选择固定读取或每次随机读取
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {
                    "default": "data.json",
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
                    "default": "{}",
                    "multiline": True,
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("json_string", "file_path", "debug_info", "seed")
    FUNCTION = "read_json"
    CATEGORY = "Acho Tools/JSON"
    
    @classmethod
    def IS_CHANGED(s, file_path, random_seed, seed, default_content="{}"):
        # 如果开启随机seed，每次都返回随机数强制重新执行
        if random_seed:
            return float("nan")
        # 如果是固定seed，返回seed值和文件路径的组合
        # 这样只有seed或文件路径改变时才会重新执行
        return (seed, file_path)
    
    def read_json(self, file_path, random_seed, seed, default_content="{}"):
        """
        读取JSON文件并返回内容
        
        Args:
            file_path: JSON文件路径（相对或绝对路径）
            random_seed: 是否使用随机seed（True=每次都重新读取，False=使用固定seed）
            seed: 固定seed值（仅在random_seed=False时使用）
            default_content: 文件不存在时的默认内容
            
        Returns:
            (json_string, file_path, debug_info, seed): JSON内容、实际文件路径、调试信息和实际使用的seed
        """
        debug_info = []
        
        # 如果是随机模式，生成新的seed
        if random_seed:
            actual_seed = random.randint(0, 0xffffffffffffffff)
            debug_info.append(f"随机模式 - 生成seed: {actual_seed}")
            print(f"[Acho_JSONReader] 随机模式 - 生成seed: {actual_seed}")
        else:
            actual_seed = seed
            debug_info.append(f"固定模式 - 使用seed: {actual_seed}")
            print(f"[Acho_JSONReader] 固定模式 - 使用seed: {actual_seed}")
        
        try:
            # 获取当前工作目录
            current_dir = os.getcwd()
            debug_info.append(f"当前工作目录: {current_dir}")
            print(f"[Acho_JSONReader] 当前工作目录: {current_dir}")
            print(f"[Acho_JSONReader] 输入文件路径: {file_path}")
            
            # 处理相对路径：如果是相对路径，基于当前工作目录
            if not os.path.isabs(file_path):
                # 尝试从当前目录查找
                abs_path = os.path.abspath(file_path)
                debug_info.append(f"相对路径转绝对路径: {abs_path}")
            else:
                abs_path = file_path
                debug_info.append(f"使用绝对路径: {abs_path}")
            
            print(f"[Acho_JSONReader] 完整路径: {abs_path}")
            
            # 检查文件是否存在
            if not os.path.exists(abs_path):
                error_msg = f"文件不存在: {abs_path}"
                debug_info.append(error_msg)
                print(f"[Acho_JSONReader] {error_msg}")
                print(f"[Acho_JSONReader] 使用默认内容: {default_content}")
                
                # 文件不存在时返回默认内容
                debug_str = "\n".join(debug_info)
                return (default_content, abs_path, debug_str, actual_seed)
            
            # 读取JSON文件
            debug_info.append(f"文件存在，准备读取")
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            debug_info.append(f"文件读取成功，大小: {len(content)} 字符")
            
            # 验证JSON格式
            try:
                parsed_data = json.loads(content)
                debug_info.append(f"JSON格式验证通过")
                print(f"[Acho_JSONReader] 成功读取并解析: {abs_path}")
                
                debug_str = "\n".join(debug_info)
                return (content, abs_path, debug_str, actual_seed)
                
            except json.JSONDecodeError as e:
                error_msg = f"JSON格式错误: {e}"
                debug_info.append(error_msg)
                print(f"[Acho_JSONReader] {error_msg}")
                print(f"[Acho_JSONReader] 使用默认内容")
                
                debug_str = "\n".join(debug_info)
                return (default_content, abs_path, debug_str, actual_seed)
                
        except Exception as e:
            error_msg = f"读取文件时出错: {e}"
            debug_info.append(error_msg)
            print(f"[Acho_JSONReader] {error_msg}")
            print(f"[Acho_JSONReader] 使用默认内容")
            
            debug_str = "\n".join(debug_info)
            return (default_content, file_path, debug_str, actual_seed)
