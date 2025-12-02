import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="高情商回覆生成器", page_icon="💬", layout="centered")

# --- 2. 標題 ---
st.title("💬 高情商回覆生成器")
st.markdown("遇到 **已讀不回**？**尷尬話題**？讓 AI 幫你生成 **得體、幽默、或犀利** 的神回覆。")

# --- 3. 側邊欄：API Key 輸入 + 傻瓜教學 ---
with st.sidebar:
    st.header("🔑 啟動金鑰")
    
    # 輸入框
    api_key = st.text_input("請在此貼上 Gemini API Key", type="password", placeholder="AIzaSy...")
    
    # 🔥 V13.0 核心：內建傻瓜教學 (使用 Expander 收納，不佔空間)
    with st.expander("❓ 沒有 Key？ 30秒免費領取教學"):
        st.markdown("""
        **完全免費，只需 3 步：**
        
        1. 👉 **[點擊這裡打開 Google AI Studio](https://aistudio.google.com/app/apikey)** (需登入 Google)
        2. 點擊藍色的 **"Create API Key"** 按鈕。
        3. 複製那串 **`AIza`** 開頭的密碼，貼回上面的格子即可！
        
        *(這是 Google 官方提供的免費額度，請安心使用)*
        """)
    
    st.divider()
    
    if api_key:
        st.success("✅ 已連接！可以開始使用了")
    else:
        st.info("⬅️ 請先輸入 Key 才能解鎖功能喔！")

# --- 4. 主介面 ---

# 鎖定模型 (延續 V11 的設定)
my_models = ["gemini-2.5-flash", "gemini-2.5-pro"]

# 如果沒有 Key，主畫面顯示一個大大的提示，引導他去看左邊
if not api_key:
    st.warning("👈 **請先在左側欄位貼上 API Key**")
    st.markdown("如果你沒有 Key，請點開左側的 **「❓ 沒有 Key？」** 看教學，30 秒就能拿到！")
    
    # 為了版面好看，放一張示意圖或佔位符
    st.text_area("對方說了什麼？", height=100, disabled=True, placeholder="請先解鎖...")
    st.button("✨ 生成神回覆", disabled=True)

else:
    # --- 有 Key 才顯示完整功能 ---
    
    # 模型選擇區
    col1, col2 = st.columns([3, 1])
    with col1:
        selected_model_name = st.selectbox("選擇模型", my_models, index=0)
    with col2:
        manual_mode = st.checkbox("手動修改")

    if manual_mode:
        final_model = st.text_input("請輸入準確的模型代號", value=selected_model_name)
    else:
        final_model = selected_model_name

    # 輸入區
    user_input = st.text_area("對方說了什麼？", height=100, placeholder="例如：你到底什麼時候才要結婚？")
    style_option = st.selectbox("風格", ("😎 幽默風趣", "❤️ 曖昧調情", "🛡️ 禮貌婉拒", "🔪 犀利回擊"))

    if st.button("✨ 生成神回覆", type="primary"):
        if not user_input:
            st.warning("⚠️ 請先輸入對方說了什麼！")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel(final_model)
                
                prompt = f"""
                你是一位社交溝通專家。
                情境：收到訊息 "{user_input}"
                目標：用 "{style_option}" 風格生成 3 個回覆 (台灣口語)。
                格式：
                ### 選項一：[標題]
                **回覆：**「[內容]」
                💡 **解析：** [內容]
                (請提供三個選項)
                """

                with st.spinner(f"🧠 AI 正在運算中 ({final_model})..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 👇 挑一個喜歡的複製吧！")
                    st.markdown(response.text)
                    st.success("🎉 成功了！")
                    
            except Exception as e:
                st.error(f"發生錯誤：{e}")
                if "429" in str(e):
                    st.warning("⚠️ 您的 API Key 額度暫時用完，請稍等幾分鐘再試。")
                elif "404" in str(e):
                    st.error("❌ 模型名稱錯誤，請檢查手動輸入的代號。")

# --- 5. 頁尾 ---
st.divider()
st.caption("Micro-SaaS V13.0 (BYOK Tutorial Mode)")