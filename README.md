# ComfyUI Acho Pack

ComfyUI 自定义节点包，提供实用的工具节点，包括文件读写、数据处理和流程控制等功能。

## 📦 安装

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/Acho001/comfyui_Acho_Pack.git
```

重启 ComfyUI 即可使用。

---

## 🎯 节点列表

### 🔀 流程控制

#### **Acho Switch (0-5)**
多输入选择器，支持三种模式：
- **First Active**: 输出第一个有效输入
- **Random**: 随机选择一个输入
- **Sequential**: 按顺序循环输出

**分类**: `Acho Tools`

---

### 💻 代码执行

#### **Acho Simple Code**
在工作流中执行自定义 Python 代码。

**特性**:
- 支持多个输入/输出（最多20个）
- 内置 `torch`, `math`, `random` 模块
- 通过 `inputs[]` 和 `outputs[]` 访问数据

**示例**:
```python
# 简单计算
outputs[0] = inputs[0] * 2

# 使用torch
outputs[0] = torch.tensor([1, 2, 3])

# 数学运算
outputs[0] = math.sqrt(inputs[0])
```

**分类**: `Acho Tools`

---

### 📝 文本处理

#### **Acho Batch Text Assembler**
批量组装文本，支持列表输出。

**特性**:
- 最多6个文本输入
- 通过 `batch_size` 控制输出数量
- 自动过滤未连接的输入
- 输出为列表形式，触发批处理

**分类**: `Acho Tools`

---

### 📄 文本文件操作

#### **Acho Text Reader**
通用文本文件读取节点，支持任意文本格式。

**特性**:
- 支持所有文本文件（txt, json, md, csv, xml, yaml等）
- 无格式限制和验证
- Seed控制（随机/固定模式）
- 自动处理相对/绝对路径

**输入**:
- `file_path`: 文件路径
- `random_seed`: 是否每次都重新读取（True/False）
- `seed`: 固定seed值
- `default_content`: 文件不存在时的默认内容

**输出**:
- `content`: 文件内容
- `file_path`: 完整文件路径
- `seed`: 实际使用的seed

**分类**: `Acho Tools/File IO`

---

#### **Acho Text Writer**
通用文本文件写入节点，支持任意文本格式。

**特性**:
- 支持所有文本文件
- **覆盖模式** (overwrite): 替换文件内容
- **追加模式** (append): 在文件末尾添加内容
- Seed控制
- 可选自动备份
- 自动创建目录

**输入**:
- `content`: 要写入的内容
- `file_path`: 文件路径
- `write_mode`: 写入模式（overwrite/append）
- `random_seed`: 是否每次都重新写入
- `seed`: 固定seed值
- `auto_backup`: 是否自动备份（带时间戳）
- `create_dir`: 是否自动创建目录

**输出**:
- `status`: 操作状态（SUCCESS/ERROR）
- `file_path`: 完整文件路径
- `seed`: 实际使用的seed

**分类**: `Acho Tools/File IO`

---

### 📊 JSON 文件操作

#### **Acho JSON Reader**
JSON文档读取节点，带格式验证。

**特性**:
- 读取并验证JSON格式
- Seed控制
- 详细的调试信息
- 格式错误时返回默认内容

**输入**:
- `file_path`: JSON文件路径
- `random_seed`: 是否每次都重新读取
- `seed`: 固定seed值
- `default_content`: 默认JSON内容

**输出**:
- `json_string`: JSON内容（字符串）
- `file_path`: 完整文件路径
- `debug_info`: 调试信息
- `seed`: 实际使用的seed

**分类**: `Acho Tools/JSON`

---

#### **Acho JSON Writer**
JSON文档写入节点，支持格式验证和合并。

**特性**:
- 验证JSON格式
- **覆盖模式** (overwrite): 替换整个文件
- **合并模式** (merge): 合并JSON对象
- Seed控制
- 可选自动备份
- 详细的错误提示

**输入**:
- `json_content`: JSON内容（必须是有效JSON）
- `file_path`: 文件路径
- `write_mode`: 写入模式（overwrite/merge）
- `random_seed`: 是否每次都重新写入
- `seed`: 固定seed值
- `auto_backup`: 是否自动备份
- `create_dir`: 是否自动创建目录

**输出**:
- `status`: 操作状态
- `file_path`: 完整文件路径
- `debug_info`: 调试信息
- `seed`: 实际使用的seed

**分类**: `Acho Tools/JSON`

---

#### **Acho JSON Formatter**
JSON格式验证和自动修复节点。

**特性**:
- 验证JSON格式
- 自动修复常见问题：
  - 单引号 → 双引号
  - 添加缺失的键名引号
  - 移除尾随逗号
- 格式化输出（美化）
- 详细的错误提示

**输入**:
- `input_text`: 待验证的JSON文本
- `auto_fix`: 是否自动修复

**输出**:
- `formatted_json`: 格式化后的JSON
- `validation_status`: 验证状态（✅正确 / ❌错误 / ✅已修复）
- `error_info`: 错误信息或修复说明

**分类**: `Acho Tools/JSON`

---

## 🌟 核心特性

### 🎲 Seed 控制机制

所有文件读写节点都支持 Seed 控制：

- **随机模式** (`random_seed=True`):
  - 每次运行都重新执行
  - 忽略 ComfyUI 缓存
  - 适用于需要实时更新的场景

- **固定模式** (`random_seed=False`):
  - 利用 ComfyUI 缓存机制
  - 只有 seed、路径或内容改变时才重新执行
  - 适用于稳定数据，提升性能

### 📁 路径处理

- 支持**相对路径**（基于 ComfyUI 工作目录）
- 支持**绝对路径**
- 自动路径转换和验证

### 🔍 调试功能

- 详细的日志输出
- 完整的错误信息
- 文件路径验证
- 内容预览

---

## 💡 使用示例

### 示例1: 文本文件读写工作流
```
[Text Reader] → [处理节点] → [Text Writer]
读取文本文件      修改内容        保存回文件
```

### 示例2: JSON配置管理
```
[JSON Reader] → [解析配置] → [生成内容] → [JSON Writer (merge)]
读取配置          使用配置        生成结果        更新配置
```

### 示例3: 日志追加记录
```
[工作流步骤] → [Text Writer]
                file_path: "workflow.log"
                write_mode: append
                content: "[时间] 步骤完成\n"
```

### 示例4: 批量文本处理
```
[文本生成1]
[文本生成2]  →  [Batch Text Assembler]  →  [批处理节点]
[文本生成3]      batch_size: 3              处理每个文本
```

### 示例5: 多路输入选择
```
[输入A]
[输入B]  →  [Acho Switch]  →  [输出]
[输入C]      mode: Random       随机选择一个输入
```

---

## 📚 文档

- **[README_Text_Nodes.md](README_Text_Nodes.md)** - 文本读写节点详细说明
- **[README_JSON_Nodes.md](README_JSON_Nodes.md)** - JSON读写节点详细说明  
- **[JSON_FORMAT_GUIDE.md](JSON_FORMAT_GUIDE.md)** - JSON格式问题排查指南
- **[README_CustomIO.md](README_CustomIO.md)** - 自定义输入输出说明

---

## 🛠️ 工具脚本

### test_json_format.py
JSON格式验证脚本，可以在命令行中测试JSON格式：

```bash
cd ComfyUI/custom_nodes/comfyui_Acho_Pack
python3 test_json_format.py
```

---

## 🎨 节点分类

所有节点都在 ComfyUI 节点菜单中按分类组织：

- `Acho Tools` - 基础工具（Switch, Simple Code, Batch Text Assembler）
- `Acho Tools/File IO` - 文件操作（Text Reader, Text Writer）
- `Acho Tools/JSON` - JSON操作（JSON Reader, Writer, Formatter）

---

## 🔄 更新日志

### v1.1.0 (2026-03-13)
- ✅ 新增 Text Reader/Writer - 通用文本读写节点
- ✅ 新增 JSON Reader/Writer/Formatter - JSON专用节点
- ✅ 新增 Seed 控制机制
- ✅ 新增自动备份功能
- ✅ 新增追加模式（Text Writer）
- ✅ 新增合并模式（JSON Writer）
- ✅ 改进调试信息输出

### v1.0.0
- ✅ Acho Switch - 多输入选择器
- ✅ Acho Simple Code - Python代码执行
- ✅ Acho Batch Text Assembler - 批量文本组装

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 License

MIT License

---

## 🙏 致谢

感谢 ComfyUI 社区的支持和贡献！

---

**作者**: Acho  
**仓库**: https://github.com/Acho001/comfyui_Acho_Pack  
**版本**: 1.1.0

这份说明书专为 **Acho Simple Code** 节点设计，包含中英文对照，适合放在项目的 Readme 或作为速查表使用。

---

# 📘 Acho Simple Code - User Manual / 使用说明书

**Acho Simple Code** is a powerful yet easy-to-use node that allows you to write Python logic directly in ComfyUI. No need to create new nodes for simple tasks!
**Acho Simple Code** 是一个强大且易用的节点，允许你在 ComfyUI 中直接编写 Python 逻辑。处理简单任务时，无需再专门编写新节点！

---

## 1. Core Syntax / 核心语法

### 📥 Inputs / 获取输入
Access input data using the `inputs` list (index 0 to 5).
使用 `inputs` 列表来获取数据（索引 0 到 5）。

*   **`inputs[0]`**: The value of input0 / 获取 input0 的值
*   **`inputs[1]`**: The value of input1 / 获取 input1 的值
*   ...

### 📤 Outputs / 设置输出
Assign results using the `outputs` dictionary (index 0 to 5).
使用 `outputs` 字典来赋值输出结果（索引 0 到 5）。

*   **`outputs[0] = ...`**: Set value for output_0 / 设置 output_0 的输出值
*   **`outputs[1] = ...`**: Set value for output_1 / 设置 output_1 的输出值

---

## 2. Built-in Environment / 内置环境
The following libraries are pre-loaded. You **DO NOT** need to `import` them.
以下库已预先加载，你**不需要**手动 `import` 它们。

*   **`torch`**: For image/tensor operations / 用于图像和张量操作
*   **`math`**: For mathematical functions / 用于数学运算 (sin, cos, etc.)
*   **`random`**: For random numbers / 用于生成随机数
*   **Standard Types**: `int`, `float`, `str`, `len`, `print`, `range`

---

## 3. Examples / 常用代码示例

### ✅ Basic: Pass Through / 基础：直通
Simple pass-through logic.
简单的直通逻辑。
```python
# Pass input0 directly to output0
# 将 input0 直接传给 output0
outputs[0] = inputs[0]
```

### 🧮 Math: Calculation / 数学：计算
Calculate resolution or numbers.
计算分辨率或数值。
```python
# Double the number from input0
# 将 input0 的数值乘以 2
outputs[0] = inputs[0] * 2

# Calculate 16:9 height based on width (input0)
# 根据宽度 (input0) 计算 16:9 的高度
outputs[1] = int(inputs[0] * 9 / 16)
```

### 📝 Text: Prompt Combination / 文本：提示词拼接
Combine two prompts with a comma.
用逗号拼接两段提示词。
```python
# Combine input0 and input1
# 拼接 input0 和 input1
outputs[0] = f"{inputs[0]}, {inputs[1]}"
```

### 🔀 Logic: Switch / 逻辑：开关
Switch output based on a boolean/int input.
根据布尔值或整数输入切换输出。
```python
# If input0 is True (or 1), output image A (input1)
# Otherwise, output image B (input2)
# 如果 input0 为真，输出图A，否则输出图B
if inputs[0]:
    outputs[0] = inputs[1]
else:
    outputs[0] = inputs[2]
```

### 🎨 Image: Invert Color / 图像：反色
Invert image colors using PyTorch.
使用 PyTorch 进行图片反色。
```python
# Invert colors (1.0 - original)
# 颜色反转 (1.0 - 原图)
outputs[0] = 1.0 - inputs[0]
```

---

## 4. Smart Features / 智能特性

*   **Auto Default Values / 自动默认值**:
    If an input is not connected, it defaults to a safe value (0 for numbers, "" for strings, black image for images). No errors!
    如果输入端口未连接，会自动使用安全默认值（数字为0，字符串为空，图像为全黑），不会报错！

*   **Error Reporting / 错误提示**:
    If your code has a bug, the node will turn red and show the error message in the console/UI.
    如果代码有 Bug，节点会变红，并在控制台/界面显示具体错误信息。
