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
