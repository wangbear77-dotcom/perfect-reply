import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="高情商回覆生成器", page_icon="💬", layout="centered")

# --- 2. 標題 ---
st.title("💬 高情商回覆生成器")
st.markdown("遇到 **已讀不回**？**尷尬話題**？讓 AI 幫你生成 **得體、幽默、或犀利** 的神回覆。")

# --- 3. 側邊欄：API Key 處理 (零門檻化) ---
with st.sidebar:
    st.header("🔑 啟動金鑰")

    # 🔥 V14.0 核心：優先讀取後台 Secrets (用戶看不到的 Key)
    sys_api_key = None
    try:
        if "GEMINI_API_KEY" in st.secrets:
            sys_api_key = st.secrets["GEMINI_API_KEY"]
            st.success("✅ 系統已自動連接金鑰 (零門檻模式)")
    except:
        pass

    # 如果後台沒設定 (開發者/本地測試模式)，才顯示輸入框
    if not sys_api_key:
        sys_api_key = st.text_input("開發者/本地測試專用 Key", type="password")
        if not sys_api_key:
            st.warning("⚠️ 請貼上 Key 以啟動功能")
        
        with st.expander("❓ 沒有 Key？ 30秒免費領取教學"):
            st.markdown("""
            **步驟 1：** 點擊 👉 **[Google AI Studio](https://aistudio.google.com/app/apikey)**
            **步驟 2：** 點擊藍色的 **"Create API Key"** 按鈕。
            **步驟 3：** 複製 `AIza` 開頭的密碼，貼回上面的格子即可！
            *(這是你的金鑰，請勿公開)*
            """)
    
    st.divider()
    
    # 模型選擇
    selected_model_name = st.selectbox("選擇 AI 模型", ["gemini-2.0-flash-exp", "gemini-2.5-flash", "gemini-2.5-pro"], index=1)
    
# --- 4. 主介面：功能區 (判斷是否有金鑰) ---

# 如果沒有任何 Key (包括 Secrets 和手動輸入都沒給)，則禁用功能
if not sys_api_key:
    st.warning("👈 **功能未啟用：請在左側貼上 API Key**")
    st.text_area("對方說了什麼？", height=100, disabled=True, placeholder="請先啟動功能...")
    st.button("✨ 生成神回覆", disabled=True)

else:
    # --- Key 存在時，顯示完整功能 ---
    
    user_input = st.text_area("對方說了什麼？", height=100, placeholder="例如：你到底什麼時候才要結婚？")
    style_option = st.selectbox("風格", ("😎 幽默風趣", "❤️ 曖昧調情", "🛡️ 禮貌婉拒", "🔪 犀利回擊"))

    if st.button("✨ 生成神回覆", type="primary"):
        if not user_input:
            st.warning("⚠️ 請先輸入對方說了什麼！")
        else:
            try:
                # 使用 sys_api_key 進行調用
                genai.configure(api_key=sys_api_key)
                model = genai.GenerativeModel(selected_model_name)
                
                prompt = f"""
                你是一位社交溝通專家。
                情境：收到訊息 "{user_input}"
                目標：用 "{style_option}" 風格生成 3 個回覆 (台灣口語)。
                格式：
                ### 選項一：[標題]
                **回覆：**「[內容]」
                💡 **解析：** [解析內容]
                (請提供三個選項)
                """

                with st.spinner(f"🧠 AI 正在運算中 ({selected_model_name})..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 👇 挑一個喜歡的複製吧！")
                    st.markdown(response.text)
                    st.success("🎉 成功了！")
                    
            except Exception as e:
                st.error(f"發生錯誤：{e}")
                if "429" in str(e):
                    st.warning("⚠️ 額度不足。請稍等一分鐘再試，或更換模型。")

# --- 5. 頁尾 ---
st.divider()
st.caption("Micro-SaaS V14.0 (Zero Barrier Mode)")
