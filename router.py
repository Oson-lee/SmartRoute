import numpy as np
import re

class ComplexityRouter:
    def __init__(self, threshold=0.6):
        self.threshold = threshold
        
        # 权重向量 w [w1: 文本长度权重, w2: 逻辑词汇权重, w3: 特殊符号权重]
        # 这里给了一组初始的“经验值”，你可以随时调整
        self.W = np.array([0.02, 1.5, 2.0])
        
        # 偏置项 b：设为负数，确保日常短句的默认得分极低
        self.b = -2.5 

    def extract_features(self, text: str) -> np.ndarray:
        """
        特征向量构建: 提取文本的三个维度特征
        """
        # v1: 长度归一化 (除以 50 避免数值过大压倒其他特征)
        v1 = len(text) / 50.0

        # v2: 逻辑关联词密度（也需归一化）
        logical_words = ["因为", "所以", "假设", "推导", "证明", "如果", "分析", "总结", "原理", "逻辑", "代码", "算法"]
        v2 = sum(text.count(word) for word in logical_words)
        v2 = v2 / max(1, len(text) // 10)  # 归一化：每10个字符为一个单位

        # v3: 特殊符号密度 (如代码块、数学符号、复杂括号)
        v3 = len(re.findall(r'[`$\[\]{}()=+\-*/]', text)) / 10.0

        return np.array([v1, v2, v3])

    def sigmoid(self, z):
        """Sigmoid 激活函数（含数值稳定性处理）"""
        # 防止溢出：对大负数直接返回0，大正数直接返回1
        if z < -500:
            return 0.0
        elif z > 500:
            return 1.0
        else:
            return 1 / (1 + np.exp(-z))

    def evaluate(self, text: str) -> dict:
        """
        计算得分并返回路由决策
        """
        # 1. 提取向量 v
        v = self.extract_features(text)
        
        # 2. 线性组合 S(x) = w^T * v + b
        score = np.dot(self.W, v) + self.b
        
        # 3. 概率映射 P(hard)
        p_hard = self.sigmoid(score)

        # 4. 路由决策
        is_hard = p_hard >= self.threshold
        route_target = "High-IQ Route" if is_hard else "Low-Cost Route"

        return {
            "text": text,
            "features": v.tolist(),
            "score": round(score, 4),
            "probability": round(p_hard, 4),
            "is_hard": bool(is_hard), # 转换为基础布尔值，方便后续 JSON 序列化
            "route_target": route_target
        }
    

# ================= 测试模块 =================
if __name__ == "__main__":
    router = ComplexityRouter()
    
    # 准备几个不同难度的测试用例
    test_cases = [
        "你好，今天天气怎么样？",
        "帮我写一封请假邮件，说明我今天感冒了，需要休息一天。",
        "假设有一个非空集合 X,证明存在一个单射 f: X -> P(X)，其中 P(X) 是 X 的幂集。同时请推导其逆否命题。",
        "帮我写一个快速排序算法"
    ]
    
    # 运行测试
    print("=" * 80)
    print("复杂度路由测试结果")
    print("=" * 80)
    for i, text in enumerate(test_cases, 1):
        result = router.evaluate(text)
        print(f"\n【测试用例 {i}】")
        print(f"输入: {result['text'][:50]}{'...' if len(result['text']) > 50 else ''}")
        print(f"特征向量: v1={result['features'][0]:.4f}, v2={result['features'][1]:.4f}, v3={result['features'][2]:.4f}")
        print(f"得分: {result['score']}, 复杂度概率: {result['probability']}")
        print(f"路由决策: {result['route_target']}")