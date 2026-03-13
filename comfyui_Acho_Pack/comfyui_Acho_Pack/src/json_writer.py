import json
import os
import random
from datetime import datetime

class Acho_JSONWriter:
    """
    每次运行后都修改并保存JSON文档的节点
    支持直接覆盖或合并模式
    带有seed控制，可以选择固定写入或每次随机写入
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_content": ("STRING", {
                    "default": '{"example": "value"}',
                    "multiline": True,
                }),
                "file_path": ("STRING", {
                    "default": "data.json",
                    "multiline": False,
                }),
                "write_mode": (["overwrite", "merge"], {
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
                    "default": True,
                }),
                "create_dir": ("BOOLEAN", {
                    "default": True,
                }),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING", "INT")
    RETURN_NAMES = ("status", "file_path", "debug_info", "seed")
    FUNCTION = "write_json"
    CATEGORY = "Acho Tools/JSON"
    
    @classmethod
    def IS_CHANGED(s, json_content, file_path, write_mode, random_seed, seed, auto_backup=True, create_dir=True):
        # 如果开启随机seed，每次都返回随机数强制重新执行
        if random_seed:
            return float("nan")
        # 如果是固定seed，返回seed值、文件路径和内容的组合
        return (seed, file_path, json_content)
    
    def write_json(self, json_content, file_path, write_mode, random_seed, seed, auto_backup=True, create_dir=True):
        """
        写入JSON内容到文件
        
        Args:
            json_content: 要写入的JSON内容（字符串形式）
            file_path: JSON文件路径（相对或绝对路径）
            write_mode: 写入模式 - "overwrite"(覆盖) 或 "merge"(合并)
            random_seed: 是否使用随机seed（True=每次都重新写入，False=使用固定seed）
            seed: 固定seed值（仅在random_seed=False时使用）
            auto_backup: 是否自动备份原文件
            create_dir: 如果目录不存在是否自动创建
            
        Returns:
            (status, file_path, debug_info, seed): 状态信息、实际文件路径、调试信息和实际使用的seed
        """
        debug_info = []
        
        # 如果是随机模式，生成新的seed
        if random_seed:
            actual_seed = random.randint(0, 0xffffffffffffffff)
            debug_info.append(f"随机模式 - 生成seed: {actual_seed}")
            print(f"[Acho_JSONWriter] 随机模式 - 生成seed: {actual_seed}")
        else:
            actual_seed = seed
            debug_info.append(f"固定模式 - 使用seed: {actual_seed}")
            print(f"[Acho_JSONWriter] 固定模式 - 使用seed: {actual_seed}")
        
        try:
            # 获取当前工作目录
            current_dir = os.getcwd()
            debug_info.append(f"当前工作目录: {current_dir}")
            print(f"[Acho_JSONWriter] 当前工作目录: {current_dir}")
            print(f"[Acho_JSONWriter] 输入文件路径: {file_path}")
            print(f"[Acho_JSONWriter] 写入模式: {write_mode}")
            
            # 处理相对路径
            if not os.path.isabs(file_path):
                abs_path = os.path.abspath(file_path)
                debug_info.append(f"相对路径转绝对路径: {abs_path}")
            else:
                abs_path = file_path
                debug_info.append(f"使用绝对路径: {abs_path}")
            
            print(f"[Acho_JSONWriter] 完整路径: {abs_path}")
            
            # 获取目录路径
            dir_path = os.path.dirname(abs_path)
            debug_info.append(f"目标目录: {dir_path}")
            
            # 创建目录（如果需要）
            if dir_path and not os.path.exists(dir_path):
                if create_dir:
                    os.makedirs(dir_path, exist_ok=True)
                    debug_info.append(f"创建目录: {dir_path}")
                    print(f"[Acho_JSONWriter] 创建目录: {dir_path}")
                else:
                    error_msg = f"目录不存在且未启用自动创建: {dir_path}"
                    debug_info.append(error_msg)
                    debug_str = "\n".join(debug_info)
                    return (f"ERROR: {error_msg}", abs_path, debug_str, actual_seed)
            
            # 解析输入的JSON内容
            # 先打印原始输入以便调试
            print(f"[Acho_JSONWriter] JSON内容长度: {len(json_content)} 字符")
            print(f"[Acho_JSONWriter] JSON内容类型: {type(json_content)}")
            print(f"[Acho_JSONWriter] JSON内容前100字符: {repr(json_content[:100])}")
            
            debug_info.append(f"原始内容长度: {len(json_content)} 字符")
            debug_info.append(f"原始内容类型: {type(json_content).__name__}")
            debug_info.append(f"原始内容前80字符: {repr(json_content[:80])}")
            
            # 清理输入内容（去除首尾空白字符）
            cleaned_content = json_content.strip()
            
            try:
                new_data = json.loads(cleaned_content)
                debug_info.append(f"✅ JSON内容解析成功")
                print(f"[Acho_JSONWriter] ✅ JSON解析成功")
            except json.JSONDecodeError as e:
                error_msg = f"JSON格式错误: {e}"
                debug_info.append(f"❌ {error_msg}")
                print(f"[Acho_JSONWriter] ❌ {error_msg}")
                print(f"[Acho_JSONWriter] 错误位置: 第{e.lineno}行 第{e.colno}列 (位置{e.pos})")
                
                # 显示错误附近的内容
                error_context_start = max(0, e.pos - 30)
                error_context_end = min(len(cleaned_content), e.pos + 30)
                error_context = cleaned_content[error_context_start:error_context_end]
                print(f"[Acho_JSONWriter] 错误附近内容: {repr(error_context)}")
                
                # 提供详细的错误提示
                error_detail = f"""❌ JSON格式错误

错误信息: {e}
错误位置: 第{e.lineno}行 第{e.colno}列
错误附近: {repr(error_context)}

原始内容前200字符:
{repr(cleaned_content[:200])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
常见问题检查：
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ❌ 使用了单引号 ' 而不是双引号 "
   错误: {{'name': 'value'}}
   正确: {{"name": "value"}}

2. ❌ 键名没有加引号
   错误: {{name: "value"}}
   正确: {{"name": "value"}}

3. ❌ 有尾随逗号
   错误: {{"name": "value",}}
   正确: {{"name": "value"}}

4. ❌ 字符串内部的引号没有转义
   错误: {{"text": "He said "hello""}}
   正确: {{"text": "He said \\"hello\\""}}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
建议使用 Acho JSON Formatter 节点来自动修复！
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
                debug_info.append(error_detail)
                debug_str = "\n".join(debug_info)
                return (error_detail, abs_path, debug_str, actual_seed)
            
            # 准备最终要写入的数据
            final_data = new_data
            
            # 如果是合并模式且文件已存在
            if write_mode == "merge" and os.path.exists(abs_path):
                try:
                    with open(abs_path, 'r', encoding='utf-8') as f:
                        existing_data = json.load(f)
                    
                    debug_info.append(f"读取现有文件成功")
                    
                    # 如果都是字典，进行合并
                    if isinstance(existing_data, dict) and isinstance(new_data, dict):
                        existing_data.update(new_data)
                        final_data = existing_data
                        debug_info.append(f"合并模式：已合并现有数据")
                        print(f"[Acho_JSONWriter] 合并模式：已合并现有数据")
                    else:
                        # 如果不是字典，直接覆盖
                        debug_info.append(f"合并模式：数据类型不是字典，使用覆盖模式")
                        print(f"[Acho_JSONWriter] 合并模式：数据类型不是字典，使用覆盖模式")
                        
                except json.JSONDecodeError:
                    debug_info.append(f"现有文件JSON格式错误，将被覆盖")
                    print(f"[Acho_JSONWriter] 现有文件JSON格式错误，将被覆盖")
                except Exception as e:
                    debug_info.append(f"读取现有文件时出错: {e}，将被覆盖")
                    print(f"[Acho_JSONWriter] 读取现有文件时出错: {e}，将被覆盖")
            
            # 备份原文件（如果存在且需要备份）
            if auto_backup and os.path.exists(abs_path):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = f"{abs_path}.backup_{timestamp}"
                try:
                    with open(abs_path, 'r', encoding='utf-8') as f_src:
                        with open(backup_path, 'w', encoding='utf-8') as f_dst:
                            f_dst.write(f_src.read())
                    debug_info.append(f"已备份到: {backup_path}")
                    print(f"[Acho_JSONWriter] 已备份到: {backup_path}")
                except Exception as e:
                    debug_info.append(f"备份失败: {e}")
                    print(f"[Acho_JSONWriter] 备份失败: {e}")
            
            # 写入JSON文件（格式化输出，便于阅读）
            final_content = json.dumps(final_data, ensure_ascii=False, indent=2)
            with open(abs_path, 'w', encoding='utf-8') as f:
                f.write(final_content)
            
            debug_info.append(f"成功写入文件，大小: {len(final_content)} 字符")
            status_msg = f"✅ SUCCESS: 已保存到 {abs_path} (模式: {write_mode})"
            print(f"[Acho_JSONWriter] {status_msg}")
            
            debug_str = "\n".join(debug_info)
            return (status_msg, abs_path, debug_str, actual_seed)
            
        except Exception as e:
            error_msg = f"写入文件时出错: {e}"
            debug_info.append(error_msg)
            print(f"[Acho_JSONWriter] {error_msg}")
            
            # 添加异常的完整堆栈信息
            import traceback
            stack_trace = traceback.format_exc()
            debug_info.append(f"错误堆栈:\n{stack_trace}")
            print(f"[Acho_JSONWriter] 错误堆栈:\n{stack_trace}")
            
            debug_str = "\n".join(debug_info)
            return (f"ERROR: {error_msg}", file_path, debug_str, actual_seed)
