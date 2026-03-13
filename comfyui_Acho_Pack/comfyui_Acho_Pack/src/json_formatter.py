import json
import re

class Acho_JSONFormatter:
    """
    JSON格式化和验证节点
    帮助修复常见的JSON格式问题
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {
                    "default": "{}",
                    "multiline": True,
                }),
                "auto_fix": ("BOOLEAN", {
                    "default": True,
                }),
            },
        }
    
    RETURN_TYPES = ("STRING", "STRING", "STRING")
    RETURN_NAMES = ("formatted_json", "validation_status", "error_info")
    FUNCTION = "format_json"
    CATEGORY = "Acho Tools/JSON"
    
    def format_json(self, input_text, auto_fix=True):
        """
        格式化和验证JSON
        
        Args:
            input_text: 输入的文本（可能是格式不正确的JSON）
            auto_fix: 是否尝试自动修复常见问题
            
        Returns:
            (formatted_json, validation_status, error_info): 格式化后的JSON、验证状态、错误信息
        """
        error_info = []
        
        try:
            # 首先尝试直接解析
            data = json.loads(input_text)
            formatted = json.dumps(data, ensure_ascii=False, indent=2)
            
            print(f"[Acho_JSONFormatter] ✅ JSON格式正确")
            return (formatted, "✅ 格式正确", "无错误")
            
        except json.JSONDecodeError as e:
            error_info.append(f"JSON解析错误: {e}")
            print(f"[Acho_JSONFormatter] ❌ JSON格式错误: {e}")
            
            if not auto_fix:
                error_msg = f"JSON格式错误: {e}\n请使用双引号包裹键和字符串值"
                return (input_text, "❌ 格式错误", error_msg)
            
            # 尝试自动修复
            fixed_text = input_text
            fixes_applied = []
            
            # 修复1: 将单引号替换为双引号（注意避免影响字符串内部的单引号）
            if "'" in fixed_text:
                # 简单替换（可能不完美，但能处理大多数情况）
                fixed_text = fixed_text.replace("'", '"')
                fixes_applied.append("单引号 → 双引号")
            
            # 修复2: 尝试修复没有引号的键名 (简化版本，只处理简单情况)
            # 例如: {key: "value"} -> {"key": "value"}
            pattern = r'\{(\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*):'
            if re.search(pattern, fixed_text):
                fixed_text = re.sub(pattern, r'{\\1"\\2"\\3:', fixed_text)
                fixes_applied.append("添加键名引号")
            
            # 修复3: 移除尾随逗号
            fixed_text = re.sub(r',(\s*[}\]])', r'\1', fixed_text)
            if ',' in input_text and ',' not in fixed_text:
                fixes_applied.append("移除尾随逗号")
            
            # 再次尝试解析修复后的内容
            try:
                data = json.loads(fixed_text)
                formatted = json.dumps(data, ensure_ascii=False, indent=2)
                
                fix_msg = "、".join(fixes_applied) if fixes_applied else "未知修复"
                success_msg = f"✅ 自动修复成功\n应用的修复: {fix_msg}"
                
                print(f"[Acho_JSONFormatter] ✅ 自动修复成功: {fix_msg}")
                return (formatted, "✅ 已修复", success_msg)
                
            except json.JSONDecodeError as e2:
                error_info.append(f"修复后仍有错误: {e2}")
                
                # 提供详细的错误提示
                error_msg = f"""❌ JSON格式错误，无法自动修复

原始错误: {e}

常见问题检查：
1. 键和字符串值必须用双引号 " 而不是单引号 '
   ❌ {{'name': 'value'}}
   ✅ {{"name": "value"}}

2. 键名必须加引号
   ❌ {{name: "value"}}
   ✅ {{"name": "value"}}

3. 不能有尾随逗号
   ❌ {{"key": "value",}}
   ✅ {{"key": "value"}}

4. 字符串内部的引号需要转义
   ❌ {{"text": "He said "hello""}}
   ✅ {{"text": "He said \\"hello\\""}}

请检查输入内容并修正格式。
"""
                print(f"[Acho_JSONFormatter] ❌ 无法自动修复")
                return (input_text, "❌ 无法修复", error_msg)
        
        except Exception as e:
            error_msg = f"处理时出错: {e}"
            print(f"[Acho_JSONFormatter] ❌ {error_msg}")
            return (input_text, "❌ 处理错误", error_msg)
