# ComfyUI 自定义输入输出代码节点

这个插件提供了支持自定义输入输出的动态代码节点，让你可以灵活地创建符合特定需求的代码处理节点。

## 节点类型

### 1. Acho_SimpleCode_CustomIO
基础的自定义输入输出节点，通过数字输入框控制输入输出数量。

**特点：**
- 使用 `input_count` 和 `output_count` 参数控制输入输出数量
- 支持 0-20 个输入输出
- 代码中使用 `inputs[0]` 访问输入，`outputs[0] = ...` 赋值输出

### 2. Acho_SimpleCode_Advanced  
高级版本，包含添加按钮但功能相对简单。

### 3. Acho_SimpleCode_Dynamic ⭐ **推荐使用**
最完整的动态节点，包含完整的按钮控制功能。

**特点：**
- 🟢 `➕ 添加输入` - 增加一个输入端口
- 🔴 `➖ 删除输入` - 减少一个输入端口  
- 🟢 `➕ 添加输出` - 增加一个输出端口
- 🔴 `➖ 删除输出` - 减少一个输出端口
- `current_inputs` - 显示当前输入数量
- `current_outputs` - 显示当前输出数量

## 使用方法

### 基本用法
```python
# 标准写法
outputs[0] = inputs[0]

# 运算示例
outputs[1] = inputs[1] * 2

# 复杂运算
outputs[0] = inputs[0] + inputs[1]
outputs[1] = inputs[2] if len(inputs) > 2 else 0
```

### 代码环境
节点提供了以下内置变量和函数：
- `inputs` - 输入列表，`inputs[0]` 对应第一个输入
- `outputs` - 输出字典，`outputs[0] = ...` 赋值给第一个输出
- `torch` - PyTorch 库
- `math` - 数学库
- `random` - 随机数库
- `print`, `len`, `range`, `int`, `float`, `str` - 基础Python函数

### 示例代码

#### 示例1：简单的数据传递
```python
# 将第一个输入传递给第一个输出
outputs[0] = inputs[0]
```

#### 示例2：数学运算
```python
# 将输入乘以2
if len(inputs) > 0:
    outputs[0] = inputs[0] * 2
```

#### 示例3：条件判断
```python
# 根据输入数量决定输出
if len(inputs) > 1:
    outputs[0] = inputs[0] + inputs[1]
else:
    outputs[0] = inputs[0] if len(inputs) > 0 else 0
```

#### 示例4：使用PyTorch
```python
# 张量运算
if isinstance(inputs[0], torch.Tensor):
    outputs[0] = torch.mean(inputs[0])
    outputs[1] = torch.std(inputs[0])
```

## 安装方法

1. 将 `.py` 文件复制到 ComfyUI 的 `custom_nodes` 目录
2. 重启 ComfyUI
3. 在节点菜单中找到 "Acho Tools" 分类
4. 选择需要的节点类型

## 注意事项

1. **输入输出索引**：`inputs` 是列表，从 0 开始；`outputs` 是字典，赋值时使用 `outputs[0] = ...`
2. **类型检查**：建议在代码中添加类型检查，避免运行时错误
3. **错误处理**：如果代码执行出错，节点会显示详细的错误信息
4. **默认值**：当输入为空时，系统会自动提供合适的默认值（0、空字符串、空列表等）

## 故障排除

### 常见错误
1. **"inputs[0] 未定义"** - 检查是否正确使用了 `inputs` 列表
2. **"outputs[0] 赋值错误"** - 检查是否正确使用了 `outputs` 字典进行赋值
3. **类型错误** - 在运算前添加类型检查

### 调试技巧
- 使用 `print()` 函数输出调试信息
- 先用简单的代码测试，再逐步复杂化
- 检查输入数据的类型和形状