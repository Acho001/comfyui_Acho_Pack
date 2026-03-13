# Acho Text Reader & Writer 节点说明

## 📝 纯文本读写节点

这两个节点用于在 ComfyUI 工作流中读取和写入**任意文本文件**，没有格式限制。

---

## 📖 Acho Text Reader（文本读取节点）

### 功能
读取任意文本文件内容，支持所有文本格式（txt, json, md, csv, xml等）。

### 输入参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `file_path` | STRING | "data.txt" | 文件路径（相对或绝对路径） |
| `random_seed` | BOOLEAN | True | 是否每次都重新读取 |
| `seed` | INT | 0 | 固定seed值（当random_seed=False时） |
| `default_content` | STRING | "" | 文件不存在时的默认内容（可选） |

### 输出

| 输出 | 类型 | 说明 |
|------|------|------|
| `content` | STRING | 读取的文件内容 |
| `file_path` | STRING | 实际使用的完整文件路径 |
| `seed` | INT | 实际使用的seed值 |

### 使用示例

```
[Acho Text Reader]
  file_path: "config.json"
  random_seed: True
  ↓
  读取文件原始内容（不验证格式）
```

---

## ✍️ Acho Text Writer（文本写入节点）

### 功能
写入任意文本内容到文件，支持覆盖和追加两种模式。

### 输入参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `content` | STRING | "" | 要写入的文本内容 |
| `file_path` | STRING | "output.txt" | 文件路径（相对或绝对路径） |
| `write_mode` | ENUM | "overwrite" | 写入模式：overwrite（覆盖）或 append（追加） |
| `random_seed` | BOOLEAN | True | 是否每次都重新写入 |
| `seed` | INT | 0 | 固定seed值（当random_seed=False时） |
| `auto_backup` | BOOLEAN | False | 是否自动备份原文件（可选） |
| `create_dir` | BOOLEAN | True | 是否自动创建不存在的目录（可选） |

### 输出

| 输出 | 类型 | 说明 |
|------|------|------|
| `status` | STRING | 操作状态信息（SUCCESS或ERROR） |
| `file_path` | STRING | 实际使用的完整文件路径 |
| `seed` | INT | 实际使用的seed值 |

### 写入模式

#### 📝 覆盖模式（overwrite）
- 完全替换文件内容
- 适用于全新的数据写入

#### ➕ 追加模式（append）
- 在文件末尾添加新内容
- 适用于日志记录、累积数据

### 使用示例

```
示例1：保存JSON文本
[文本输入] → [Acho Text Writer]
  content: {"name": "test", "value": 123}
  file_path: "output.json"
  write_mode: overwrite
  ↓
  直接写入文本，不验证JSON格式

示例2：追加日志
[日志生成] → [Acho Text Writer]
  content: "2026-03-13: 操作完成\n"
  file_path: "log.txt"
  write_mode: append
  ↓
  在文件末尾添加新行
```

---

## 🎯 与 JSON 节点的区别

| 特性 | Text Reader/Writer | JSON Reader/Writer |
|------|-------------------|-------------------|
| **格式验证** | ❌ 无验证 | ✅ 验证JSON格式 |
| **支持格式** | ✅ 任意文本 | ⚠️ 仅JSON |
| **错误处理** | 直接读写 | 格式错误时报错 |
| **适用场景** | 通用文本文件 | 结构化JSON数据 |
| **追加模式** | ✅ 支持 | ❌ 仅覆盖/合并 |

---

## 💡 使用场景

### 场景1：读取配置文件（任意格式）
```
[Acho Text Reader]
  file_path: "config.yaml"
  ↓
  读取YAML配置（作为纯文本）
```

### 场景2：保存提示词
```
[提示词生成] → [Acho Text Writer]
  content: "a beautiful landscape..."
  file_path: "prompts/scene01.txt"
  ↓
  保存为纯文本文件
```

### 场景3：追加日志记录
```
[工作流步骤] → [Acho Text Writer]
  content: "[2026-03-13 14:30] Step completed\n"
  file_path: "workflow.log"
  write_mode: append
  ↓
  累积日志内容
```

### 场景4：读取-处理-保存
```
[Acho Text Reader] → [处理节点] → [Acho Text Writer]
  读取文本文件        修改内容        保存回文件
```

---

## 🔧 Seed 控制机制

### 🎲 随机模式（random_seed = True）
- ✅ 每次运行都重新执行
- ✅ 适用于需要实时更新的场景

### 🔒 固定模式（random_seed = False）
- ✅ 利用ComfyUI缓存机制
- ✅ 只有seed、路径或内容改变时才执行
- ✅ 适用于稳定数据，提升性能

---

## 📁 支持的文件类型

Text Reader/Writer 支持所有文本文件：

- ✅ `.txt` - 纯文本
- ✅ `.json` - JSON（作为文本读写）
- ✅ `.md` - Markdown
- ✅ `.csv` - CSV数据
- ✅ `.xml` - XML
- ✅ `.yaml` / `.yml` - YAML
- ✅ `.log` - 日志文件
- ✅ `.html` - HTML
- ✅ `.py` / `.js` / `.css` - 代码文件
- ✅ 任何UTF-8编码的文本文件

---

## ⚠️ 注意事项

1. **编码格式**：默认使用 UTF-8 编码
2. **文件大小**：理论上无限制，但超大文件可能影响ComfyUI性能
3. **路径格式**：
   - 相对路径：基于 ComfyUI 工作目录
   - 绝对路径：直接使用指定路径
4. **追加模式**：不会自动添加换行符，需要手动在内容末尾添加 `\n`

---

## 🎨 工作流示例

### 示例1：配置驱动的工作流
```
[Text Reader: config.txt] → [解析配置] → [根据配置生成] → [Text Writer: result.txt]
```

### 示例2：批处理日志
```
[循环处理] → [Text Writer: log.txt]
              write_mode: append
              content: "处理项目X完成\n"
```

### 示例3：提示词库管理
```
[Text Reader: prompts/base.txt] → [组合提示词] → [生成图像] → [Text Writer: used_prompts.txt]
```

---

## 🆚 什么时候用哪个节点？

| 需求 | 推荐节点 |
|------|---------|
| 读写JSON且需要验证格式 | JSON Reader/Writer |
| 读写JSON但只作为文本 | Text Reader/Writer |
| 读写任意文本文件 | Text Reader/Writer |
| 需要追加内容 | Text Writer |
| 需要合并JSON对象 | JSON Writer |

---

## 📚 快速开始

1. **重启 ComfyUI**
2. **在节点菜单中找到**：`Acho Tools/File IO`
3. **添加节点**：
   - Acho Text Reader
   - Acho Text Writer
4. **设置路径和内容**
5. **运行工作流**

就这么简单！🎉
