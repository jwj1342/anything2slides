# anything2slides - 快速开始指南

## 🚀 立即开始

### 第一步：安装依赖
```bash
pip install langchain langchain-openai python-dotenv jinja2 pyyaml
```

### 第二步：配置API密钥
```bash
# 复制配置文件
cp .env.example .env

# 编辑.env文件，填入你的API密钥
# OPENAI_API_KEY=你的密钥
# OPENAI_BASE_URL=https://api.openai.com/v1  # 或你的API地址
```

### 第三步：运行测试
```bash
# 创建示例文件并运行测试
python main.py

# 生成示例幻灯片
python main.py -i sample_input.txt
```

### 第四步：查看结果
在浏览器中打开 `output/index.html` 查看生成的幻灯片！

## 📖 使用示例

```bash
# 1. 从文本直接生成
python main.py -i "深度学习是AI的重要分支，包括CNN、RNN、Transformer等技术。"

# 2. 从文件生成
python main.py -i my_document.txt -o my_slides

# 3. 仅生成规划
python main.py -i input.txt --plan-only

# 4. 从规划生成幻灯片
python main.py --from-plan output/plan.json
```

## 🎯 项目特点

✅ **已实现功能**：
- 智能文本分析和幻灯片规划
- 多种布局模板（标题页、文字页、列表页、双栏、网格卡片）
- 现代化的HTML5幻灯片界面
- 键盘导航和进度显示
- 基于Jinja2的模板系统

🚧 **后续开发**：
- PDF/Word文档解析
- 公式和表格支持
- reviewer和editor智能体
- 更多主题和样式
- 图片和媒体支持

## 🛠️ 架构说明

- **Planner Agent**: 使用LLM分析文本，规划幻灯片结构
- **Generator Agent**: 基于规划生成HTML页面，支持多种布局
- **模板系统**: 灵活的Jinja2模板，易于扩展新布局
- **文件工具**: 统一的文件操作和资源管理

## 📞 问题反馈

如有问题请查看：
1. 检查API密钥配置
2. 确认依赖包安装
3. 查看控制台错误信息
4. 运行 `python test.py` 进行诊断
