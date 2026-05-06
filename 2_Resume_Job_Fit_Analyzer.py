import streamlit as st
from docx import Document
from openai import OpenAI
import json
import plotly.graph_objects as go
import urllib.parse

# --- 1. 页面配置 ---
st.set_page_config(page_title="TalentLens AI Pro", page_icon="🎯", layout="wide")

# --- 🎨 核心美化 CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #F0F7FF; }
    .header-box {
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .header-box h1 { color: white !important; margin: 0; }
    .feature-container {
        background-color: #ffffff;
        border: 2px solid #1E3A8A;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    .advice-card {
        background-color: #F0F7FF;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #1E3A8A;
        color: #333;
        line-height: 1.6;
    }
    .learning-link {
        display: inline-block;
        padding: 10px 20px;
        background-color: #1E3A8A;
        color: white !important;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        margin: 5px;
        font-size: 0.85rem;
        transition: 0.3s;
        box-shadow: 0 4px 6px rgba(30,58,138,0.15);
    }
    .learning-link:hover {
        background-color: #3B82F6;
        transform: translateY(-2px);
    }
    /* 评分拆解样式 */
    .score-breakdown {
        margin-top: 10px;
        font-size: 0.9rem;
        color: #555;
    }
    </style>
    """, unsafe_allow_html=True)

client = OpenAI(api_key='sk-394e6c6525c9436ab085290d76bb2c46', base_url="https://api.deepseek.com")

# --- 2. 核心功能：优化后的精英多语言 AI 逻辑 ---
def extract_and_match_logic(uploaded_file, user_intent, resume_lang):
    doc = Document(uploaded_file)
    full_text = "\n".join([p.text for p in doc.paragraphs])
    
    # 升级版高级 Prompt：强迫 AI 进行原文引用、对比改写、行动拆解，以及分数维度细化
    prompt = f"""
    You are an elite Senior Career Consultant specialized in premium tech and finance recruiting. 
    The uploaded resume is written in {resume_lang}. 
    Analyze this resume strictly against the target job requirements or JD provided here: "{user_intent}".
    
    CRITICAL REQUIREMENT: 
    Regardless of the input resume language, you MUST provide the entire analysis, reasons, gaps, and strategies in ENGLISH.
    
    Tasks:
    1. Calculate a match score (0-100).
    2. Provide a breakdown of the score: hard_skills_score (0-100) and soft_skills_score (0-100) to help users trust the grading system.
    3. Provide 5-dimension scores (0-10) for Radar Chart: Technical, Leadership, Communication, Analytics, Industry Knowledge.
    4. Identify exactly 3 missing skills or gaps.
    5. Provide 3 specific courses or learning resources and specify their platform (e.g., Coursera, Udemy, Wall Street Prep, or LinkedIn Learning).
    6. Provide a 'Positioning Tip' that is deeply personalized. Do NOT give generic advice. You MUST format the 'positioning_tip' exactly like this HTML structure:
       "<strong>[Original Resume Snippet]</strong>: \\"Quote a real, weak phrase or bullet point from the candidate's actual text here\\" <br>
        <strong>[Tailored Revision]</strong>: \\"Provide the rewritten, high-impact version using industry keywords from the target JD here\\" <br><br>
        <strong>🎯 Actionable Next Step</strong>: Provide one clear, immediate action item the student can do right now to bridge this gap."

    Resume Content: {full_text}

    Return ONLY JSON:
    {{
      "match_score": int,
      "hard_skills_score": int,
      "soft_skills_score": int,
      "reasoning": "summary of fit in English",
      "dimension_scores": [int, int, int, int, int],
      "gaps": ["gap 1 in English", "gap 2 in English", "gap 3 in English"],
      "positioning_tip": "The HTML formatted string combining Original Snippet, Tailored Revision, and Actionable Next Step as instructed above.",
      "learning_resources": [
        {{"name": "Course Name 1", "platform": "Wall Street Prep"}},
        {{"name": "Course Name 2", "platform": "Coursera"}},
        {{"name": "Course Name 3", "platform": "Udemy"}}
      ]
    }}
    """
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" },
        temperature=0
    )
    return json.loads(response.choices[0].message.content)

# 升级链接直达逻辑：如果是高频平台，直接链接到官方核心落地页，其余的使用智能聚合搜索
# 升级版：实现真正的 Deep Link Mapping（深层链接映射），直达具体课程的搜索与详情页
def get_smart_url(course_name, platform):
    platform_lower = platform.lower()
    # 将课程名称进行 URL 编码，防止空格和特殊字符导致链接失效
    encoded_name = urllib.parse.quote(course_name)
    
    if "wall street prep" in platform_lower:
        # 直达 Wall Street Prep 的站内课程搜索，精准定位金融认证
        return f"https://www.wallstreetprep.com/?s={encoded_name}"
        
    elif "coursera" in platform_lower:
        # 直达 Coursera 具体的课程搜索结果落地页，用户点开就能看到这门课的注册按钮
        return f"https://www.coursera.org/search?query={encoded_name}"
        
    elif "udemy" in platform_lower:
        # 直达 Udemy 具体的课程商品详情搜索页
        return f"https://www.udemy.com/courses/search/?q={encoded_name}"
        
    elif "linkedin" in platform_lower or "领英" in platform_lower:
        # 直达 LinkedIn Learning 的技能课程搜索详情页
        return f"https://www.linkedin.com/learning/search?keywords={encoded_name}"
    
    # 兜底：其余不常见的平台依然使用 Google 智能聚合搜索
    query = f"{course_name} {platform}"
    return f"https://www.google.com/search?q={urllib.parse.quote(query)}"

# --- 3. 页面大标题 ---
st.markdown("""
    <div class="header-box">
        <h1>🎯 TalentLens: Career Alignment Ecosystem</h1>
        <p style="opacity: 0.9; margin-top: 5px; font-size: 1.1rem;">AI-Powered Multi-language Resume Diagnosis & Precision Mapping</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. 主界面布局 ---
col_left, col_right = st.columns([1, 1.3], gap="large")

with col_left:
    st.markdown('<div class="feature-container">', unsafe_allow_html=True)
    st.subheader("📁 Candidate Input")
    
    resume_file = st.file_uploader("Upload Resume (DOCX)", type="docx")
    
    resume_lang = st.selectbox(
        "Resume Language",
        ["English", "Chinese (中文)", "Spanish", "French", "German", "Japanese", "Other"]
    )
    
    # 改进点 1：大文本框输入，允许粘贴完整的企业职位描述 (JD)
    intent = st.text_area(
        "Target Job Description / Role Requirements", 
        placeholder="Paste the job title or the full Job Description (JD) from the corporate career page here...",
        height=180
    )
    
    run_btn = st.button("Generate Full Analysis", use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if run_btn and resume_file and intent:
        with st.spinner(f"🚀 Analyzing compatibility and optimizing career positioning..."):
            data = extract_and_match_logic(resume_file, intent, resume_lang)
            score = data.get('match_score', 0)
            
            st.markdown('<div class="feature-container">', unsafe_allow_html=True)
            c1, c2 = st.columns([1, 1])
            with c1:
                st.metric("Overall Match Score", f"{score}%")
                
                # 改进点 2：拆解硬技能与软技能得分，建立算法透明度与系统信任
                hard_score = data.get('hard_skills_score', score)
                soft_score = data.get('soft_skills_score', score)
                st.markdown(f"""
                <div class="score-breakdown">
                    ⚙️ <strong>Hard Skills Match</strong>: {hard_score}% <br>
                    🤝 <strong>Soft Skills Match</strong>: {soft_score}%
                </div>
                """, unsafe_allow_html=True)
                
            with c2:
                if score >= 80: st.success("Strong Alignment")
                elif score >= 60: st.warning("Potential Fit")
                else: st.error("Gap Identified")
            
            categories = ['Technical', 'Leadership', 'Communication', 'Analytics', 'Industry Knowledge']
            fig = go.Figure(data=go.Scatterpolar(
                r=data.get('dimension_scores', [5]*5),
                theta=categories, fill='toself', fillcolor='rgba(30, 58, 138, 0.2)', line_color='#1E3A8A'
            ))
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), height=350, margin=dict(t=30, b=30), paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="feature-container">', unsafe_allow_html=True)
            st.subheader("🔍 Diagnostics & Learning Paths")
            cg1, cg2 = st.columns(2)
            with cg1:
                st.markdown("**Identified Gaps:**")
                for gap in data.get('gaps', []): st.write(f"🚩 {gap}")
            with cg2:
                st.markdown("**Recommended Courses (Clickable):**")
                for res in data.get('learning_resources', []):
                    name = res.get('name')
                    platform = res.get('platform')
                    # 改进点 3：一键直接导向平台详情页，缩短学习路径链路
                    url = get_smart_url(name, platform)
                    st.markdown(f'<a href="{url}" target="_blank" class="learning-link">🔗 {name} ({platform})</a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="feature-container">', unsafe_allow_html=True)
            st.subheader("💡 Positioning Strategy")
            # 改进点 4：前端无缝渲染带有原句引用、对比修改以及具体Action的卡片
            st.markdown(f'<div class="advice-card">{data.get("positioning_tip")}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👈 Upload your resume, select language, and paste the target role/JD to unlock the advanced alignment ecosystem.")

# 侧边栏
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Admin Panel")
    st.caption("Developed by Isabella Wang | TalentLens 2026")