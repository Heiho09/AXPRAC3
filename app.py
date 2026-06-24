import streamlit as st
from data_loader import load_qa_data
from search import build_index, search

st.set_page_config(page_title="의료 Q&A 검색", page_icon="🏥", layout="centered")


@st.cache_resource
def get_index():
    records = load_qa_data()
    vectorizer, matrix = build_index(records)
    return records, vectorizer, matrix


records, vectorizer, matrix = get_index()

st.title("의료 Q&A 검색")
st.caption(f"총 {len(records)}개 Q&A 기반 검색 (내과 · 산부인과 · 소아청소년과 · 응급의학과)")

with st.form("search_form"):
    query = st.text_input(
        "질문 또는 키워드를 입력하세요",
        placeholder="예: COPD 합병증, 자궁내막증 진단, 간질 발작 처치",
    )
    submitted = st.form_submit_button("검색", type="primary")

if submitted:
    if not query.strip():
        st.warning("검색어를 입력해주세요.")
    else:
        with st.spinner("검색 중..."):
            results = search(query, records, vectorizer, matrix, top_n=5)

        if not results:
            st.info("유사한 Q&A를 찾지 못했습니다. 더 구체적인 의학 용어나 증상으로 검색해보세요.")
        else:
            st.markdown(f"**{len(results)}개 결과**")
            for r in results:
                label = f"[{r['department']}] {r['question'][:60]}{'...' if len(r['question']) > 60 else ''}"
                with st.expander(label, expanded=True):
                    st.markdown("**질문**")
                    st.write(r["question"])
                    st.divider()
                    st.markdown("**답변**")
                    st.write(r["answer"])
                    col1, col2, col3 = st.columns(3)
                    col1.metric("진료과", r["department"])
                    col2.metric("문제 유형", r["q_type_label"])
                    col3.metric("유사도", f"{r['score']:.2f}")
