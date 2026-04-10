import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载 .env 文件中的隐藏密钥
load_dotenv()

class LLMDispatcher:
    def __init__(self, temperature: float = 0.7, max_tokens: int = 1000, timeout: int = 30):
        """
        初始化LLM调度器
        
        Args:
            temperature: 模型输出的随机性 (0-1)
            max_tokens: 最大生成长度
            timeout: API调用超时时间（秒）
        """
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        
        # 验证必须的环境变量
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        doubao_key = os.getenv("DOUBAO_API_KEY")
        
        if not deepseek_key:
            logger.warning("⚠️ DEEPSEEK_API_KEY 未设置，DeepSeek 模型将不可用")
        if not doubao_key:
            logger.warning("⚠️ DOUBAO_API_KEY 未设置，豆包模型将不可用")
        
        # 1. 初始化低成本模型客户端 (DeepSeek)
        self.cheap_client = OpenAI(
            api_key=deepseek_key or "sk-placeholder",
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            timeout=timeout
        )
        self.cheap_model = "deepseek-chat"

        # 2. 初始化高智商模型客户端 (字节豆包 Doubao)
        self.smart_client = OpenAI(
            api_key=doubao_key or "sk-placeholder",
            base_url=os.getenv("DOUBAO_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
            timeout=timeout
        )
        self.smart_model = os.getenv("DOUBAO_MODEL_EP")
        
        logger.info("✓ LLMDispatcher 初始化完成 (DeepSeek + 豆包)")

    def get_response(self, prompt: str, route_target: str, system_prompt: Optional[str] = None) -> dict:
        """
        根据路由决策，调用对应的大模型
        
        Args:
            prompt: 用户输入提示词
            route_target: 路由决策 ("High-IQ Route" 或 "Low-Cost Route")
            system_prompt: 自定义系统提示词（可选）
            
        Returns:
            dict: 包含状态、模型名称和回答的字典
        """
        # 默认系统提示词
        if system_prompt is None:
            system_prompt = "你是一个有用的 AI 助手。"
        
        # 判断该用哪个客户端和哪个模型
        if route_target == "High-IQ Route":
            client = self.smart_client
            model = self.smart_model
            model_name_display = "Doubao-Pro (High-IQ)"
        else:
            client = self.cheap_client
            model = self.cheap_model
            model_name_display = "DeepSeek (Low-Cost)"

        try:
            logger.info(f"🚀 调用模型: {model_name_display}")
            
            # 统一标准的 API 调用格式 (OpenAI 兼容模式)
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            answer = response.choices[0].message.content
            
            logger.info(f"✓ 模型 {model_name_display} 返回成功")
            return {
                "status": "success",
                "model_used": model_name_display,
                "answer": answer
            }
            
        except FileNotFoundError:
            logger.error(f"✗ API 密钥或基础URL配置不正确")
            return {
                "status": "error",
                "model_used": model_name_display,
                "answer": "❌ API 配置错误：请检查环境变量中的 API 密钥"
            }
        except TimeoutError:
            logger.error(f"✗ API 调用超时 (>{self.timeout}s)")
            return {
                "status": "error",
                "model_used": model_name_display,
                "answer": f"❌ 请求超时：模型响应超过 {self.timeout} 秒"
            }
        except Exception as e:
            error_msg = str(e)
            logger.error(f"✗ API 调用异常: {error_msg}")
            return {
                "status": "error",
                "model_used": model_name_display,
                "answer": f"❌ 调用失败: {error_msg}"
            }

# ================= 测试模块 =================
if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("开始 LLMDispatcher 测试 (DeepSeek + 豆包)")
    logger.info("=" * 80)
    
    # 创建调度器实例（可自定义参数）
    dispatcher = LLMDispatcher(temperature=0.7, max_tokens=1000, timeout=30)
    
    # 测试一下低成本路由 (DeepSeek)
    print("\n--- 测试低成本模型调用 (DeepSeek) ---")
    res1 = dispatcher.get_response("你好，用一句话介绍一下你自己。", "Low-Cost Route")
    print(f"状态: {res1['status']}")
    print(f"使用的模型: {res1['model_used']}")
    print(f"AI 回答: {res1['answer']}\n")

    # 测试一下高智商路由 (豆包)
    print("--- 测试高智商模型调用 (豆包 Doubao) ---")
    res2 = dispatcher.get_response(
        "如果存在外星人，请用三段论逻辑推导他们为什么还没有联系地球。", 
        "High-IQ Route"
    )
    print(f"状态: {res2['status']}")
    print(f"使用的模型: {res2['model_used']}")
    print(f"AI 回答: {res2['answer']}")
    
    logger.info("=" * 80)
    logger.info("LLMDispatcher 测试完成")
    logger.info("=" * 80)