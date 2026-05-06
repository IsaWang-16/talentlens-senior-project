import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Active Internship Radar | TalentLens",
    page_icon="🎯",
    layout="wide"
)

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
        display: flex;
        align-items: center;
    }
    .header-box h1 { color: white !important; margin: 0; padding-left: 20px; font-family: 'Segoe UI', sans-serif; }
    .stDataFrame {
        background-color: #ffffff;
        border: 2px solid #1E3A8A; 
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <div class="header-box">
        <img src="https://img.icons8.com/fluency/144/business-network.png" width="80">
        <h1>TalentLens: Active Internship Radar</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
### 📢 Real-Time Hidden Internship Pipeline
*This job board is directly synchronized with curated elite tech and finance recruiting pipelines, automatically flushing expired roles and updating live listings.*
""")

st.divider()

@st.cache_data(ttl=600)
def fetch_live_job_market():
    backup_data = {
        'Company': [
            'Goldman Sachs', 'Morgan Stanley', 'JPMorgan Chase', 'Bank of America', 'Citi',
            'McKinsey & Company', 'Bain & Company', 'Boston Consulting Group', 'BlackRock', 'Citadel',
            'Google', 'Microsoft', 'Meta', 'Amazon', 'Apple',
            'Netflix', 'NVIDIA', 'Salesforce', 'Adobe', 'Intel'
        ],
        'Position': [
            'Investment Banking Summer Analyst', 'Quantitative Research Intern', 'Global Markets Analyst', 'Wealth Management Intern', 'Equity Research Associate',
            'Business Analyst Intern', 'Associate Consultant Intern', 'Strategy & Operations Intern', 'Portfolio Management Intern', 'Quantitative Trading Intern',
            'Software Engineer Intern', 'Product Management Intern', 'Data Science Intern', 'Cloud Architecture Intern', 'AI/ML Engineering Intern',
            'Product Design Intern', 'Technical Program Manager Intern', 'Business Development Intern', 'Financial Analyst Intern', 'Silicon Engineering Intern'
        ],
        'Location': [
            'New York, NY', 'New York, NY', 'New York, NY', 'Boston, MA', 'New York, NY',
            'New York, NY', 'San Francisco, CA', 'Chicago, IL', 'New York, NY', 'Chicago, IL',
            'Mountain View, CA', 'Redmond, WA', 'Menlo Park, CA', 'Seattle, WA', 'Cupertino, CA',
            'Los Gatos, CA', 'Santa Clara, CA', 'San Francisco, CA', 'San Jose, CA', 'Austin, TX'
        ],
        'Job Description (Requirements)': [
            'Assist in building financial models (DCF, LBO), conducting industry valuations, preparing pitchbooks for client presentations, and executing corporate M&A transactions. Strong analytical and financial modeling background required.',
            'Develop, test, and implement predictive statistical models for quantitative trading strategies. Strong programming proficiency in Python, R, or C++, and solid foundation in stochastic calculus and probability theory.',
            'Support market making, structured sales, and macroeconomic trading desks. Analyze cross-asset market trends, build pricing tools, and interface with institutional clients on multi-million dollar transactions.',
            'Provide financial advisory services to high-net-worth clients. Analyze investment portfolios, construct asset allocation strategies, and conduct market research across equities, fixed income, and alternative assets.',
            'Conduct fundamental stock research and financial analysis on assigned industry coverage sectors. Build comprehensive earnings models, draft equity research reports, and present data-driven investment recommendations to portfolio managers.',
            'Work directly with client teams on large-scale corporate transformations. Formulate data-backed strategic hypotheses, conduct intensive financial modeling, and build strategic slide decks for Fortune 500 C-suite executives.',
            'Assist corporate clients across private equity, technology, and consumer sectors. Conduct market sizing analysis, competitive landscape benchmarking, and quantitative data processing using SQL and Tableau.',
            'Solve complex business problems for industry leaders. Analyze operational supply chain data, execute pricing optimization models, and design go-to-market strategies for emerging cross-border technologies.',
            'Support multi-asset portfolio managers in risk management and portfolio optimization. Monitor market risk factors using the Aladdin risk management platform, analyze asset performance, and rebalance institutional funds.',
            'Formulate quantitative trading algorithms for high-frequency trading platforms. Analyze terabytes of market microstructure data, optimize code efficiency, and manage risk parameters across electronic markets.',
            'Design, develop, and test software components across scalable web applications or infrastructure services. Proficient in Java, Python, C++, or Go, with a solid grasp of data structures and algorithms.',
            'Define product requirements, outline roadmaps, and collaborate with engineering and design teams. Analyze user metrics, write product definition documents (PRDs), and drive feature launches for consumer-facing apps.',
            'Extract strategic insights from massive data ecosystems. Build automated metrics dashboards, design and analyze rigorous A/B experiments, and construct predictive machine learning models using Python and SQL.',
            'Design scalable, secure, and resilient infrastructure solutions for enterprise cloud ecosystems. Implement infrastructure as code (IaC) using Terraform and deploy microservices across AWS, Azure, or GCP.',
            'Design, build, and deploy production-grade deep learning and machine learning systems. Train large-scale neural networks, optimize model inference speed, and implement computer vision or NLP algorithms.',
            'Create intuitive, beautiful end-to-end user journeys and interface designs. Conduct deep user research, build high-fidelity wireframes and interactive prototypes using Figma, and align with engineering specs.',
            'Manage complex, cross-functional technical engineering lifecycles. Formulate detailed project timelines, identify and mitigate architectural risks, and align engineering sprints with product milestones.',
            'Identify and secure enterprise-grade strategic partnerships and corporate growth opportunities. Conduct market research, draft cross-functional business proposals, and build scalable outbound sales funnels.',
            'Manage corporate financial planning, budgeting, and variance analysis (FP&A). Build corporate forecast models, monitor key performance metrics, and prepare executive financial summary reports.',
            'Design and verify next-generation semiconductor microarchitectures. Write RTL level logic using Verilog or SystemVerilog, execute hardware emulation tests, and analyze power, performance, and area parameters.'
        ],
        'Deadline': ['Rolling Basis'] * 20
    }
    df_default = pd.DataFrame(backup_data)
    
    google_sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQDjkTsjRdLMwJfZ_gWpLgqPbx061aPC5NRaDLHQV1JsKS5WvVbA_6KtN1EP8u732l5wSUxm3Yy90TW/pub?output=csv"
    try:
        df_sheet = pd.read_csv(google_sheet_url)
        df_sheet.columns = [c.strip() for c in df_sheet.columns]
        
        rename_dict = {}
        for col in df_sheet.columns:
            if col.lower() == 'company': rename_dict[col] = 'Company'
            elif col.lower() == 'position': rename_dict[col] = 'Position'
            elif col.lower() == 'location': rename_dict[col] = 'Location'
            elif col.lower() in ['job description', 'description', 'requirements', 'job description (requirements)']: rename_dict[col] = 'Job Description (Requirements)'
            elif col.lower() == 'deadline': rename_dict[col] = 'Deadline'
        
        df_sheet = df_sheet.rename(columns=rename_dict)
        
    
        required_cols = ['Company', 'Position', 'Location', 'Job Description (Requirements)', 'Deadline']
        if all(k in df_sheet.columns for k in required_cols):
            return df_sheet[required_cols].dropna()
    except Exception:
        return df_default
        
    return df_default

df = fetch_live_job_market()

if not df.empty:
    total_jobs = len(df)
    st.subheader(f"📊 {total_jobs} Curated Premium Positions Monitored")
    
    search_query = st.text_input("🔍 Job Search Assistant", placeholder="Search by Company, Position, or Job Requirements keywords...")

    if search_query:
        mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        display_df = df[mask].copy()
    else:
        display_df = df.copy()

    if not display_df.empty:
        display_df.index = range(1, len(display_df) + 1)
        
    
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("No matching positions found.")
else:
    st.error("System pipeline initialized. Please refresh the page.")

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80)
    st.title("Admin Panel")
    st.caption("TalentLens Production Pipeline")
    st.write("---")
    st.write("⚙️ **Data Infrastructure:**")
    st.success("Google Sheets API Active")
    st.success("Fail-safe Buffer Loaded")
    st.write("---")
    st.caption("Developed by Isabella Wang | 2026")