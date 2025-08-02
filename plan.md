# anything2slides 项目规划文档

## 项目目标
输入任意文档（如 PDF、Word、纯文本等），自动生成结构化、可交互的网页幻灯片，支持内容与布局的多轮智能优化。

---

## 总体流程

1. **解析阶段**
   - **parser agent**：负责解析原始文档（如 PDF），提取文本、图片、表格、公式等结构化信息。

2. **规划阶段**
   - **planner agent**：根据解析结果，规划每一页幻灯片的主题、内容要点、顺序等。

3. **生成阶段**
   - **generator agent**：根据 planner 的规划，生成每一页的前端代码（HTML/CSS），实现内容与图文布局，结构参考 demo 文件夹示例。

4. **多轮优化阶段（Loop）**
   - **reviewer agent**：对生成的幻灯片进行审阅，提出内容或布局的修改建议。
   - **edit agent**：根据 reviewer 的建议，定位问题并进行局部修改。
   - **循环**：reviewer 确认问题解决后，继续提出下一个建议，循环往复，直到幻灯片大体完善。

---

## 近期开发计划

### 1. 先实现 planner 和 generator
- 输入：一段文本（无需 parser，手动提供即可）。
- planner 负责将文本拆分为多页幻灯片的规划。
- generator 负责将每页规划转为 demo 风格的 HTML 页面。
- 产出：一套网页幻灯片初版。

### 2. 后续补充 parser agent 及 generator 工具
- 实现 parser agent，支持 PDF/Word/Markdown 等格式的解析。
- 针对公式、表格等内容，探索 HTML 的原生支持与第三方工具（如 MathJax、KaTeX、markdown-it、table 组件等）的集成方案。
- 使 generator 能自动渲染公式、表格等复杂内容。

### 3. 实现 reviewer agent 与 edit agent 的多轮 loop
- reviewer agent 自动审阅幻灯片，提出内容/布局等修改建议。
- edit agent 能根据建议定位并局部修改 HTML/CSS。
- 支持人工参与，人工建议与 reviewer agent 逻辑一致。
- 形成“建议-修改-确认-再建议”的多轮优化闭环。

---

## 关键技术点与注意事项

- 幻灯片页面结构参考 demo 文件夹，采用独立 HTML 文件+统一样式。
- 页面顺序可用 JSON 文件维护，便于插入/删除/重排页面。
- 公式渲染可用 MathJax/KaTeX，表格可用 HTML 原生或第三方库。
- 后续可用 Node.js 脚本或后端 API 实现自动化页面生成与修改。
- edit agent 需支持精确定位并局部修改页面内容。

---

## 未来展望

- 支持多种文档格式的自动解析。
- 支持多种幻灯片主题与布局模板。
- 支持协作式多智能体优化与人工交互。
- 支持一键导出/分享/演示。

---

如有补充和建议，欢迎随时讨论！
