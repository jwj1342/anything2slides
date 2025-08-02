#!/usr/bin/env python3
"""
anything2slides - 智能幻灯片生成系统
主程序入口
"""

import argparse
import os
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.append(str(Path(__file__).parent))

from src.agents.planner import PlannerAgent
from src.agents.generator import GeneratorAgent

def main():
    parser = argparse.ArgumentParser(description='anything2slides - 智能幻灯片生成系统')
    parser.add_argument('--input', '-i', required=True, help='输入文本内容（文件路径或直接文本）')
    parser.add_argument('--output', '-o', default='./output', help='输出目录路径')
    parser.add_argument('--config', '-c', default='config.yaml', help='配置文件路径')
    parser.add_argument('--plan-only', action='store_true', help='仅生成规划，不生成HTML')
    parser.add_argument('--from-plan', help='从已有规划文件生成HTML')
    
    args = parser.parse_args()
    
    try:
        if args.from_plan:
            # 从规划文件生成幻灯片
            print(f"📖 从规划文件生成幻灯片: {args.from_plan}")
            generator = GeneratorAgent(args.config)
            
            import json
            with open(args.from_plan, 'r', encoding='utf-8') as f:
                plan_data = json.load(f)
            
            output_dir = generator.generate_slides(plan_data, args.output)
            print(f"🎉 幻灯片生成完成！请打开: {output_dir}/index.html")
            
        else:
            # 完整流程：规划 + 生成
            
            # 1. 读取输入内容
            input_text = read_input(args.input)
            print(f"📝 输入内容长度: {len(input_text)} 字符")
            
            # 2. 生成规划
            print("🧠 开始规划幻灯片结构...")
            planner = PlannerAgent(args.config)
            plan_data = planner.plan_slides(input_text)
            
            print(f"📋 规划完成，共 {len(plan_data['slides'])} 页")
            print(f"📋 演示标题: {plan_data['title']}")
            
            # 保存规划文件
            plan_output_path = Path(args.output) / "plan.json"
            planner.save_plan(plan_data, str(plan_output_path))
            
            if args.plan_only:
                print(f"✅ 规划已保存到: {plan_output_path}")
                return
            
            # 3. 生成幻灯片
            print("🎨 开始生成幻灯片...")
            generator = GeneratorAgent(args.config)
            output_dir = generator.generate_slides(plan_data, args.output)
            
            print(f"🎉 幻灯片生成完成！")
            print(f"📂 输出目录: {output_dir}")
            print(f"🌐 请打开浏览器访问: file://{Path(output_dir).absolute()}/index.html")
    
    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def read_input(input_arg: str) -> str:
    """读取输入内容"""
    
    # 判断是文件路径还是直接文本
    if os.path.isfile(input_arg):
        # 从文件读取
        print(f"📖 从文件读取输入: {input_arg}")
        with open(input_arg, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        # 直接使用输入文本
        print("📝 使用直接输入的文本")
        return input_arg

def create_sample_input():
    """创建示例输入文件"""
    sample_text = """
人工智能的发展历程

人工智能（AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。

## 发展阶段

### 1. 符号主义时期（1950s-1980s）
这一时期主要依靠逻辑推理和符号处理。专家系统是这个时期的代表，通过编码专家知识来解决特定领域的问题。

### 2. 连接主义兴起（1980s-1990s）
神经网络重新受到关注，反向传播算法的发明使得多层神经网络的训练成为可能。

### 3. 统计学习时代（1990s-2010s）
支持向量机、决策树、随机森林等统计学习方法变得流行。这一时期注重数据驱动的方法。

### 4. 深度学习革命（2010s-至今）
深度学习的突破引发了AI的第三次浪潮，在图像识别、自然语言处理、语音识别等领域取得了突破性进展。

## 未来展望

我们现在正在迈向AGI（通用人工智能）时代。大语言模型如GPT系列展现出了前所未有的语言理解和生成能力，为实现真正的人工智能铺平了道路。

人工智能将继续改变我们的生活方式，从自动驾驶汽车到智能助手，AI正在成为现代生活不可或缺的一部分。
    """
    
    with open('sample_input.txt', 'w', encoding='utf-8') as f:
        f.write(sample_text.strip())
    
    print("📄 已创建示例输入文件: sample_input.txt")

if __name__ == "__main__":
    # 如果没有参数，显示帮助和创建示例
    if len(sys.argv) == 1:
        print("🎯 anything2slides - 智能幻灯片生成系统")
        print("\n使用示例:")
        print("  python main.py -i 'AI技术发展很快，包括机器学习、深度学习等领域。'")
        print("  python main.py -i sample_input.txt -o ./my_slides")
        print("  python main.py --from-plan ./output/plan.json")
        print("\n创建示例输入文件:")
        create_sample_input()
        print("\n现在你可以运行:")
        print("  python main.py -i sample_input.txt")
    else:
        main()
