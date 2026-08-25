import os
import chromadb
import ollama

# --------------------------------------------------------------
# 1. READ & CHUNK THE DOCUMENT
# --------------------------------------------------------------
file_path = "my_notes.txt"

if not os.path.exists(file_path):
    print(f"❌ Error: Could not find '{file_path}'. Make sure it is in your folder!")
    exit()

with open(file_path, "r", encoding="utf-8") as f:
    text = f.read().strip()

if len(text) == 0:
    print(f"❌ Error: '{file_path}' is empty!")
    exit()

# Chunk text into manageable pieces
chunk_size = 300
overlap = 50
chunks = [text[i : i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]

# --------------------------------------------------------------
# 2. STORE CHUNKS IN CHROMADB
# --------------------------------------------------------------
chroma_client = chromadb.Client()
collection = chroma_client.create_collection(name="local_notes")

collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print("\n--- Notes Database Ready! ---")
print("Type your question below (or type 'exit' to quit).\n")

# --------------------------------------------------------------
# 3. INTERACTIVE CHAT LOOP
# --------------------------------------------------------------
while True:
    user_query = input("Ask a question about your notes: ")

    # Check if the user wants to quit
    if user_query.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    if not user_query.strip():
        continue

    # Retrieve relevant context
    results = collection.query(
        query_texts=[user_query],
        n_results=2
    )

    retrieved_context = "\n---\n".join(results["documents"][0])

    prompt = f"""
Answer the user's question using ONLY the provided context below.
If the context doesn't contain the answer, say "I couldn't find that in your notes."

Context:
{retrieved_context}

User Question: {user_query}
"""

    # Generate answer
    response = ollama.chat(
        model="llama3.2",
        messages=[{"role": "user", "content": prompt}]
    )

    print("\n🤖 Answer:")
    print(response["message"]["content"])
    print("-" * 50 + "\n")