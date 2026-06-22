import streamlit as st
from src.rag.generator import RAG

st.title("Refract")
st.caption("Audience intelligence engine for systems programming discussions")

query = st.text_input("Ask a question about systems programming:")

if st.button("Ask") and query.strip():
    with st.spinner("Searching dataset..."):
        rag = RAG(query=query, threshold=0.6)
        result = rag.routing()
        rag.close()
    
    st.subheader("Answer")
    st.write(result["answer"])

    st.subheader("Source")
    st.write(result["source"])

    st.subheader("Confidence")
    st.progress(result["confidence"])
    st.caption(f"{round(result['confidence'] * 100)}% confidence")
    evidence = result.get("evidence", [])
    #below is done using ai i couldnt figure out to do it. wait no im just lazy to do LMAO
    if evidence:
        with st.expander(f"Evidence ({len(evidence)} results)"):
            for item in evidence:
                props = item[0] if isinstance(item, tuple) else item
                st.markdown(f"**{props.get('source', '').upper()}** | {props.get('sentiment_label', '')} | {props.get('author') or 'Anonymous'}")
                st.write(props.get("text_clean", ""))
                st.divider()
