import os
import json
from pathlib import Path
from typing import Dict, Any, List
import yaml
from src.utils.file_utils import FileUtils

class GeneratorAgent:
    """幻灯片生成智能体"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.template_dir = Path(self.config['generator']['template_dir'])
        self.file_utils = FileUtils()
        
        # 布局模板映射
        self.layout_templates = {
            'title': 'title_layout.html',
            'text_heavy': 'text_heavy_layout.html', 
            'bullet_list': 'bullet_list_layout.html',
            'two_column': 'two_column_layout.html',
            'grid_cards': 'grid_cards_layout.html',
            'timeline': 'text_heavy_layout.html',  # 暂时用text_heavy
            'conclusion': 'text_heavy_layout.html'  # 暂时用text_heavy
        }
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def generate_slides(self, plan_data: Dict[str, Any], output_dir: str):
        """根据规划数据生成完整的幻灯片"""
        
        print(f"开始生成幻灯片到目录: {output_dir}")
        
        # 1. 清理并创建输出目录结构
        if Path(output_dir).exists():
            self.file_utils.clean_output_dir(output_dir)
        
        slide_count = len(plan_data['slides'])
        self.file_utils.create_slide_structure(output_dir, slide_count)
        
        # 2. 复制公共资源
        self.file_utils.copy_common_assets(str(self.template_dir), output_dir)
        
        # 3. 生成每一页幻灯片
        for slide in plan_data['slides']:
            self._generate_single_slide(slide, output_dir)
        
        # 4. 生成主导航页面
        self._generate_main_page(plan_data, output_dir)
        
        # 5. 生成slides.json配置
        self.file_utils.generate_slides_json(plan_data['slides'], output_dir)
        
        # 6. 验证生成结果
        if self.file_utils.validate_slide_files(output_dir):
            print(f"✅ 幻灯片生成完成！输出目录: {output_dir}")
        else:
            print("❌ 幻灯片生成可能存在问题，请检查输出文件")
        
        return output_dir
    
    def _generate_single_slide(self, slide_data: Dict[str, Any], output_dir: str):
        """生成单页幻灯片"""
        
        slide_id = slide_data['id']
        layout = slide_data.get('layout', 'text_heavy')
        
        print(f"生成第{slide_id}页 - 布局: {layout}")
        
        # 准备幻灯片数据
        processed_slide = self._process_slide_data(slide_data)
        
        # 选择布局模板
        layout_template = self.layout_templates.get(layout, 'text_heavy_layout.html')
        layout_path = self.template_dir / layout_template
        
        # 读取布局模板
        with open(layout_path, 'r', encoding='utf-8') as f:
            layout_content = f.read()
        
        # 渲染布局内容
        rendered_content = self.file_utils.render_template(layout_content, {
            'slide': processed_slide
        })
        
        # 准备完整页面数据
        page_data = {
            'slide': {
                'title': slide_data['title'],
                'custom_css': self._extract_css_from_content(rendered_content),
                'body_class': self._get_body_class(layout),
                'content': self._extract_html_from_content(rendered_content)
            },
            'logo': self.config['styles']['logo']
        }
        
        # 读取基础模板
        base_template_path = self.template_dir / 'base_slide.html'
        with open(base_template_path, 'r', encoding='utf-8') as f:
            base_template = f.read()
        
        # 渲染完整页面
        final_html = self.file_utils.render_template(base_template, page_data)
        
        # 保存页面文件
        output_path = Path(output_dir) / "pages" / slide_id / "index.html"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        
        print(f"  ✅ 已生成: {output_path}")
    
    def _process_slide_data(self, slide_data: Dict[str, Any]) -> Dict[str, Any]:
        """处理幻灯片数据，适配不同布局"""
        
        processed = slide_data.copy()
        layout = slide_data.get('layout', 'text_heavy')
        
        if layout == 'title':
            # 标题页处理
            if 'subtitle' not in processed:
                processed['subtitle'] = '智能生成演示文稿'
            if 'tagline' not in processed:
                processed['tagline'] = '基于AI技术的自动化幻灯片生成'
                
        elif layout == 'bullet_list':
            # 要点列表处理
            content = slide_data.get('content', '')
            if isinstance(content, str):
                # 将文本转换为列表项
                lines = [line.strip() for line in content.split('\n') if line.strip()]
                # 简单的列表识别：以-、•、数字.开头的行
                items = []
                for line in lines:
                    if line.startswith(('-', '•', '*')) or any(line.startswith(f'{i}.') for i in range(1, 10)):
                        items.append(line.lstrip('-•*123456789. '))
                    elif len(line) < 100:  # 短句可能是要点
                        items.append(line)
                
                if not items:  # 如果没找到明显的列表，按句子分割
                    items = [s.strip() for s in content.split('。') if s.strip()]
                
                processed['items'] = items[:6]  # 最多6个要点
        
        elif layout == 'two_column':
            # 双栏布局处理
            content = slide_data.get('content', '')
            if isinstance(content, str):
                # 简单分割内容
                parts = content.split('\n\n')
                mid = len(parts) // 2
                
                processed['left_title'] = '方面一'
                processed['left_content'] = '\n\n'.join(parts[:mid])
                processed['right_title'] = '方面二' 
                processed['right_content'] = '\n\n'.join(parts[mid:])
        
        elif layout == 'grid_cards':
            # 网格卡片处理
            content = slide_data.get('content', '')
            if isinstance(content, str):
                # 将内容分割为卡片
                parts = [p.strip() for p in content.split('\n\n') if p.strip()]
                cards = []
                icons = ['🎯', '🔄', '💡', '⚡', '🚀', '🎨']  # 默认图标
                
                for i, part in enumerate(parts[:6]):  # 最多6个卡片
                    lines = part.split('\n')
                    title = lines[0] if lines else f'要点 {i+1}'
                    content_text = '\n'.join(lines[1:]) if len(lines) > 1 else part
                    
                    cards.append({
                        'icon': icons[i % len(icons)],
                        'title': title,
                        'content': content_text
                    })
                
                processed['cards'] = cards
        
        return processed
    
    def _extract_css_from_content(self, content: str) -> str:
        """从渲染内容中提取CSS"""
        if '<style>' in content and '</style>' in content:
            start = content.find('<style>') + 7
            end = content.find('</style>')
            return content[start:end].strip()
        return ''
    
    def _extract_html_from_content(self, content: str) -> str:
        """从渲染内容中提取HTML"""
        if '<style>' in content:
            # 移除style标签
            start = content.find('<style>')
            end = content.find('</style>') + 8
            return content[:start] + content[end:]
        return content
    
    def _get_body_class(self, layout: str) -> str:
        """根据布局类型获取body class"""
        if layout == 'title':
            return 'title-slide'
        return ''
    
    def _generate_main_page(self, plan_data: Dict[str, Any], output_dir: str):
        """生成主导航页面"""
        
        print("生成主导航页面...")
        
        # 准备slides列表
        slides_list = []
        for slide in plan_data['slides']:
            slides_list.append(f"{slide['id']}/index.html")
        
        # 主页面HTML模板（基于demo的结构）
        main_html = self._get_main_page_template()
        
        # 渲染主页面
        rendered_html = self.file_utils.render_template(main_html, {
            'title': plan_data['title'],
            'slides_json': json.dumps(slides_list),
            'total_slides': len(slides_list)
        })
        
        # 保存主页面
        main_page_path = Path(output_dir) / "index.html"
        with open(main_page_path, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"  ✅ 已生成主页面: {main_page_path}")
    
    def _get_main_page_template(self) -> str:
        """获取主页面HTML模板"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            color: #2d3748;
            overflow: hidden;
        }

        .viewer-container {
            width: 100vw;
            height: 100vh;
            position: relative;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 30px;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .slide-frame {
            width: min(85vw, calc(78vh * 16/9));
            height: min(78vh, calc(85vw * 9/16));
            border: none;
            border-radius: 16px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08), 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
            background: white;
            border: 1px solid rgba(0, 0, 0, 0.05);
        }

        .navigation {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            align-items: center;
            gap: 15px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 12px 24px;
            border-radius: 50px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .nav-btn {
            width: 44px;
            height: 44px;
            border: none;
            border-radius: 50%;
            background: linear-gradient(135deg, #4f46e5, #6366f1);
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
        }

        .nav-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        }

        .nav-btn:disabled {
            background: #cbd5e1;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .slide-counter {
            font-size: 14px;
            font-weight: 500;
            color: #64748b;
            margin: 0 8px;
        }

        .progress-bar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: rgba(255, 255, 255, 0.3);
            z-index: 1000;
        }

        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #4f46e5, #6366f1);
            transition: width 0.5s ease;
            border-radius: 0 3px 3px 0;
        }
    </style>
</head>
<body>
    <div class="progress-bar">
        <div class="progress-fill" id="progressFill"></div>
    </div>

    <div class="viewer-container">
        <iframe class="slide-frame" id="slideFrame" src="pages/01/index.html"></iframe>
    </div>

    <div class="navigation">
        <button class="nav-btn" id="prevBtn" onclick="previousSlide()">←</button>
        <span class="slide-counter">
            <span id="currentSlide">1</span> / <span id="totalSlides">{{ total_slides }}</span>
        </span>
        <button class="nav-btn" id="nextBtn" onclick="nextSlide()">→</button>
    </div>

    <script>
        class SlideViewer {
            constructor() {
                this.slides = {{ slides_json }};
                this.currentSlide = 1;
                this.totalSlides = this.slides.length;
                this.slideFrame = document.getElementById('slideFrame');
                this.currentSlideSpan = document.getElementById('currentSlide');
                this.totalSlidesSpan = document.getElementById('totalSlides');
                this.progressFill = document.getElementById('progressFill');
                this.prevBtn = document.getElementById('prevBtn');
                this.nextBtn = document.getElementById('nextBtn');

                this.init();
            }

            init() {
                this.updateDisplay();
                this.bindEvents();
                this.loadSlide();
            }

            bindEvents() {
                document.addEventListener('keydown', (e) => {
                    switch(e.key) {
                        case 'ArrowLeft':
                        case 'ArrowUp':
                            this.previousSlide();
                            break;
                        case 'ArrowRight':
                        case 'ArrowDown':
                        case ' ':
                            this.nextSlide();
                            break;
                        case 'Home':
                            this.goToSlide(1);
                            break;
                        case 'End':
                            this.goToSlide(this.totalSlides);
                            break;
                    }
                });
            }

            loadSlide() {
                const slidePath = `pages/${this.slides[this.currentSlide - 1]}`;
                this.slideFrame.src = slidePath;
                this.updateDisplay();
            }

            updateDisplay() {
                this.currentSlideSpan.textContent = this.currentSlide;
                this.totalSlidesSpan.textContent = this.totalSlides;
                
                const progress = (this.currentSlide / this.totalSlides) * 100;
                this.progressFill.style.width = progress + '%';
                
                this.prevBtn.disabled = this.currentSlide === 1;
                this.nextBtn.disabled = this.currentSlide === this.totalSlides;
            }

            nextSlide() {
                if (this.currentSlide < this.totalSlides) {
                    this.currentSlide++;
                    this.loadSlide();
                }
            }

            previousSlide() {
                if (this.currentSlide > 1) {
                    this.currentSlide--;
                    this.loadSlide();
                }
            }

            goToSlide(slideNumber) {
                if (slideNumber >= 1 && slideNumber <= this.totalSlides) {
                    this.currentSlide = slideNumber;
                    this.loadSlide();
                }
            }
        }

        // 全局函数供按钮调用
        let viewer;
        function nextSlide() { viewer.nextSlide(); }
        function previousSlide() { viewer.previousSlide(); }

        // 页面加载完成后初始化
        window.addEventListener('load', () => {
            viewer = new SlideViewer();
        });
    </script>
</body>
</html>'''

if __name__ == "__main__":
    # 测试代码
    generator = GeneratorAgent()
    
    # 测试数据
    test_plan = {
        "title": "人工智能发展历程",
        "slides": [
            {
                "id": "01",
                "type": "title",
                "title": "人工智能发展历程",
                "subtitle": "从符号主义到大语言模型",
                "content": "",
                "layout": "title"
            },
            {
                "id": "02",
                "type": "content",
                "title": "AI发展的四个阶段",
                "content": "人工智能的发展可以分为四个重要阶段。\n\n首先是符号主义时期，专家系统是这个时期的代表。\n\n然后是连接主义的兴起，神经网络开始受到关注。\n\n接着是统计学习方法的发展，支持向量机等算法变得流行。\n\n最近十年，深度学习引发了AI的第三次浪潮。",
                "layout": "text_heavy"
            }
        ]
    }
    
    generator.generate_slides(test_plan, "./test_output")
