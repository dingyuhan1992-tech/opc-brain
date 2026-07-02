from ai.engine import engine


class ContentGenerator:
    def generate_ad_copy(self, product_name: str, platform: str, audience: str) -> str:
        prompt = f"""产品：{product_name}
投放平台：{platform}
目标受众：{audience}

请生成 3 版不同风格的广告文案供 A/B 测试。"""
        return engine.chat("你是一位擅长宠物行业的广告文案专家。", prompt)

    def generate_video_script(self, product_name: str, duration: str = "60秒", style: str = "科普评测") -> dict:
        prompt = f"""产品：{product_name}
视频时长：{duration}
风格：{style}

请生成短视频脚本，包含分镜描述和口播文案。

输出 JSON 格式：
{{
  "title": "视频标题",
  "script": [
    {{"scene": 1, "time": "0:00-0:15", "visual": "画面描述", "audio": "口播文案", "text_overlay": "字幕"}}
  ],
  "hashtags": ["#标签"],
  "music_suggestion": "背景音乐建议"
}}"""
        return engine.chat_json("你是一位短视频编导，擅长宠物类内容创作。", prompt)
