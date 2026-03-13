# JSON 格式问题排查指南

## 🚨 如果你看到 "JSON格式错误" 的提示

这个错误通常是因为输入的内容**不符合标准JSON格式**。

---

## ✅ 正确的JSON格式规则

### 规则1: 必须使用双引号 `"`，不能用单引号 `'`

❌ **错误示例**：
```javascript
{'name': 'test'}
```

✅ **正确示例**：
```json
{"name": "test"}
```

### 规则2: 键名必须加双引号

❌ **错误示例**：
```javascript
{name: "test"}
```

✅ **正确示例**：
```json
{"name": "test"}
```

### 规则3: 不能有尾随逗号

❌ **错误示例**：
```json
{
  "name": "test",
  "value": 123,
}
```

✅ **正确示例**：
```json
{
  "name": "test",
  "value": 123
}
```

### 规则4: 字符串内部的引号需要转义

❌ **错误示例**：
```json
{"text": "He said "hello""}
```

✅ **正确示例**：
```json
{"text": "He said \"hello\""}
```

---

## 📝 在 ComfyUI 中正确输入 JSON

### 方法1: 简单的单行JSON（推荐用于简单数据）

在 `json_content` 输入框中输入：

```json
{"name": "测试", "value": 123}
```

⚠️ **注意**：
- 整个内容用**双引号**
- 键和值都用**双引号**
- 不要有多余的逗号

### 方法2: 多行格式化JSON（推荐用于复杂数据）

```json
{
  "title": "测试文档",
  "author": "Acho",
  "tags": ["tag1", "tag2", "tag3"],
  "data": {
    "key1": "value1",
    "key2": 123,
    "key3": true
  }
}
```

### 方法3: 使用 JSON Formatter 节点（最推荐）

```
[文本输入] → [Acho JSON Formatter] → [Acho JSON Writer]
              (自动检查和修复)         (写入文件)
```

---

## 🧪 测试你的JSON格式

### 在命令行中测试

```bash
cd /Users/acho/Documents/comfyui/custom_nodes/comfyui_Acho_Pack
python3 test_json_format.py
```

这个脚本可以帮你：
1. 测试JSON字符串是否有效
2. 显示详细的错误信息
3. 交互式测试你的输入

### 在线JSON验证工具

- https://jsonlint.com/
- https://jsonformatter.org/

---

## 🔍 常见错误案例分析

### 案例1: 使用了单引号

**你输入的：**
```javascript
{'name': 'test', 'value': 123}
```

**错误信息：**
```
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

**修正方法：**
把所有单引号 `'` 改成双引号 `"`
```json
{"name": "test", "value": 123}
```

### 案例2: 键名没有引号

**你输入的：**
```javascript
{name: "test", value: 123}
```

**错误信息：**
```
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
```

**修正方法：**
给所有键名加上双引号
```json
{"name": "test", "value": 123}
```

### 案例3: 有尾随逗号

**你输入的：**
```json
{
  "name": "test",
  "value": 123,
}
```

**错误信息：**
```
Expecting property name enclosed in double quotes: line 4 column 1 (char 35)
```

**修正方法：**
删除最后一个逗号
```json
{
  "name": "test",
  "value": 123
}
```

### 案例4: 中文路径或中文内容

**你输入的：**
```json
{"文件": "测试.json", "内容": "这是中文内容"}
```

✅ **这个是正确的！** JSON完全支持中文。

如果仍然出错，可能是编码问题。确保：
- ComfyUI使用UTF-8编码
- 文件保存为UTF-8格式

---

## 🛠️ 排查步骤

如果你按照正确格式输入还是报错，请按以下步骤排查：

### 1. 检查ComfyUI控制台日志

查找这些关键信息：
```
[Acho_JSONWriter] JSON内容类型: <class 'str'>
[Acho_JSONWriter] JSON内容前100字符: ...
[Acho_JSONWriter] 错误位置: 第X行 第Y列
```

### 2. 查看 debug_info 输出

连接 `debug_info` 输出到显示节点，查看：
- 原始内容长度
- 原始内容前80字符
- 具体的错误位置

### 3. 使用 JSON Formatter 节点

```
[输入] → [Acho JSON Formatter] → [查看结果]
         auto_fix: True
```

Formatter节点会自动尝试修复并告诉你问题在哪里。

### 4. 运行测试脚本

```bash
python3 test_json_format.py
```

在交互式模式中粘贴你的JSON内容，查看详细错误。

---

## 💡 快速解决方案

### 方案A: 使用正确的格式模板

**复制这个模板**，然后修改值：

```json
{"key1": "value1", "key2": "value2", "key3": 123}
```

或多行格式：

```json
{
  "key1": "value1",
  "key2": "value2",
  "key3": 123,
  "list": [1, 2, 3],
  "nested": {
    "subkey": "subvalue"
  }
}
```

### 方案B: 使用 JSON Formatter 工作流

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│ 文本输入节点 │────▶│ JSON Formatter   │────▶│  JSON Writer    │
│ (任意格式)   │     │ (自动修复)       │     │  (写入文件)     │
└─────────────┘     └──────────────────┘     └─────────────────┘
```

### 方案C: 先在线验证，再粘贴

1. 访问 https://jsonlint.com/
2. 粘贴你的JSON内容
3. 点击 "Validate JSON"
4. 如果有错误，会提示你具体位置
5. 修正后再粘贴到 ComfyUI

---

## 📞 还是不行？

如果你按照以上所有步骤操作还是出错，请提供以下信息：

1. **你输入的完整JSON内容**（用代码块包裹）
2. **完整的错误信息**（从 debug_info 或控制台）
3. **ComfyUI 控制台的日志**（特别是 `[Acho_JSONWriter]` 开头的行）

示例：
```
我输入的JSON:
{"name": "test"}

错误信息:
Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

控制台日志:
[Acho_JSONWriter] JSON内容前100字符: '{"name": "test"}'
```

---

## 📚 JSON格式学习资源

- **JSON官方网站**: https://www.json.org/json-zh.html
- **MDN JSON教程**: https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Objects/JSON
- **JSON在线编辑器**: https://jsoneditoronline.org/

---

## ✨ 最后的建议

1. 🎯 **最简单的方法**: 使用 JSON Formatter 节点，让它自动处理格式问题
2. 📋 **复制模板**: 从上面的正确示例复制，然后修改值
3. 🧪 **先测试**: 使用 test_json_format.py 脚本或在线工具验证
4. 📖 **学习规则**: 记住4条核心规则（双引号、键加引号、无尾随逗号、转义引号）

祝你使用愉快！🎉
