#!/usr/bin/env python3
"""
测试 planner 和 generator 的基本功能
"""

import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.append(str(Path(__file__).parent))

def test_planner():
    """测试规划代理"""
    print("🧪 测试 Planner Agent...")
    
    try:
        from src.agents.planner import PlannerAgent
        
        planner = PlannerAgent()
        
        test_text = """
        深度学习是机器学习的一个分支，它模仿人脑的神经网络结构。

        深度学习的核心是人工神经网络，特别是深层神经网络。这些网络由多个层次组成，每一层都能学习数据的不同特征。

        深度学习在许多领域都有应用，包括：
        - 计算机视觉：图像识别、物体检测
        - 自然语言处理：机器翻译、文本生成  
        - 语音识别：语音转文字、语音合成
        - 推荐系统：个性化推荐

        深度学习的优势在于它能够自动学习特征，不需要人工设计特征工程。但同时也需要大量的数据和计算资源。

        未来，深度学习将继续发展，向着更加智能和高效的方向前进。
        """
        
        plan = planner.plan_slides(test_text)
        
        print(f"✅ 规划成功，共 {len(plan['slides'])} 页")
        print(f"📋 标题: {plan['title']}")
        
        for i, slide in enumerate(plan['slides'][:3]):  # 只显示前3页
            print(f"  第{slide['id']}页: {slide['title']} ({slide['layout']})")
        
        return plan
        
    except Exception as e:
        print(f"❌ Planner 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_generator(plan_data):
    """测试生成代理"""
    print("\n🧪 测试 Generator Agent...")
    
    if not plan_data:
        print("❌ 没有规划数据，跳过生成测试")
        return
    
    try:
        from src.agents.generator import GeneratorAgent
        
        generator = GeneratorAgent()
        output_dir = "./test_output"
        
        result = generator.generate_slides(plan_data, output_dir)
        
        print(f"✅ 生成成功，输出目录: {result}")
        
        # 检查生成的文件
        output_path = Path(output_dir)
        if (output_path / "index.html").exists():
            print(f"✅ 主页面生成成功")
        if (output_path / "slides.json").exists():
            print(f"✅ 配置文件生成成功") 
        if (output_path / "pages").exists():
            print(f"✅ 页面目录生成成功")
            
        print(f"🌐 请在浏览器中打开: file://{output_path.absolute()}/index.html")
        
    except Exception as e:
        print(f"❌ Generator 测试失败: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("🚀 开始测试 anything2slides 组件...")
    
    # 测试规划代理
    plan_data = test_planner()
    
    # 测试生成代理  
    test_generator(plan_data)
    
    print("\n🎉 测试完成！")

if __name__ == "__main__":
    main()
