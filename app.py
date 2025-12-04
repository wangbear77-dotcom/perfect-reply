import streamlit as st
import google.generativeai as genai

# --- 1. 頁面設定 ---
st.set_page_config(page_title="高情商回覆生成器", page_icon="💬", layout="centered")

# --- 2. 標題 ---
st.title("💬 高情商回覆生成器")
st.markdown("遇到 **已讀不回**？**尷尬話題**？讓 AI 幫你生成 **得體、幽默、或犀利** 的神回覆。")

# --- 3. 側邊欄：設定與打賞 ---
with st.sidebar:
    st.header("🔑 啟動金鑰")

    # [A] 隱藏式 API Key (優先讀取 Secrets)
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
            1. 點擊 👉 **[Google AI Studio](https://aistudio.google.com/app/apikey)**
            2. 點擊藍色的 **"Create API Key"** 按鈕。
            3. 複製 `AIza` 開頭的密碼，貼回上面的格子即可！
            """)
    
    st.divider()

    # [B] 🔥 新增：打賞鼓勵區
    st.subheader("☕ 鼓勵開發者")
    st.markdown("如果覺得這工具救了你的社交生活，歡迎請我喝杯咖啡！")
    
    # 請將 href 換成你自己的 Buy Me a Coffee 網址
    st.markdown(
        """
        <a href="https://www.buymeacoffee.com/wangbear77" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 150px !important;" >
        </a>
        """,
        unsafe_allow_html=True
    )

    st.divider()
    
    # [C] 模型選擇 (加入最新的 2.5 系列)
    selected_model_name = st.selectbox(
        "選擇 AI 模型", 
        ["gemini-2.5-flash", "gemini-2.0-flash-exp", "gemini-2.5-pro"]
    )
    
# --- 4. 主介面：功能區 ---

# 如果沒有任何 Key，禁用功能
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
                genai.configure(api_key=sys_api_key)
                model = genai.GenerativeModel(selected_model_name)
                
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

                with st.spinner(f"🧠 AI 正在運算中 ({selected_model_name})..."):
                    response = model.generate_content(prompt)
                    st.markdown("### 👇 挑一個喜歡的複製吧！")
                    st.markdown(response.text)
                    st.success("🎉 成功了！如果不滿意，可以再按一次生成。")
                    
            except Exception as e:
                st.error(f"發生錯誤：{e}")
                if "429" in str(e):
                    st.warning("⚠️ 額度不足。請稍等一分鐘再試，或更換模型。")

# --- 5. 頁尾 ---
st.divider()
st.caption("Micro-SaaS V15.0 (Donation Model)")
