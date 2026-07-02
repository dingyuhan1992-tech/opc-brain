from ai.engine import engine


class ImageOptimizer:
    def suggest_optimization(self, product_name: str, category: str, platform: str) -> dict:
        prompt = f"""产品名称：{product_name}
产品品类：{category}
目标平台：{platform}

请给出产品主图和详情页图片的优化建议：
1. 主图风格建议
2. 色彩搭配建议
3. 构图建议
4. 详情页图片结构
5. 参考风格描述

输出 JSON 格式。"""
        return engine.chat_json("你是一位电商视觉设计师，擅长宠物产品摄影与设计。", prompt)

    def generate_alt_text(self, image_description: str) -> str:
        prompt = f"""请为以下产品图片生成 SEO 友好的 alt 文本（用于搜索引擎优化）：
图片描述：{image_description}"""
        return engine.chat("你是一位电商SEO专家。", prompt, temperature=0.3)
