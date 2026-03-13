import os
import random
from datetime import datetime

class Acho_TextWriter:
    """
    通用文本文件写入节点
    每次运行后都可以写入文本内容，支持任意文本格式
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "content": ("STRING", {
                    "default": "",
                    "multiline": True,
                }),
                "file_path": ("STRING", {
                    "default": "output.txt",
                    "multiline": False,
                }),
                "write_mode": (["overwrite", "append"], {
                    "default": "overwrite"
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
                "auto_backup": ("BOOLEAN", {
                    "default": False,
                }),
                "create_dir": ("BOOLEAN", {
                    "default": True,
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("status", "file_path", "seed")
    FUNCTION = "write_text"
    CATEGORY = "Acho Tools/File IO"
    
    @classmethod
    def IS_CHANGED(s, content, file_path, write_mode, random_seed, seed, auto_backup=False, create_dir=True):
        # 如果开启随机seed，每次都返回随机数强制重新执行
        if random_seed:
            return float("nan")
        # 如果是固定seed，返回seed值、文件路径和内容的组合
        return (seed, file_path, content)
    
    def write_text(self, content, file_path, write_mode, random_seed, seed, auto_backup=False, create_dir=True):
        """
        写入文本内容到文件
        
        Args:
            content: 要写入的文本内容
            file_path: 文件路径（相对或绝对路径）
            write_mode: 写入模式 - "overwrite"(覆盖) 或 "append"(追加)
            random_seed: 是否使用随机seed
            seed: 固定seed值
            auto_backup: 是否自动备份原文件
            create_dir: 是否自动创建不存在的目录
            
        Returns:
            (status, file_path, seed): 状态信息、实际文件路径、实际使用的seed
        """
        # 如果是随机模式，生成新的seed
        if random_seed:
            actual_seed = random.randint(0, 0xffffffffffffffff)
            print(f"[Acho_TextWriter] 随机模式 - seed: {actual_seed}")
        else:
            actual_seed = seed
            print(f"[Acho_TextWriter] 固定模式 - seed: {actual_seed}")
        
        try:
            # 获取当前工作目录
            current_dir = os.getcwd()
            print(f"[Acho_TextWriter] 当前工作目录: {current_dir}")
            print(f"[Acho_TextWriter] 输入文件路径: {file_path}")
            print(f"[Acho_TextWriter] 写入模式: {write_mode}")
            print(f"[Acho_TextWriter] 内容长度: {len(content)} 字符")
            
            # 处理相对路径
            if not os.path.isabs(file_path):
                abs_path = os.path.abspath(file_path)
            else:
                abs_path = file_path
            
            print(f"[Acho_TextWriter] 完整路径: {abs_path}")
            
            # 获取目录路径
            dir_path = os.path.dirname(abs_path)
            
            # 创建目录（如果需要）
            if dir_path and not os.path.exists(dir_path):
                if create_dir:
                    os.makedirs(dir_path, exist_ok=True)
                    print(f"[Acho_TextWriter] 创建目录: {dir_path}")
                else:
                    error_msg = f"目录不存在且未启用自动创建: {dir_path}"
                    print(f"[Acho_TextWriter] {error_msg}")
                    return (f"ERROR: {error_msg}", abs_path, actual_seed)
            
            # 备份原文件（如果存在且需要备份）
            if auto_backup and os.path.exists(abs_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{abs_path}.backup_{timestamp}"
                try:
                    with open(abs_path, 'r', encoding='utf-8') as f_src:
                        with open(backup_path, 'w', encoding='utf-8') as f_dst:
                            f_dst.write(f_src.read())
                    print(f"[Acho_TextWriter] 已备份到: {backup_path}")
                except Exception as e:
                    print(f"[Acho_TextWriter] 备份失败: {e}")
            
            # 写入文件
            mode = 'a' if write_mode == "append" else 'w'
            with open(abs_path, mode, encoding='utf-8') as f:
                f.write(content)
            
            status_msg = f"SUCCESS: 已保存到 {abs_path} (模式: {write_mode}, {len(content)} 字符)"
            print(f"[Acho_TextWriter] {status_msg}")
            
            return (status_msg, abs_path, actual_seed)
            
        except Exception as e:
            error_msg = f"写入文件时出错: {e}"
            print(f"[Acho_TextWriter] {error_msg}")
            return (f"ERROR: {error_msg}", file_path, actual_seed)
