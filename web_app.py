import os
import json
import streamlit as st
from openai import OpenAI

# 1. PAGE SETUP
st.set_page_config(page_title="K-Beauty Skincare Wiki", layout="wide")

# 2. INJECT GOOGLE STITCH CSS & DESIGN TOKENS
st.markdown("""
<style>
/* Import Google Fonts from Stitch */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

/* Base App Styling */
.stApp {
    background-color: #FAF7F2 !important;
    color: #2C2420 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Force Text Colors across all HTML elements */
h1, h2, h3, h4, h5, h6, p, label, div, summary, caption {
    color: #2C2420 !important;
}

/* Editorial Serif Typography */
h1, h2, h3 {
    font-family: 'Cormorant Garamond', serif !important;
    font-weight: 500 !important;
    letter-spacing: -0.01em;
}

h1 {
    font-size: 2.75rem !important;
    color: #2C2420 !important;
}

/* Header Banner Navigation Bar (#48111B Burgundy) */
div[data-baseweb="tab-list"] {
    background-color: #48111B !important;
    padding: 10px 24px !important;
    border-radius: 6px !important;
    gap: 32px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08) !important;
}

button[data-baseweb="tab"] {
    background-color: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 8px 12px !important;
}

button[data-baseweb="tab"] p, button[data-baseweb="tab"] span {
    color: rgba(224, 207, 194, 0.8) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 400 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.02em;
}

button[aria-selected="true"] {
    border-bottom: 2px solid #E2C7A9 !important;
}

button[aria-selected="true"] p, button[aria-selected="true"] span {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* Product Cards & Expanders */
div[data-testid="stExpander"] {
    background-color: #FAF7F2 !important;
    border-radius: 12px !important;
    border: 1px solid #E3D9CC !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02) !important;
    margin-bottom: 14px;
}

div[data-testid="stExpander"] summary p {
    color: #2C2420 !important;
    font-weight: 500 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.25rem !important;
}

div[data-testid="stExpander"] summary svg {
    fill: #827468 !important;
}

/* Search Bar & Inputs */
input, textarea {
    background-color: #FAF7F2 !important;
    color: #2C2420 !important;
    border-radius: 6px !important;
    border: 1px solid #D5C7B8 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 12px 16px !important;
}

input:focus, textarea:focus {
    border-color: #48111B !important;
    box-shadow: 0 0 0 1px #48111B !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    background-color: #EFE8DE !important;
    color: #4A3E34 !important;
    border-radius: 6px !important;
    border: 1px solid #DACDC0 !important;
}

/* Dropdown Menu Options */
body div[data-baseweb="popover"],
body div[data-baseweb="popover"] *,
body [data-baseweb="menu"],
body [data-baseweb="menu"] * {
    background-color: #FAF7F2 !important;
    color: #2C2420 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

body [data-baseweb="option"]:hover,
body [data-baseweb="option"]:hover * {
    background-color: #48111B !important;
    color: #FFFFFF !important;
}

/* Primary Action Buttons */
.stButton>button {
    background-color: #48111B !important;
    color: #FAF7F2 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 12px 24px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
}

.stButton>button p, .stButton>button span {
    color: #FAF7F2 !important;
}

.stButton>button:hover {
    background-color: #380A12 !important;
    transform: translateY(-1px);
}

/* Chat Bubbles */
div[data-testid="stChatMessage"] {
    background-color: #F5EFE6 !important;
    border: 1px solid #E4D9CC !important;
    border-radius: 12px !important;
    color: #2C2420 !important;
}

/* Custom Stitch Tag Badges */
.skin-type-tag {
    display: inline-block;
    background-color: #EBE3D8;
    color: #54483E;
    font-size: 0.75rem;
    padding: 4px 12px;
    border-radius: 6px;
    font-weight: 500;
    margin-bottom: 12px;
}

.pro-icon {
    color: #5D6F41;
    font-weight: bold;
    margin-right: 8px;
}

.con-icon {
    color: #786C62;
    font-weight: bold;
    margin-right: 8px;
}

/* Product Card Images */
img {
    border-radius: 8px;
    border: 1px solid #E2D6C6;
    object-fit: cover;
}
</style>
""", unsafe_allow_html=True)

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
                        "description": "Keywords such as product name, brand, skin type, or category."
                    }
                },
                "required": ["query"]
            }
        }
    }
]

# 6. STREAMLIT NAVIGATION TABS
tab1, tab2, tab3 = st.tabs(["Skincare Directory", "AI Assistant", "Routine Quiz"])

# --- TAB 1: WIKI DIRECTORY ---
with tab1:
    st.markdown("<h1 style='text-align: center; margin-bottom: 24px;'>Skincare Directory</h1>", unsafe_allow_html=True)
    
    # Search Input
    search_term = st.text_input("", placeholder="Search products by name, brand, or ingredient", label_visibility="collapsed")
    
    # Filter Row (Category & Skin Type)
    f_col1, f_col2 = st.columns([3, 1])
    with f_col1:
        selected_category = st.pills(
            "Category",
            ["All", "Sunscreen", "Toner", "Essence", "Serum", "Eye Cream", "Moisturizer"],
            default="All",
            label_visibility="collapsed"
        )
    with f_col2:
        selected_skin_type = st.selectbox(
            "Skin Type Filter",
            ["All Skin Types", "Dry", "Oily", "Sensitive", "Combination", "Normal"],
            label_visibility="collapsed"
        )

    # Filter Database Logic
    filtered_db = skincare_db
    if search_term:
        filtered_db = [
            item for item in filtered_db 
            if search_term.lower() in item['name'].lower() 
            or search_term.lower() in item['brand'].lower()
            or search_term.lower() in item['category'].lower()
            or search_term.lower() in item['skin_sheet'].lower()
        ]

    if selected_category and selected_category != "All":
        filtered_db = [item for item in filtered_db if selected_category.lower() in item['category'].lower()]

    if selected_skin_type and selected_skin_type != "All Skin Types":
        filtered_db = [item for item in filtered_db if any(selected_skin_type.lower() in st_type.lower() for st_type in item['skin_type'])]

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Product Cards
    for item in filtered_db:
        with st.expander(f"{item['brand']} - {item['name']}"):
            img_col, text_col = st.columns([5, 7])
            
            with img_col:
                if item.get('image_url'):
                    st.image(item['image_url'], use_container_width=True)
            
            with text_col:
                st.markdown(f"## {item['name']}")
                st.markdown(f"<span class='skin-type-tag'>Skin Types: {', '.join(item['skin_type'])}</span>", unsafe_allow_html=True)
                st.markdown(f"<p style='color: #3E332C; font-size: 0.95rem;'>{item['skin_sheet']}</p>", unsafe_allow_html=True)
                
                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    st.markdown("**Pros:**")
                    for pro in item['pros']:
                        st.markdown(f"<span class='pro-icon'>+</span> {pro}", unsafe_allow_html=True)
                with p_col2:
                    st.markdown("**Cons:**")
                    for con in item['cons']:
                        st.markdown(f"<span class='con-icon'>—</span> {con}", unsafe_allow_html=True)
                
                # Minimalist Text Link without Embedded Player or Thumbnail
                if item.get('video_url'):
                    st.markdown(
                        f"""
                        <div style="margin-top: 16px;">
                            <a href="{item['video_url']}" target="_blank" style="color: #48111B; font-weight: 600; text-decoration: underline; font-size: 0.9rem; letter-spacing: 0.02em;">
                                Watch Video Review →
                            </a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# --- TAB 2: CHATBOT INTERFACE ---
with tab2:
    st.markdown("<h1 style='text-align: center;'>Ask Your AI Skincare Assistant</h1>", unsafe_allow_html=True)
    st.caption("Powered by DeepSeek AI — Ask for recommendations, Skin Sheets, or video review links.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Type your question here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing request..."):
                system_instruction = (
                    "You are an expert K-Beauty assistant powered by DeepSeek.\n"
                    "1. Always call `search_skincare_db` to look up product details from the database.\n"
                    "2. ALWAYS include the YouTube try-out video link as an explicit Markdown link in your final response."
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
                            
                            st.info(f"Searching database for: `{fn_args}`")
                            
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
    st.markdown("<h1 style='text-align: center;'>Interactive Skin Quiz & Routine Generator</h1>", unsafe_allow_html=True)
    st.caption("Answer three questions to receive a personalized K-Beauty regimen tailored to your skin's needs.")

    col1, col2, col3 = st.columns(3)
    with col1:
        skin_type = st.selectbox(
            "Skin Type",
            ["Dry", "Oily", "Combination", "Sensitive", "Dehydrated", "Normal"]
        )
    with col2:
        concern = st.selectbox(
            "Primary Concern",
            ["Acne & Breakouts", "Anti-Aging & Fine Lines", "Redness & Sensitivity", "Pores & Rough Texture", "Barrier Repair & Dryness"]
        )
    with col3:
        routine_style = st.selectbox(
            "Routine Complexity",
            ["Minimalist Routine (2-3 Core Steps)", "Balanced Routine (4-5 Steps)", "Full Glass-Skin Routine (6+ Steps)"]
        )

    if st.button("Generate My Custom Routine", use_container_width=True):
        with st.spinner("Building your custom routine..."):
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
                f"1. Divide the response into two clear sections: 'AM Morning Routine' and 'PM Evening Routine'.\n"
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
                
                st.success("Your Personalized AM/PM Routine is Ready")
                st.markdown(routine_response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error generating routine: {e}")
