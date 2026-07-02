import streamlit as st
from src.rag.generator import RAG
import pandas as pd
from collections import Counter

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
        # Extract properties from evidence
        props_list = [item[0] if isinstance(item, tuple) else item for item in evidence]

        if result.get("summary"):
            st.subheader("Evidence Summary")
            st.write(result["summary"])
            
        st.divider()
    
        st.subheader("Sentiment Breakdown")
        st.caption("How developers feel about this topic based on retrieved discussions")
        sentiments = [p.get("sentiment_label", "neutral") for p in props_list]
        sentiment_counts = Counter(sentiments)
        sentiment_df = pd.DataFrame({
            "Sentiment": list(sentiment_counts.keys()),
            "Count": list(sentiment_counts.values())
        })
        st.bar_chart(sentiment_df.set_index("Sentiment"))
 
        st.divider()
 
        # Source Breakdown
        st.subheader("Source Breakdown")
        st.caption("Where these discussions come from")
        sources = [p.get("source", "unknown") for p in props_list]
        source_counts = Counter(sources)
        source_df = pd.DataFrame({
            "Source": list(source_counts.keys()),
            "Count": list(source_counts.values())
        })
        st.bar_chart(source_df.set_index("Source"))
 
        st.divider()
 
        # Top Keywords 
        st.subheader("Top Keywords")
        st.caption("Most frequent technical terms across retrieved discussions")
        all_keywords = []
        for p in props_list:
            kw = p.get("keyword", [])
            if isinstance(kw, list):
                all_keywords.extend(kw)
            elif isinstance(kw, str):
                try:
                    import ast
                    all_keywords.extend(ast.literal_eval(kw))
                except:
                    pass
        if all_keywords:
            kw_counts = Counter(all_keywords).most_common(10)
            kw_df = pd.DataFrame(kw_counts, columns=["Keyword", "Count"])
            st.bar_chart(kw_df.set_index("Keyword"))
 
        st.divider()
 
        # Source Comparison 
        st.subheader("YouTube vs Stack Overflow")
        st.caption("How each community discusses this topic differently")
 
        yt_comments = [p.get("text_clean", "") for p in props_list if p.get("source") == "youtube"]
        so_comments = [p.get("text_clean", "") for p in props_list if p.get("source") == "stackoverflow"]
 
        col_yt, col_so = st.columns(2)
 
        with col_yt:
            st.markdown("**YouTube Developers say:**")
            if yt_comments:
                for c in yt_comments:
                    st.caption(f'"{c}"')
            else:
                st.caption("No YouTube results for this query.")
 
        with col_so:
            st.markdown("**Stack Overflow Experts say:**")
            if so_comments:
                for c in so_comments:
                    st.caption(f'"{c}"')
            else:
                st.caption("No Stack Overflow results for this query.")
 
        st.divider()
 
        #  Evidence 
        with st.expander(f"Full Evidence ({len(evidence)} results)"):
            for item in evidence:
                props = item[0] if isinstance(item, tuple) else item
                st.markdown(f"**{props.get('source', '').upper()}** | {props.get('sentiment_label', '')} | {props.get('author') or 'Anonymous'}")
                st.write(props.get("text_clean", ""))
                st.divider()