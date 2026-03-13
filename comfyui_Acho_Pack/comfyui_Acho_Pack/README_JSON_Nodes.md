# Acho JSON 节点使用说明

## 节点概述

这两个节点用于在 ComfyUI 工作流中读取和写入 JSON 文档，并带有智能的seed控制机制来管理缓存行为。

---

## 📖 Acho JSON Reader（JSON读取节点）

### 功能
每次运行都可以重新读取JSON文档，支持固定模式和随机模式。

### 输入参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `file_path` | STRING | "data.json" | JSON文件路径（相对或绝对路径） |
| `random_seed` | BOOLEAN | True | 是否使用随机seed |
| `seed` | INT | 0 | 固定seed值（当random_seed=False时使用） |
| `default_content` | STRING | "{}" | 文件不存在时的默认内容（可选） |

### 输出

| 输出 | 类型 | 说明 |
|------|------|------|
| `json_string` | STRING | 读取的JSON内容（字符串形式） |
| `file_path` | STRING | 实际使用的完整文件路径 |
| `debug_info` | STRING | 详细的调试信息和状态 |
| `seed` | INT | 实际使用的seed值 |

### Seed 控制机制

#### 🎲 随机模式（random_seed = True）
- ✅ **每次运行都重新读取文件**
- ✅ 自动生成新的随机seed
- ✅ 忽略ComfyUI的缓存机制
- 📌 **适用场景**：需要实时监控文件变化，或文件内容经常更新

#### 🔒 固定模式（random_seed = False）
- ✅ **只有当seed值或文件路径改变时才重新读取**
- ✅ 利用ComfyUI的缓存机制提升性能
- ✅ 手动控制seed来决定何时重新读取
- 📌 **适用场景**：文件内容稳定，不需要频繁重新读取

### 使用示例

```
示例1：实时监控JSON文件
[Acho JSON Reader]
  file_path: "config.json"
  random_seed: True (开启)
  ↓
  每次运行工作流都会重新读取最新的config.json

示例2：固定配置读取
[Acho JSON Reader]
  file_path: "settings.json"
  random_seed: False (关闭)
  seed: 42
  ↓
  只有改变seed值或文件路径时才会重新读取
```

---

## ✍️ Acho JSON Writer（JSON写入节点）

### 功能
每次运行后都可以修改并保存JSON文档，支持覆盖和合并两种模式。

### 输入参数

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `json_content` | STRING | "{}" | 要写入的JSON内容 |
| `file_path` | STRING | "data.json" | JSON文件路径（相对或绝对路径） |
| `write_mode` | ENUM | "overwrite" | 写入模式：overwrite（覆盖）或 merge（合并） |
| `random_seed` | BOOLEAN | True | 是否使用随机seed |
| `seed` | INT | 0 | 固定seed值（当random_seed=False时使用） |
| `auto_backup` | BOOLEAN | True | 是否自动备份原文件（可选） |
| `create_dir` | BOOLEAN | True | 是否自动创建不存在的目录（可选） |

### 输出

| 输出 | 类型 | 说明 |
|------|------|------|
| `status` | STRING | 操作状态信息（SUCCESS或ERROR） |
| `file_path` | STRING | 实际使用的完整文件路径 |
| `debug_info` | STRING | 详细的调试信息和状态 |
| `seed` | INT | 实际使用的seed值 |

### 写入模式

#### 📝 覆盖模式（overwrite）
- 完全替换文件内容
- 适用于全新的数据写入

#### 🔄 合并模式（merge）
- 将新数据与现有数据合并（仅限字典类型）
- 新键值对会添加，同名键会被更新
- 如果不是字典类型，自动降级为覆盖模式

### Seed 控制机制

#### 🎲 随机模式（random_seed = True）
- ✅ **每次运行都重新写入文件**
- ✅ 自动生成新的随机seed
- ✅ 忽略ComfyUI的缓存机制
- 📌 **适用场景**：需要实时保存数据，或数据频繁变化

#### 🔒 固定模式（random_seed = False）
- ✅ **只有当seed值、文件路径或内容改变时才重新写入**
- ✅ 利用ComfyUI的缓存机制避免重复写入
- ✅ 手动控制seed来决定何时写入
- 📌 **适用场景**：批量处理时避免重复写入相同内容

### 自动备份
当 `auto_backup=True` 且文件已存在时，会自动创建备份文件：
```
原文件：data.json
备份文件：data.json.backup_20260313_142233
```

### 使用示例

```
示例1：实时保存生成结果
[生成节点] → [Acho JSON Writer]
  json_content: {"result": "...", "timestamp": "..."}
  file_path: "output/results.json"
  write_mode: overwrite
  random_seed: True
  ↓
  每次运行都会保存新的结果

示例2：增量更新配置
[配置生成] → [Acho JSON Writer]
  json_content: {"new_setting": "value"}
  file_path: "config.json"
  write_mode: merge
  random_seed: False
  seed: 1
  ↓
  只有改变seed时才会写入，且会合并现有配置
```

---

## 🔗 组合使用示例

### 场景1：读取-处理-保存工作流
```
[Acho JSON Reader] → [处理节点] → [Acho JSON Writer]
  读取配置          处理数据        保存结果
  random_seed: True               random_seed: True
```

### 场景2：增量更新配置文件
```
[Acho JSON Reader] → [修改节点] → [Acho JSON Writer]
  file_path: "config.json"        file_path: "config.json"
  random_seed: False              write_mode: merge
  seed: 1                         random_seed: False
                                  seed: 1
```

---

## 🐛 调试技巧

1. **查看 debug_info 输出**：包含详细的执行信息
   - 当前工作目录
   - 完整文件路径
   - Seed模式和值
   - 操作状态

2. **查看 ComfyUI 控制台**：所有操作都有日志输出
   ```
   [Acho_JSONReader] 随机模式 - 生成seed: 12345678
   [Acho_JSONReader] 当前工作目录: /path/to/comfyui
   [Acho_JSONReader] 完整路径: /path/to/comfyui/data.json
   [Acho_JSONReader] 成功读取并解析: /path/to/comfyui/data.json
   ```

3. **路径问题排查**：
   - 相对路径基于ComfyUI的工作目录
   - 使用绝对路径可以避免路径问题
   - debug_info 会显示最终的完整路径

---

## 💡 性能优化建议

- 📌 **频繁更新的文件**：使用 `random_seed=True` 确保实时性
- 📌 **稳定的配置文件**：使用 `random_seed=False` 利用缓存提升性能
- 📌 **批量处理**：使用固定seed避免重复写入
- 📌 **开发调试**：使用随机seed确保每次都执行

---

## 🎯 常见问题

### Q: 为什么需要seed控制？
A: ComfyUI默认会缓存节点结果。如果输入不变，就不会重新执行。seed机制让你可以灵活控制何时重新执行。

### Q: random_seed应该选True还是False？
A: 
- **True**：需要实时性，每次都重新执行
- **False**：追求性能，只在必要时重新执行

### Q: merge模式什么时候有用？
A: 当你想保留原文件的部分内容，只更新特定字段时使用merge模式。

### Q: 备份文件太多怎么办？
A: 设置 `auto_backup=False` 关闭自动备份，或定期清理 .backup_ 文件。

---

## 📁 文件路径说明

### 相对路径（推荐用于项目内文件）
```
"data.json"                    → ComfyUI根目录/data.json
"configs/settings.json"        → ComfyUI根目录/configs/settings.json
"../shared/common.json"        → ComfyUI上级目录/shared/common.json
```

### 绝对路径（推荐用于跨项目文件）
```
"/Users/acho/Documents/data.json"                      (macOS)
"C:/Users/acho/Documents/data.json"                    (Windows)
```

---

## 版本历史

- **v1.1** (2026-03-13)
  - ✅ 新增seed控制机制
  - ✅ 支持随机/固定两种模式
  - ✅ 优化缓存性能
  - ✅ 新增seed输出

- **v1.0** (2026-03-13)
  - ✅ 初始版本
  - ✅ 基础读写功能
  - ✅ 调试信息输出
