import os
import shutil
import json
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader, Template

class FileUtils:
    """文件操作工具类"""
    
    @staticmethod
    def create_slide_structure(output_dir: str, slide_count: int):
        """创建幻灯片文件夹结构"""
        output_path = Path(output_dir)
        
        # 创建主目录
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 创建pages目录
        pages_dir = output_path / "pages"
        pages_dir.mkdir(exist_ok=True)
        
        # 为每一页创建子目录
        for i in range(1, slide_count + 1):
            slide_dir = pages_dir / f"{i:02d}"
            slide_dir.mkdir(exist_ok=True)
        
        print(f"已创建幻灯片结构: {output_dir}")
        return str(output_path)
    
    @staticmethod
    def copy_common_assets(template_dir: str, output_dir: str):
        """复制公共资源文件"""
        template_path = Path(template_dir)
        output_path = Path(output_dir)
        
        # 复制common.css到pages目录
        common_css_src = template_path / "common.css"
        common_css_dst = output_path / "pages" / "common.css"
        
        if common_css_src.exists():
            shutil.copy2(common_css_src, common_css_dst)
            print(f"已复制公共样式文件到: {common_css_dst}")
        else:
            print(f"警告: 未找到公共样式文件 {common_css_src}")
    
    @staticmethod
    def render_template(template_content: str, context: Dict[str, Any]) -> str:
        """使用Jinja2渲染模板"""
        template = Template(template_content)
        return template.render(**context)
    
    @staticmethod
    def render_template_file(template_path: str, context: Dict[str, Any], output_path: str):
        """渲染模板文件并保存"""
        # 读取模板文件
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # 渲染模板
        rendered_content = FileUtils.render_template(template_content, context)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存渲染结果
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(rendered_content)
        
        print(f"已生成文件: {output_path}")
    
    @staticmethod
    def generate_slides_json(slides_data: List[Dict[str, Any]], output_dir: str):
        """生成slides.json配置文件"""
        slides_list = []
        
        for slide in slides_data:
            slide_path = f"{slide['id']}/index.html"
            slides_list.append(slide_path)
        
        slides_json_path = Path(output_dir) / "slides.json"
        
        with open(slides_json_path, 'w', encoding='utf-8') as f:
            json.dump(slides_list, f, ensure_ascii=False, indent=2)
        
        print(f"已生成slides配置文件: {slides_json_path}")
        return slides_list
    
    @staticmethod
    def clean_output_dir(output_dir: str):
        """清理输出目录"""
        output_path = Path(output_dir)
        
        if output_path.exists():
            shutil.rmtree(output_path)
            print(f"已清理输出目录: {output_dir}")
    
    @staticmethod
    def validate_slide_files(output_dir: str) -> bool:
        """验证生成的文件是否完整"""
        output_path = Path(output_dir)
        
        # 检查主要文件是否存在
        required_files = [
            output_path / "index.html",
            output_path / "slides.json",
            output_path / "pages" / "common.css"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
        
        if missing_files:
            print(f"缺失文件: {missing_files}")
            return False
        
        print("文件验证通过")
        return True
    
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """加载JSON文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @staticmethod
    def save_json(data: Dict[str, Any], file_path: str):
        """保存JSON文件"""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试代码
    test_output_dir = "./test_output"
    
    # 创建测试结构
    FileUtils.create_slide_structure(test_output_dir, 5)
    
    # 生成测试的slides.json
    test_slides = [
        {"id": "01", "title": "标题页"},
        {"id": "02", "title": "内容页1"},
        {"id": "03", "title": "内容页2"}
    ]
    FileUtils.generate_slides_json(test_slides, test_output_dir)
    
    # 验证文件
    # FileUtils.validate_slide_files(test_output_dir)
