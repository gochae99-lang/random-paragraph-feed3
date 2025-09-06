import streamlit as st
import pdfplumber
import random
import re

st.set_page_config(page_title="랜덤 텍스트 피드", layout="centered")
st.title("📖 PDF 랜덤 쓱뽕 피드 (문장 기준)")
st.markdown("PDF에서 문장 단위로 추출한 텍스트를 랜덤으로 보여줍니다. 최신 10개까지만 표시됩니다.")

# 세션 상태 초기화
if 'texts' not in st.session_state:
    st.session_state.texts = []  # (pdf_title, sentence)
if 'feed' not in st.session_state:
    st.session_state.feed = []

# PDF 업로드
uploaded_files = st.file_uploader("📄 PDF 파일 업로드 (여러 개 가능)", type="pdf", accept_multiple_files=True)

# 문장 단위로 나누는 함수
def split_into_sentences(text, max_len=280):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        if len(sent) <= max_len:
            chunks.append(sent)
        else:
            for i in range(0, len(sent), max_len):
                chunks.append(sent[i:i+max_len].strip())
    return chunks

# PDF 업로드 시 즉시 문장 단위로 텍스트 준비
if uploaded_files:
    for uploaded_file in uploaded_files:
        pdf_title = uploaded_file.name
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    sentences = split_into_sentences(text)
                    st.session_state.texts.extend([(pdf_title, s) for s in sentences])
    st.success(f"{len(st.session_state.texts)} 문장 추출 완료!")

# 버튼 영역
col1, col2 = st.columns(2)
with col1:
    if st.button("🎲 랜덤 텍스트 추가"):
        if st.session_state.texts:
            pdf_title, new_text = random.choice(st.session_state.texts)
            st.session_state.feed.insert(0, (pdf_title, new_text))
            st.session_state.feed = st.session_state.feed[:10]

with col2:
    if st.button("🔁 연속 랜덤 5개 추가"):
        if st.session_state.texts:
            for _ in range(min(5, len(st.session_state.texts))):
                st.session_state.feed.insert(0, random.choice(st.session_state.texts))
            st.session_state.feed = st.session_state.feed[:10]

# 피드 출력 (expander 사용)
if st.session_state.feed:
    st.markdown("### 📰 최신 랜덤 텍스트 (최대 10개)")
    for pdf_title, txt in st.session_state.feed:
        with st.expander(f"📄 {pdf_title}"):
            st.markdown(f"{txt}")
else:
    st.info("PDF 파일을 업로드하세요.")
