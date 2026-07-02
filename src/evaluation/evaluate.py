import mlflow
from src.rag.generator import RAG

mlflow.set_experiment("Refract-Evaluation")

test_questions = [
    "What frustrates C++ developers about memory management?",
    "Is Rust better than C++ for systems programming?",
    "What do developers think about undefined behavior in C++?",
    "How do developers feel about learning C++?",
    "What are common mistakes in multithreading with C++?",
    "What is the opinion on modern C++ features?",
    "How do Stack Overflow experts recommend handling memory leaks?",
    "What do developers say about C++ vs Python performance?",
    "What tools do systems programmers use for debugging?",
    "What is the general sentiment around the C++ learning curve?",
    "What is photosynthesis?",
    "Who is Lionel Messi?",
    "What is machine learning?",
    "What is the capital of France?",
    "How do I bake a chocolate cake?"
]

for question in test_questions:
    with mlflow.start_run(run_name=question[:50]):
        rag = RAG(query=question, threshold=0.6)
        result = rag.routing()
        rag.close()

        mlflow.log_param("question", question)
        mlflow.log_param("source", str(result["source"]))
        mlflow.log_metric("confidence", result["confidence"])
        mlflow.log_metric("evidence_count", len(result["evidence"]))
        mlflow.log_metric("used_fallback", 1 if result["source"] == "Ollama fallback" else 0)
        mlflow.log_text(result["answer"], "answer.txt")

        print(f"Logged: {question[:50]} | Confidence: {result['confidence']:.2f} | Source: {result['source']}")