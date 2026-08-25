import os
import json
import streamlit as st
from openai import OpenAI

# 1. PAGE SETUP
st.set_page_config(page_title="Skincare Directory", layout="wide", initial_sidebar_state="collapsed")

# 2. INJECT EXACT STITCH / AI STUDIO CSS
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Remove Streamlit Default Header and Paddings */
header[data-testid="stHeader"] {
    display: none !important;
}

.main .block-container {
    padding-top: 0rem !important;
    padding-bottom: 3rem !important;
    max-width: 950px !important;
}

/* App Canvas Styling (#FAF7F2 Warm Cream Background) */
.stApp {
    background-color: #FAF7F2 !important;
    color: #2C2420 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Force High Contrast Text Color Across General Elements */
h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: #2C2420 !important;
}

/* Font Family Classes */
.font-serif {
    font-family: 'Cormorant Garamond', serif !important;
}
.font-sans {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Header Tab Buttons Styling */
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    background-color: transparent !important;
    border: none !important;
    color: rgba(224, 207, 194, 0.8) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 400 !important;
    border-radius: 0px !important;
    border-bottom: 2px solid transparent !important;
    padding: 6px 16px !important;
}

div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
    color: #FFFFFF !important;
    border-bottom: 2px solid rgba(224, 207, 194, 0.4) !important;
}

/* Form Inputs & Selectboxes */
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
    background-color: #FAF7F2 !important;
    color: #2C2420 !important;
    border-radius: 6px !important;
    border: 1px solid #8C7E72 !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.15rem !important;
}

/* Custom Product Card Container */
.product-card {
    background-color: #FAF7F2;
    border: 1px solid #E3D9CC;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 16px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    transition: all 0.2s ease;
}

.product-card-expanded {
    padding: 24px 28px;
}

/* Skin Type Pill */
.skin-type-badge {
    display: inline-block;
    background-color: #EBE3D8;
    color: #54483E;
    font-size: 0.75rem;
    padding: 4px 12px;
    border-radius: 6px;
    font-weight: 500;
    letter-spacing: 0.02em;
    margin-top: 8px;
    margin-bottom: 12px;
}

/* Pros and Cons Styling */
.pro-item {
    color: #3E332C;
    font-size: 0.875rem;
    display: flex;
    align-items: flex-start;
    margin-bottom: 6px;
}
.pro-icon {
    color: #5D6F41;
    font-weight: 700;
    margin-right: 8px;
    font-size: 1rem;
}

.con-item {
    color: #3E332C;
    font-size: 0.875rem;
    display: flex;
    align-items: flex-start;
    margin-bottom: 6px;
}
.con-icon {
    color: #786C62;
    font-weight: 700;
    margin-right: 8px;
    font-size: 1rem;
}

/* Key Actives Badges */
.active-tag {
    background-color: #F0E9DF;
    color: #52463C;
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 3px;
    margin-right: 6px;
    margin-bottom: 4px;
    display: inline-block;
}

/* Chat Message Bubbles */
.chat-bubble-user {
    background-color: #ECE5DC;
    color: #2C2420;
    font-size: 0.95rem;
    padding: 12px 20px;
    border-radius: 16px 16px 2px 16px;
    max-width: 80%;
    margin-left: auto;
    margin-bottom: 12px;
    line-height: 1.6;
}

.chat-bubble-assistant {
    background-color: #FFFFFF;
    border: 1px solid #E6DDD1;
    color: #2C2420;
    font-size: 0.95rem;
    padding: 16px 24px;
    border-radius: 16px 16px 16px 2px;
    max-width: 90%;
    margin-right: auto;
    margin-bottom: 12px;
    line-height: 1.6;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

/* PRIMARY ACTION BUTTON (#48111B Solid Fill) */
button[data-testid="stBaseButton-primary"],
div.stButton > button[kind="primary"] {
    background-color: #48111B !important;
    color: #FAF7F2 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 14px 32px !important;
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.25rem !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 12px rgba(72, 17, 27, 0.2) !important;
}

/* FORCE BUTTON TEXT TO MATCH BACKGROUND (#FAF7F2) */
button[data-testid="stBaseButton-primary"] *,
button[data-testid="stBaseButton-primary"] p,
button[data-testid="stBaseButton-primary"] span,
button[data-testid="stBaseButton-primary"] div,
div.stButton > button[kind="primary"] *,
div.stButton > button[kind="primary"] p,
div.stButton > button[kind="primary"] span,
div.stButton > button[kind="primary"] div {
    color: #FAF7F2 !important;
    font-weight: 600 !important;
}

button[data-testid="stBaseButton-primary"]:hover,
div.stButton > button[kind="primary"]:hover {
    background-color: #380A12 !important;
    transform: translateY(-1px);
}

/* Quiz Labels */
.quiz-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    color: #736559;
    margin-bottom: 6px;
    text-transform: uppercase;
}

/* Dynamic Product Image Styling */
div[data-testid="stImage"] img, img {
    width: 100% !important;
    height: auto !important;
    aspect-ratio: 1 / 1 !important;
    object-fit: cover !important;
    object-position: center !important;
    border-radius: 8px !important;
    border: 1px solid #E2D6C6 !important;
    display: block !important;
}

/* Custom Footer */
.custom-footer {
    border-top: 1px solid #E4D9CC;
    margin-top: 80px;
    padding: 24px 0;
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    color: #807267;
}
</style>
""", unsafe_allow_html=True)

# 3. API KEY DETECTION
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

# 5. INITIALIZE SESSION STATE
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "directory"

if "expanded_ids" not in st.session_state:
    st.session_state.expanded_ids = {"boj-relief-sun": True}

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "user", "content": "What are you as my AI skincare assistant?"},
        {"role": "assistant", "content": "I am your dedicated luxury K-Beauty and dermatological skincare advisor. I can analyze your skin type, recommend the finest cult-favorite Korean formulations, explain complex ingredient synergies (like Centella, Snail Mucin, Niacinamide, and Ceramides), and design step-by-step morning and evening routines."},
        {"role": "user", "content": "What is the beauty of K-Skincare sunscreens like Beauty of Joseon Relief Sun?"},
        {"role": "assistant", "content": "Lightweight, creamy chemical sunscreen that hydrates deeply without feeling sticky or leaving a white cast. Gives a soft, glowing finish with 30% Rice Extract and Grain Probiotics.\n\n• Deeply hydrating with skin-barrier prebiotics\n• Sits invisibly under makeup without pilling\n• Note: Can feel slightly too dewy on extremely oily skin."}
    ]

# 6. TOOL SCHEMA & SEARCH LOGIC
def search_skincare_db(query: str) -> str:
    if not skincare_db:
        return "Skincare database is empty."
    query_lower = query.lower()
    matched_products = []
    for item in skincare_db:
        searchable_text = f"{item.get('name', '')} {item.get('brand', '')} {item.get('category', '')} {' '.join(item.get('skin_type', []))} {item.get('skin_sheet', '')}".lower()
        if any(term in searchable_text for term in query_lower.split()):
            matched_products.append(item)

    if not matched_products:
        return f"No products found for query: '{query}'."

    results = []
    for p in matched_products:
        results.append(
            f"Product: {p.get('name')} by {p.get('brand')}\n"
            f"Category: {p.get('category')}\n"
            f"Best for Skin Types: {', '.join(p.get('skin_type', []))}\n"
            f"Skin Sheet: {p.get('skin_sheet')}\n"
            f"Pros: {', '.join(p.get('pros', []))}\n"
            f"Cons: {', '.join(p.get('cons', []))}\n"
            f"Try-out Video: {p.get('video_url', '')}\n"
        )
    return "\n---\n".join(results)

AVAILABLE_TOOLS = {"search_skincare_db": search_skincare_db}
tools_schema = [{
    "type": "function",
    "function": {
        "name": "search_skincare_db",
        "description": "Search local Korean Skincare database.",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"]
        }
    }
}]

# 7. HEADER NAVIGATION BAR
nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])

with nav_col1:
    if st.button("Skincare Directory", key="nav_dir", type="secondary", use_container_width=True):
        st.session_state.active_tab = "directory"
        st.rerun()

with nav_col2:
    if st.button("AI Assistant", key="nav_ai", type="secondary", use_container_width=True):
        st.session_state.active_tab = "ai-assistant"
        st.rerun()

with nav_col3:
    if st.button("Routine Quiz", key="nav_quiz", type="secondary", use_container_width=True):
        st.session_state.active_tab = "quiz"
        st.rerun()

st.markdown("<hr style='border: 0; border-top: 1px solid #E3D9CC; margin-top: 0px; margin-bottom: 24px;'>", unsafe_allow_html=True)


# ==========================================
# TAB 1: DIRECTORY VIEW
# ==========================================
if st.session_state.active_tab == "directory":
    st.markdown("<h1 class='font-serif' style='text-align: center; margin-bottom: 32px;'>Skincare Directory</h1>", unsafe_allow_html=True)
    
    # Search Input
    search_query = st.text_input("Search", placeholder="Search products by name, brand, or ingredient", label_visibility="collapsed")
    
    # Quick Filter Bar
    col_cat, col_skin = st.columns([3, 1])
    with col_cat:
        selected_category = st.pills(
            "Category",
            ["All", "Sunscreen", "Toner", "Essence", "Serum", "Moisturizer"],
            default="All",
            label_visibility="collapsed"
        )
    with col_skin:
        selected_skin_type = st.selectbox(
            "Skin Type",
            ["All Skin Types", "Dry", "Oily", "Sensitive", "Combination", "Normal"],
            label_visibility="collapsed"
        )

    # Filtering Logic
    filtered_products = skincare_db
    if search_query:
        filtered_products = [
            item for item in filtered_products 
            if search_query.lower() in item.get('name', '').lower() 
            or search_query.lower() in item.get('brand', '').lower()
            or search_query.lower() in item.get('skin_sheet', '').lower()
        ]

    if selected_category and selected_category != "All":
        filtered_products = [item for item in filtered_products if selected_category.lower() in item.get('category', '').lower()]

    if selected_skin_type and selected_skin_type != "All Skin Types":
        filtered_products = [item for item in filtered_products if any(selected_skin_type.lower() in st_type.lower() for st_type in item.get('skin_type', []))]

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Product Cards
    for idx, item in enumerate(filtered_products):
        p_id = item.get("id", f"prod-{idx}")
        is_expanded = st.session_state.expanded_ids.get(p_id, False)

        if not is_expanded:
            card_col1, card_col2 = st.columns([10, 1])
            with card_col1:
                st.markdown(f"<div class='font-serif' style='font-size: 1.25rem; color: #2C2420; padding-top: 6px;'>{item.get('brand', '')} - {item.get('name', '')} ({item.get('category', '')})</div>", unsafe_allow_html=True)
            with card_col2:
                if st.button("▼", key=f"expand_{p_id}", type="secondary"):
                    st.session_state.expanded_ids[p_id] = True
                    st.rerun()
            st.markdown("<hr style='border-top: 1px solid #E3D9CC; margin: 8px 0 16px 0;'>", unsafe_allow_html=True)

        else:
            st.markdown("<div class='product-card product-card-expanded'>", unsafe_allow_html=True)
            img_col, details_col = st.columns([5, 7])
            
            with img_col:
                if item.get('image_url'):
                    st.image(item['image_url'], use_container_width=True)
            
            with details_col:
                st.markdown(f"<h2 class='font-serif' style='font-size: 1.6rem; margin-bottom: 4px;'>{item.get('brand', '')} - {item.get('name', '')}</h2>", unsafe_allow_html=True)
                
                skin_types_str = ", ".join(item.get('skin_type', []))
                st.markdown(f"<span class='skin-type-badge'>Skin Types: {skin_types_str}</span>", unsafe_allow_html=True)
                
                st.markdown(f"<p style='color: #3E332C; font-size: 0.95rem; line-height: 1.6; margin-bottom: 16px;'>{item.get('skin_sheet', '')}</p>", unsafe_allow_html=True)
                
                # Pros & Cons
                p_col1, p_col2 = st.columns(2)
                with p_col1:
                    st.markdown("<strong style='font-size: 0.85rem;'>Pros:</strong>", unsafe_allow_html=True)
                    for pro in item.get('pros', []):
                        st.markdown(f"<div class='pro-item'><span class='pro-icon'>+</span>{pro}</div>", unsafe_allow_html=True)
                with p_col2:
                    st.markdown("<strong style='font-size: 0.85rem;'>Cons:</strong>", unsafe_allow_html=True)
                    for con in item.get('cons', []):
                        st.markdown(f"<div class='con-item'><span class='con-icon'>—</span>{con}</div>", unsafe_allow_html=True)
                
                # Key Actives
                if item.get('key_actives'):
                    st.markdown("<div style='margin-top: 12px; border-top: 1px solid #EAE1D4; padding-top: 8px;'>", unsafe_allow_html=True)
                    st.markdown("<span style='font-size: 0.75rem; color: #7D7065; font-weight: 600; margin-right: 6px;'>Key Actives:</span>", unsafe_allow_html=True)
                    actives_html = "".join([f"<span class='active-tag'>{act}</span>" for act in item.get('key_actives', [])])
                    st.markdown(actives_html, unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                # Minimalist Video Link
                if item.get('video_url'):
                    st.markdown(f"<div style='margin-top: 12px;'><a href='{item['video_url']}' target='_blank' style='color: #48111B; font-weight: 600; text-decoration: underline; font-size: 0.85rem;'>Watch Video Review →</a></div>", unsafe_allow_html=True)

                # Ask AI Assistant Button
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"Ask AI Assistant about this product", key=f"ask_{p_id}", type="secondary"):
                    st.session_state.messages.append({"role": "user", "content": f"Can you give me a breakdown of {item.get('name')} by {item.get('brand')}?"})
                    st.session_state.active_tab = "ai-assistant"
                    st.rerun()

            if st.button("▲ Collapse Details", key=f"collapse_{p_id}", type="secondary", use_container_width=True):
                st.session_state.expanded_ids[p_id] = False
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)


# ==========================================
# TAB 2: AI ASSISTANT VIEW
# ==========================================
elif st.session_state.active_tab == "ai-assistant":
    st.markdown("<h1 class='font-serif' style='text-align: center; margin-bottom: 24px;'>Ask Your AI Skincare Assistant</h1>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #807267; font-size: 0.85rem; margin-bottom: 12px;'>Select a quick query or type below:</p>", unsafe_allow_html=True)
    
    q_col1, q_col2 = st.columns(2)
    with q_col1:
        if st.button("Best sunscreen for oily acne-prone skin?", key="qp1", type="secondary", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "Best sunscreen for oily acne-prone skin?"})
            st.rerun()
        if st.button("What should I use for redness and damaged barrier?", key="qp2", type="secondary", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "What should I use for redness and damaged barrier?"})
            st.rerun()
    with q_col2:
        if st.button("How do I layer Snail Mucin and Niacinamide?", key="qp3", type="secondary", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "How do I layer Snail Mucin and Niacinamide?"})
            st.rerun()
        if st.button("How to build a Korean Glass Skin morning routine?", key="qp4", type="secondary", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": "How to build a Korean Glass Skin morning routine?"})
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Render Chat Messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-assistant'>{msg['content']}</div>", unsafe_allow_html=True)

    # Multi-turn Execution Loop for DeepSeek Tools
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        with st.spinner("Consulting dermatological formulas..."):
            system_instruction = (
                "You are an expert K-Beauty assistant powered by DeepSeek.\n"
                "1. Always call `search_skincare_db` to look up product details from the database.\n"
                "2. ALWAYS include the YouTube try-out video link as an explicit Markdown link in your final response."
            )
            messages_payload = [{"role": "system", "content": system_instruction}]
            for m in st.session_state.messages:
                messages_payload.append({"role": m["role"], "content": m["content"]})

            turns = 0
            max_turns = 3
            reply_text = "I apologize, but I could not fulfill your request."

            try:
                while turns < max_turns:
                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=messages_payload,
                        tools=tools_schema
                    )
                    msg = response.choices[0].message
                    messages_payload.append(msg)

                    if msg.tool_calls:
                        for tool_call in msg.tool_calls:
                            fn_name = tool_call.function.name
                            fn_args = json.loads(tool_call.function.arguments or "{}")
                            
                            if fn_name in AVAILABLE_TOOLS:
                                tool_out = AVAILABLE_TOOLS[fn_name](**fn_args)
                            else:
                                tool_out = "Tool not found."

                            messages_payload.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": str(tool_out)
                            })
                        turns += 1
                    else:
                        reply_text = msg.content
                        break

                st.session_state.messages.append({"role": "assistant", "content": reply_text})
                st.rerun()
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"I am unable to reach the skincare database right now. ({e})"})
                st.rerun()

    # Chat Input Bar
    chat_input_val = st.chat_input("Type your question here...")
    if chat_input_val:
        st.session_state.messages.append({"role": "user", "content": chat_input_val})
        st.rerun()

    # Reset Chat
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Reset Chat Conversation", type="secondary"):
        st.session_state.messages = []
        st.rerun()


# ==========================================
# TAB 3: ROUTINE QUIZ VIEW
# ==========================================
elif st.session_state.active_tab == "quiz":
    st.markdown("<h1 class='font-serif' style='text-align: center; margin-bottom: 8px;'>Interactive Skin Quiz & Routine Generator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #52463D; font-size: 1.05rem; margin-bottom: 32px;'>Answer three questions to receive a personalized K-Beauty regimen tailored to your skin's needs.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='quiz-label'>SKIN TYPE</div>", unsafe_allow_html=True)
        quiz_skin = st.selectbox("Skin Type", ["Dry", "Oily", "Combination", "Normal", "Sensitive", "Very Dry & Dehydrated", "Acne-Prone"], label_visibility="collapsed")
    with col2:
        st.markdown("<div class='quiz-label'>PRIMARY CONCERN</div>", unsafe_allow_html=True)
        quiz_concern = st.selectbox("Primary Concern", ["Dehydration & Dryness", "Acne & Blemishes", "Hyperpigmentation & Dark Spots", "Redness & Barrier Repair", "Anti-Aging & Fine Lines", "Dullness & Lack of Glow"], label_visibility="collapsed")
    with col3:
        st.markdown("<div class='quiz-label'>ROUTINE COMPLEXITY</div>", unsafe_allow_html=True)
        quiz_complexity = st.selectbox("Routine Complexity", ["Minimalist (3-Step)", "Balanced (5-Step)", "Full K-Beauty Glass Skin (7-10 Step)"], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    
    b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
    with b_col2:
        generate_clicked = st.button("Generate My Custom Routine", type="primary", use_container_width=True)

    if generate_clicked:
        with st.spinner("Analyzing K-Beauty Synergies..."):
            catalog_summary = "\n".join([
                f"- Name: {item.get('name')} | Brand: {item.get('brand')} | Category: {item.get('category')} | Suitable for: {', '.join(item.get('skin_type', []))} | Summary: {item.get('skin_sheet')} | Video: {item.get('video_url')}"
                for item in skincare_db
            ])

            quiz_prompt = (
                f"Build a personalized AM and PM skincare routine for a user with:\n"
                f"- Skin Type: {quiz_skin}\n"
                f"- Primary Concern: {quiz_concern}\n"
                f"- Preferred Complexity: {quiz_complexity}\n\n"
                f"CATALOG PRODUCTS (MUST ONLY USE PRODUCTS FROM THIS LIST):\n{catalog_summary}\n\n"
                f"STRICT FORMATTING:\n"
                f"1. Divide into 'AM Morning Routine' and 'PM Evening Routine'.\n"
                f"2. Number each step chronologically.\n"
                f"3. Include Product Name and Brand.\n"
                f"4. Provide a 1-sentence explanation of why it addresses their skin.\n"
                f"5. Include clickable video link where available."
            )

            try:
                routine_response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": "You are a professional K-Beauty aesthetician."},
                        {"role": "user", "content": quiz_prompt}
                    ]
                )
                st.markdown("<hr style='border-top: 1px solid #E3D9CC; margin: 32px 0;'>", unsafe_allow_html=True)
                st.markdown("<h2 class='font-serif' style='text-align: center;'>Your Custom K-Beauty Prescription</h2><br>", unsafe_allow_html=True)
                st.markdown(routine_response.choices[0].message.content)
            except Exception as e:
                st.error(f"Error generating routine: {e}")

# --- FOOTER ---
st.markdown("""
<div class="custom-footer">
    <div>Skincare Directory & AI Assistant</div>
    <div>Curated K-Beauty formulations & personalized dermatological AI advice.</div>
</div>
""", unsafe_allow_html=True)
