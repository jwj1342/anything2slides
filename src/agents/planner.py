import os
import json
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import yaml

# 加载环境变量
load_dotenv()

class PlannerAgent:
    """幻灯片规划智能体"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.llm = self._init_llm()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载配置文件"""
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _init_llm(self) -> ChatOpenAI:
        """初始化LLM"""
        return ChatOpenAI(
            model=self.config['llm']['model'],
            temperature=self.config['llm']['temperature'],
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            openai_api_base=os.getenv('OPENAI_BASE_URL')
        )
    
    def plan_slides(self, input_text: str) -> Dict[str, Any]:
        """根据输入文本规划幻灯片结构"""
        
        system_prompt = self._get_system_prompt()
        human_prompt = self._get_human_prompt(input_text)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            # 解析LLM返回的JSON
            plan_data = json.loads(response.content)
            
            # 验证和修正规划数据
            plan_data = self._validate_and_fix_plan(plan_data)
            
            return plan_data
            
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            print(f"LLM原始回复: {response.content}")
            # 返回默认的规划结构
            return self._get_fallback_plan(input_text)
    
    def _get_system_prompt(self) -> str:
        """获取系统提示词"""
        slide_types = self.config['planner']['slide_types']
        max_slides = self.config['planner']['max_slides']
        words_per_slide = self.config['planner']['words_per_slide']
        
        return f"""你是一个专业的幻灯片规划专家。你的任务是将用户提供的文本内容规划为结构化的幻灯片演示。

## 规划规则：
1. 总页数不超过{max_slides}页
2. 每页内容控制在{words_per_slide}字左右
3. 必须包含标题页和总结页
4. 逻辑清晰，层次分明

## 可用的布局类型：
- title: 标题页（用于开场）
- text_heavy: 文字密集型（适合详细解释）
- bullet_list: 要点列表（适合要点总结）
- two_column: 双栏对比（适合对比分析）
- grid_cards: 网格卡片（适合多个要点展示）
- timeline: 时间线（适合历史发展或流程）
- conclusion: 总结页（用于结尾）

## 输出格式要求：
请返回标准的JSON格式，包含以下结构：
{{
  "title": "整体演示标题",
  "slides": [
    {{
      "id": "01",
      "type": "title",
      "title": "主标题",
      "subtitle": "副标题（可选）",
      "content": "",
      "layout": "title"
    }},
    {{
      "id": "02",
      "type": "content", 
      "title": "页面标题",
      "content": "页面主要内容",
      "layout": "text_heavy"
    }}
  ]
}}

注意：
- 每页都必须有唯一的id（01, 02, 03...）
- title页面的content字段可以为空
- content字段支持HTML标签
- 根据内容特点合理选择layout类型"""

    def _get_human_prompt(self, input_text: str) -> str:
        """获取人类提示词"""
        return f"""请为以下文本内容规划幻灯片演示：

{input_text}

请分析内容结构，提取核心要点，规划合适的页面数量和布局，生成JSON格式的幻灯片规划。"""

    def _validate_and_fix_plan(self, plan_data: Dict[str, Any]) -> Dict[str, Any]:
        """验证和修正规划数据"""
        
        # 确保有title字段
        if 'title' not in plan_data:
            plan_data['title'] = "演示文稿"
        
        # 确保有slides字段
        if 'slides' not in plan_data or not isinstance(plan_data['slides'], list):
            plan_data['slides'] = []
        
        # 验证每一页的结构
        for i, slide in enumerate(plan_data['slides']):
            # 确保有必要的字段
            slide.setdefault('id', f"{i+1:02d}")
            slide.setdefault('type', 'content')
            slide.setdefault('title', f"第{i+1}页")
            slide.setdefault('content', '')
            slide.setdefault('layout', 'text_heavy')
            
            # 验证layout类型
            if slide['layout'] not in self.config['planner']['slide_types']:
                slide['layout'] = 'text_heavy'
        
        # 确保第一页是title页
        if plan_data['slides'] and plan_data['slides'][0]['layout'] != 'title':
            title_slide = {
                'id': '01',
                'type': 'title',
                'title': plan_data['title'],
                'subtitle': '智能生成演示文稿',
                'content': '',
                'layout': 'title'
            }
            plan_data['slides'].insert(0, title_slide)
            
            # 重新编号
            for i, slide in enumerate(plan_data['slides']):
                slide['id'] = f"{i+1:02d}"
        
        return plan_data
    
    def _get_fallback_plan(self, input_text: str) -> Dict[str, Any]:
        """获取后备规划（当LLM解析失败时使用）"""
        
        # 简单的文本分段逻辑
        paragraphs = [p.strip() for p in input_text.split('\n') if p.strip()]
        
        slides = [
            {
                'id': '01',
                'type': 'title',
                'title': '演示文稿',
                'subtitle': '基于文本内容生成',
                'content': '',
                'layout': 'title'
            }
        ]
        
        # 将段落分配到不同页面
        words_per_slide = self.config['planner']['words_per_slide']
        current_content = ""
        slide_num = 2
        
        for paragraph in paragraphs:
            if len(current_content) + len(paragraph) <= words_per_slide:
                current_content += paragraph + "\n\n"
            else:
                if current_content:
                    slides.append({
                        'id': f'{slide_num:02d}',
                        'type': 'content',
                        'title': f'第{slide_num-1}部分',
                        'content': current_content.strip(),
                        'layout': 'text_heavy'
                    })
                    slide_num += 1
                current_content = paragraph + "\n\n"
        
        # 添加最后一页内容
        if current_content:
            slides.append({
                'id': f'{slide_num:02d}',
                'type': 'content', 
                'title': f'第{slide_num-1}部分',
                'content': current_content.strip(),
                'layout': 'text_heavy'
            })
        
        return {
            'title': '演示文稿',
            'slides': slides
        }
    
    def save_plan(self, plan_data: Dict[str, Any], output_path: str):
        """保存规划数据到文件"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, ensure_ascii=False, indent=2)
        print(f"规划数据已保存到: {output_path}")

if __name__ == "__main__":
    # 测试代码
    planner = PlannerAgent()
    
    test_text = """
    人工智能的发展历程可以分为几个重要阶段。首先是符号主义时期，专家系统是这个时期的代表。
    然后是连接主义的兴起，神经网络开始受到关注。接着是统计学习方法的发展，支持向量机等算法变得流行。
    最近十年，深度学习引发了AI的第三次浪潮，在图像识别、自然语言处理等领域取得了突破性进展。
    现在我们正在迈向AGI时代，大语言模型展现出了前所未有的能力。
    """
    
    plan = planner.plan_slides(test_text)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
