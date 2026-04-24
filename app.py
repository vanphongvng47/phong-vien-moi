import os
import subprocess
import sys

# Tự động cài đặt thư viện nếu thiếu (Chiêu cuối để sửa lỗi ModuleNotFoundError)
def install_dependencies():
    try:
        import langchain
        import langchain_openai
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "langchain", "langchain-openai"])

install_dependencies()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Cấu hình trang web
st.set_page_config(page_title="AI Phóng Viên Hệ Điều Hành", layout="wide")

# Giao diện Sidebar
st.sidebar.header("⚙️ Cấu hình AI")
api_key = st.sidebar.text_input("Nhập OpenAI API Key", type="password")
model_choice = st.sidebar.selectbox("Chọn Model", ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"])
temperature = st.sidebar.slider("Độ 'phiêu' (Cảm xúc)", 0.0, 1.0, 0.7)

# Giao diện chính
st.title("✍️ AI Phóng Viên: Viết Báo Bằng Trái Tim")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📥 Dữ liệu đầu vào")
    raw_data = st.text_area("Nhập thông tin thô, số liệu hoặc sự kiện...", height=300, 
                            placeholder="Ví dụ: Lễ khánh thành cầu nông thôn, kinh phí 2 tỷ, dân bản vui mừng...")
    
    style = st.selectbox("Chọn phong cách viết", 
                          ["Phóng sự giàu cảm xúc", "Tin tức nhanh chính xác", "Xã luận sắc bén", "Ký sự nhân văn"])
    
    submit_button = st.button("🚀 Bắt đầu chấp bút")

with col2:
    st.subheader("📰 Bài báo hoàn chỉnh")
    if submit_button:
        if not api_key:
            st.error("Vui lòng nhập API Key ở bên trái!")
        elif not raw_data:
            st.warning("Vui lòng nhập dữ liệu thô!")
        else:
            with st.spinner("AI đang nhập vai phóng viên và viết bài..."):
                try:
                    # Thiết lập LLM (Sử dụng cú pháp mới nhất của LangChain)
                    llm = ChatOpenAI(model=model_choice, temperature=temperature, openai_api_key=api_key)
                    
                    template = """
                    Bạn là một phóng viên kỳ cựu chuyên viết về {style}.
                    Dựa trên dữ liệu thô sau đây, hãy tạo ra một bài báo hoàn chỉnh:
                    ---
                    DỮ LIỆU: {data}
                    ---
                    YÊU CẦU:
                    1. Tiêu đề hấp dẫn, gợi cảm xúc.
                    2. Sapo lôi cuốn.
                    3. Nội dung chi tiết, sử dụng ngôn từ hình ảnh, không khô khan nhưng phải tuyệt đối chính xác về số liệu/tên riêng.
                    4. Kết luận nhân văn.
                    
                    Hãy viết bằng tiếng Việt, giọng văn tự nhiên như người viết.
                    """
                    
                    prompt = PromptTemplate(template=template, input_variables=["style", "data"])
                    
                    # Chạy AI bằng LCEL (Cú pháp hiện đại nhất)
                    chain = prompt | llm
                    response = chain.invoke({"style": style, "data": raw_data})
                    article = response.content
                    
                    # Hiển thị kết quả
                    st.markdown(article)
                    st.download_button("📥 Tải bài viết (.txt)", article, file_name="bai_bao_ai.txt")
                except Exception as e:
                    st.error(f"Có lỗi xảy ra: {e}")
    else:
        st.info("Kết quả sẽ hiển thị ở đây sau khi bạn nhấn nút.")

st.markdown("---")
st.caption("Công cụ hỗ trợ tác nghiệp dành cho phóng viên hiện đại.")
