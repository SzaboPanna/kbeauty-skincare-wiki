import os
import json
import streamlit as st
from openai import OpenAI

# 1. PAGE SETUP
st.set_page_config(page_title="K-Beauty Skincare Wiki", page_icon="✨", layout="wide")

# 2. INJECT PASTEL LILAC & HIGH-CONTRAST CSS
st.markdown("""
<style>
/* Main Gradient Background & Dark Base Text */
.stApp {
    background: linear-gradient(135deg, #fff5f7 0%, #f7f3ff 50%, #f0f7ff 100%) !important;
    color: #2b2038 !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Force text visibility across headers, body, labels, and markdown */
h1, h2, h3, h4, h5, h6, p, span, label, div, summary, caption {
    color: #2b2038 !important;
}

/* Headings */
h1 {
    color: #3b2a59 !important;
    font-weight: 700 !important;
}

h2, h3 {
    color: #4a3b69 !important;
    font-weight: 600 !important;
}

/* Glassmorphism Expander Cards */
div[data-testid="stExpander"] {
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 16px !important;
    border: 1px solid rgba(230, 180, 200, 0.5) !important;
    box-shadow: 0 8px 24px 0 rgba(150, 100, 150, 0.08);
    margin-bottom: 12px;
}

/* Expander Header Text */
div[data-testid="stExpander"] summary p, div[data-testid="stExpander"] summary span {
    color: #2b2038 !important;
    font-weight: 600 !important;
}

/* Tab Selection Styling */
button[data-baseweb="tab"] {
    background-color: rgba(255, 255, 255, 0.6) !important;
    border-radius: 20px !important;
    padding: 8px 24px !important;
    border: 1px solid transparent !important;
}

button[data-baseweb="tab"] p, button[data-baseweb="tab"] span {
    color: #5a4b7c !important;
    font-weight: 600 !important;
}

button[aria-selected="true"] {
    background: linear-gradient(135deg, #ffc0cb 0%, #e6e6fa 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    box-shadow: 0 4px 15px rgba(255, 192, 203, 0.4);
}

button[aria-selected="true"] p, button[aria-selected="true"] span {
    color: #2c1e4a !important;
    font-weight: 700 !important;
}

/* Inputs & Form Controls Base */
input, select, textarea, div[data-baseweb="select"] {
    color: #000000 !important;
    background-color: #ffffff !important;
    border-radius: 10px !important;
}

/* DROPDOWN MENU FIX: Pastel Lilac Background & Black Text */
div[data-baseweb="popover"],
div[data-baseweb="popover"] *,
div[data-baseweb="menu"],
div[data-baseweb="menu"] *,
ul[data-baseweb="menu"],
ul[data-baseweb="menu"] *,
[data-baseweb="option"],
[data-baseweb="option"] * {
    background-color: #E5D9F2 !important;
    color: #000000 !important;
    font-weight: 600 !important;
}

/* Dropdown Hover & Selected State */
[data-baseweb="option"]:hover,
[data-baseweb="option"]:hover *,
li[aria-selected="true"],
li[aria-selected="true"] * {
    background-color: #D4BEEB !important;
    color: #000000 !important;
    font-weight: 700 !important;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(135deg, #ff9ebb 0%, #c49ed8 100%) !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 12px rgba(255, 158, 187, 0.4) !important;
    transition: all 0.3s ease !important;
}

.stButton>button p, .stButton>button span {
    color: #ffffff !important;
    font-weight: 700 !important;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(255, 158, 187, 0.6) !important;
}

/* Product Card Images */
img {
    border-radius: 12px;
    object-fit: cover;
}
</style>
""", unsafe_allow_html=True)

st.title("✨ K-Beauty Skincare Wiki & AI Assistant")

# 3. API KEY DETECTION (Cloud Secrets vs Local Fallback)
try:
    DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
except Exception:
    DEEPSEEK_API_KEY = "sk-ce85833ae46843db9a6d5f8e03fa8a5f"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

# 4. LOAD DATABASE
DATA_FILE = "skincare_data.json"

@st.cache_data
def load_skincare_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

skincare_db = load_skincare_data()

# 5. DEFINE AGENT TOOL & SCHEMA
def search_skincare_db(query: str) -> str:
    """
    Search the local Korean Skincare database for products, brands, skin types, recommendations, or video review links.
    """
    if not skincare_db:
        return "Skincare database is empty."
    
    query_lower = query.lower()
    matched_products = []

    for item in skincare_db:
        searchable_text = f"{item['name']} {item['brand']} {item['category']} {' '.join(item['skin_type'])} {item['skin_sheet']}".lower()
        if any(term in searchable_text for term in query_lower.split()):
            matched_products.append(item)

    if not matched_products:
        return f"No products found in the database for query: '{query}'."

    results = []
    for p in matched_products:
        results.append(
            f"Product: {p['name']} by {p['brand']}\n"
            f"Category: {p['category']}\n"
            f"Best for Skin Types: {', '.join(p['skin_type'])}\n"
            f"Skin Sheet: {p['skin_sheet']}\n"
            f"Pros: {', '.join(p['pros'])}\n"
            f"Cons: {', '.join(p['cons'])}\n"
            f"Try-out Video: {p['video_url']}\n"
        )
    return "\n---\n".join(results)

AVAILABLE_TOOLS = {
    "search_skincare_db": search_skincare_db
}

tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "search_skincare_db",
            "description": "Search the local Korean Skincare database for products, brands, skin types, recommendations, or video review links.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keywords such as product name, brand, skin type (e.g., 'dry', 'sensitive'), or category."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# 6. STREAMLIT NAVIGATION TABS
tab1, tab2, tab3 = st.tabs(["📚 Skincare Directory", "💬 AI Skincare Assistant", "🪄 AM/PM Routine Quiz"])

# --- TAB 1: WIKI DIRECTORY ---
with tab1:
    st.subheader("Browse Korean Skincare Products")
    
    search_term = st.text_input("🔍 Search products by name, brand, or ingredient:", "")
    
    filtered_db = skincare_db
    if search_term:
        filtered_db = [
            item for item in skincare_db 
            if search_term.lower() in item['name'].lower() 
            or search_term.lower() in item['brand'].lower()
            or search_term.lower() in item['category'].lower()
        ]

    for item in filtered_db:
        with st.expander(f"**{item['brand']}** - {item['name']} ({item['category']})"):
            img_col, text_col = st.columns([1, 2])
            
            with img_col:
                if item.get('image_url'):
                    st.image(item['image_url'], use_container_width=True)
            
            with text_col:
                st.markdown(f"**Skin Types:** {', '.join([f'`{s}`' for s in item['skin_type']])}")
                st.markdown(f"**Skin Sheet:** {item['skin_sheet']}")
                
                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    st.markdown("**Pros:**")
                    for pro in item['pros']:
                        st.markdown(f"- ✅ {pro}")
                with p_col2:
                    st.markdown("**Cons:**")
                    for con in item['cons']:
                        st.markdown(f"- ❌ {con}")
                
                if item.get('video_url'):
                    st.video(item['video_url'])
                    st.link_button("▶️ Watch directly on YouTube", item['video_url'])

# --- TAB 2: CHATBOT INTERFACE ---
with tab2:
    st.subheader("Ask Your AI Skincare Assistant")
    st.caption("Powered by DeepSeek AI - Ask for recommendations, Skin Sheets, or video review links!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("e.g. What is the Skin Sheet for Beauty of Joseon sunscreen?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("DeepSeek is thinking..."):
                system_instruction = (
                    "You are an expert K-Beauty assistant powered by DeepSeek.\n"
                    "1. Always call `search_skincare_db` to look up product details from the database.\n"
                    "2. ALWAYS include the YouTube try-out video link as an explicit Markdown link (e.g. [Watch Try-out Video](url)) in your final response."
                )
                
                messages = [{"role": "system", "content": system_instruction}]
                for msg in st.session_state.messages:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                max_turns = 3
                turns = 0
                
                while turns < max_turns:
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=messages,
                        tools=tools_schema
                    )
                    
                    msg = response.choices[0].message
                    messages.append(msg)

                    if msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            fn_name = tool_call.function.name
                            fn_args = json.loads(tool_call.function.arguments)
                            
                            st.info(f"🛠️ **DeepSeek searching Wiki DB for:** `{fn_args}`")
                            
                            if fn_name in AVAILABLE_TOOLS:
                                tool_out = AVAILABLE_TOOLS[fn_name](**fn_args)
                                messages.append({
                                    "role": "tool",
                                    "tool_call_id": tool_call.id,
                                    "content": tool_out
                                })
                        turns += 1
                    else:
                        st.markdown(msg.content)
                        st.session_state.messages.append({"role": "assistant", "content": msg.content})
                        break

# --- TAB 3: ROUTINE QUIZ & GENERATOR ---
with tab3:
    st.subheader("🪄 Interactive Skin Quiz & AM/PM Routine Generator")
    st.caption("Answer 3 quick questions to generate a step-by-step Morning and Evening routine using products exclusively from your catalog!")

    col1, col2, col3 = st.columns(3)
    with col1:
        skin_type = st.selectbox(
            "1. Select your Skin Type:",
            ["Dry", "Oily", "Combination", "Sensitive", "Dehydrated", "Normal"]
        )
    with col2:
        concern = st.selectbox(
            "2. Select Primary Skin Concern:",
            ["Acne & Breakouts", "Anti-Aging & Fine Lines", "Redness & Sensitivity", "Pores & Rough Texture", "Barrier Repair & Dryness"]
        )
    with col3:
        routine_style = st.selectbox(
            "3. Choose Routine Complexity / Budget:",
            ["Minimalist Routine (2-3 Core Steps)", "Balanced Routine (4-5 Steps)", "Full Glass-Skin Routine (6+ Steps)"]
        )

    if st.button("✨ Generate My Custom AM/PM Routine", use_container_width=True):
        with st.spinner("DeepSeek is analyzing your catalog and building your routine..."):
            catalog_summary = "\n".join([
                f"- Name: {item['name']} | Brand: {item['brand']} | Category: {item['category']} | Suitable for: {', '.join(item['skin_type'])} | Summary: {item['skin_sheet']} | Video: {item['video_url']}"
                for item in skincare_db
            ])

            quiz_prompt = (
                f"Build a personalized AM and PM skincare routine for a user with the following profile:\n"
                f"- Skin Type: {skin_type}\n"
                f"- Primary Concern: {concern}\n"
                f"- Preferred Complexity: {routine_style}\n\n"
                f"CATALOG PRODUCTS (YOU MUST ONLY USE PRODUCTS FROM THIS LIST):\n"
                f"{catalog_summary}\n\n"
                f"STRICT FORMATTING RULES:\n"
                f"1. Divide the response into two clear sections: '☀️ AM Morning Routine' and '🌙 PM Evening Routine'.\n"
                f"2. Number each step chronologically (e.g., Step 1: Cleanser, Step 2: Toner...).\n"
                f"3. Include the exact Product Name and Brand.\n"
                f"4. Provide a 1-sentence explanation of why that specific product addresses their skin type/concern.\n"
                f"5. Provide the clickable video link for each product (e.g., [Watch Video Review](url))."
            )

            try:
                routine_response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a professional K-Beauty aesthetician. You create structured skincare routines using ONLY products supplied in the user's catalog list."
                        },
                        {"role": "user", "content": quiz_prompt}
                    ]
                )
                
                st.success("Your Personalized AM/PM Routine is Ready!")
                st.markdown(routine_response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error generating routine: {e}")
