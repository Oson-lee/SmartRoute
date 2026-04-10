import streamlit as st
from router import ComplexityRouter
from llm_client import LLMDispatcher

# ================= 1. 页面配置 =================
st.set_page_config(page_title="SmartRoute MVP", page_icon="🧭", layout="wide")

# ================= 2. 初始化核心组件 =================
# 使用 cache_resource 防止每次刷新页面都重新初始化
@st.cache_resource
def init_components():
    try:
        return ComplexityRouter(), LLMDispatcher()
    except Exception as e:
        st.error(f"❌ 初始化失败: {str(e)}")
        st.stop()

router, dispatcher = init_components()

# 初始化 session_state 缓存，用于存储对话历史和累计省下的钱
if "messages" not in st.session_state:
    st.session_state.messages = []
if "total_saved" not in st.session_state:
    st.session_state.total_saved = 0.0

# ================= 3. 页面布局 (前端 UI) =================
st.title("🧭 SmartRoute 智能路由网关 (MVP)")
st.markdown("基于数学启发式评估的 LLM 动态路由中间件。自动将简单任务分配给低成本模型，复杂任务分配给高智商模型。")

# 侧边栏：成本节省看板 + 控制面板
with st.sidebar:
    st.header("💰 成本节省看板")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="累计节省", value=f"${st.session_state.total_saved:.4f}")
    with col2:
        st.metric(label="对话次数", value=len([m for m in st.session_state.messages if m['role'] == 'user']))
    
    st.markdown("---")
    st.markdown("**计费测算参考:**\n* 高配模型全量请求: ~$0.010 / 次\n* 降级低配模型: ~$0.001 / 次\n* **每次降级可省**: **$0.009**")
    
    st.markdown("---")
    st.subheader("⚙️ 控制面板")
    
    # 清除历史记录按钮
    if st.button("🗑️ 清除对话历史", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_saved = 0.0
        st.success("✓ 历史已清除")
        st.rerun()
    
    # 显示系统状态
    st.markdown("---")
    st.subheader("📊 系统状态")
    st.info(f"✓ 路由器: OK\n✓ 调度器: OK\n✓ 缓存: 已启用")

# 展示历史对话
if st.session_state.messages:
    st.markdown("### 📝 对话历史")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "meta" in msg:
                st.caption(f"🔧 {msg['meta']}")

# ================= 4. 核心交互逻辑 =================
# 聊天输入框
if prompt := st.chat_input("输入测试问题 (试试普通的闲聊，或者复杂的数学/代码任务)..."):
    
    # 将用户输入上屏并保存
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # AI 处理与回答区块
    with st.chat_message("assistant"):
        with st.spinner("🧠 SmartRoute 正在进行智能路由..."):
            try:
                # 第一步：调用大脑 (router) 评估复杂度
                route_res = router.evaluate(prompt)
                
                # 第二步：调用神经 (llm_client) 获取大模型回答
                llm_res = dispatcher.get_response(prompt, route_res["route_target"])
                
                # 检查LLM返回状态
                if llm_res["status"] == "error":
                    st.error(f"❌ 模型调用失败: {llm_res['answer']}")
                    st.session_state.messages.pop()  # 移除本次记录
                    st.stop()
                
                # 第三步：计算省了多少钱 (如果是低成本路由，就省下了差价)
                saved_this_time = 0.0
                if route_res["route_target"] == "Low-Cost Route":
                    saved_this_time = 0.009
                    st.session_state.total_saved += saved_this_time # 累加到侧边栏面板
                
                # 第四步：组装底层信息面板
                answer = llm_res["answer"]
                meta_info = f"复杂度: {route_res['probability']*100:.1f}% | 路由: **{route_res['route_target']}** | 模型: **{llm_res['model_used']}** | 节省: **${saved_this_time:.4f}**"
                
                # 将回答和底层信息展示到网页上
                st.markdown(answer)
                st.caption(f"🔧 {meta_info}")
                
                # 将 AI 的回答保存到历史记录
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer,
                    "meta": meta_info
                })
                
            except Exception as e:
                error_msg = f"处理失败: {str(e)}"
                st.error(f"❌ {error_msg}")
                st.session_state.messages.pop()  # 移除本次失败的用户输入
                st.stop()