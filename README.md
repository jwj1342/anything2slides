# anything2slides

智能幻灯片生成系统 - 将任意文本自动转换为精美的网页幻灯片

## 功能特点

- 🧠 **智能规划**: 使用AI分析文本结构，自动规划幻灯片内容和布局
- 🎨 **多种布局**: 支持标题页、文字页、列表页、双栏对比、网格卡片等多种布局
- 🌐 **网页展示**: 生成现代化的HTML5幻灯片，支持键盘导航和进度显示  
- ⚡ **快速生成**: 一键从文本生成完整的演示文稿
- 🔧 **易于定制**: 基于模板系统，便于扩展和修改样式

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制 `.env.example` 为 `.env` 并填入你的OpenAI API密钥：

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥
```

### 3. 运行示例

```bash
# 创建示例输入文件
python main.py

# 生成幻灯片
python main.py -i sample_input.txt

# 指定输出目录
python main.py -i "你的文本内容" -o ./my_slides
```

### 4. 查看结果

生成完成后，在浏览器中打开 `output/index.html` 查看幻灯片。

## 使用方法

### 基本用法

```bash
# 从文本文件生成
python main.py -i input.txt -o output_dir

# 直接输入文本
python main.py -i "这是我的文本内容..."

# 仅生成规划（不生成HTML）
python main.py -i input.txt --plan-only

# 从已有规划生成幻灯片
python main.py --from-plan output/plan.json
```

### 配置选项

在 `config.yaml` 中可以调整：

- LLM模型和参数
- 幻灯片最大页数和每页字数
- 支持的布局类型
- 输出样式主题

## 项目结构

```
anything2slides/
├── main.py                 # 主程序入口
├── config.yaml            # 配置文件
├── requirements.txt       # Python依赖
├── src/
│   ├── agents/
│   │   ├── planner.py     # 规划智能体
│   │   └── generator.py   # 生成智能体
│   ├── templates/         # HTML模板
│   │   ├── base_slide.html
│   │   ├── title_layout.html
│   │   ├── text_heavy_layout.html
│   │   └── ...
│   └── utils/
│       └── file_utils.py  # 文件操作工具
├── demo/                  # 示例幻灯片
└── output/               # 生成的幻灯片输出
```

## 支持的布局类型

- **title**: 标题页 - 用于演示开场
- **text_heavy**: 文字密集型 - 适合详细说明
- **bullet_list**: 要点列表 - 适合要点总结
- **two_column**: 双栏对比 - 适合对比分析
- **grid_cards**: 网格卡片 - 适合多要点展示
- **timeline**: 时间线 - 适合历史发展
- **conclusion**: 总结页 - 用于演示结尾

## 开发计划

- [x] 基础的planner和generator实现
- [ ] 支持PDF/Word等文档解析
- [ ] 支持公式和表格渲染
- [ ] 实现reviewer和editor的多轮优化循环
- [ ] 支持更多主题和样式
- [ ] 添加图片和媒体支持

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License