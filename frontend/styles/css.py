def get_custom_css():
    """Return the SuperKart dashboard design system."""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --sk-bg: #0b1220;
        --sk-panel: #111c2e;
        --sk-panel-soft: #152238;
        --sk-border: rgba(148, 163, 184, .16);
        --sk-text: #edf3fb;
        --sk-muted: #91a2b8;
        --sk-cyan: #45d6c5;
        --sk-blue: #6c9cff;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }
    .stApp {
        background:
            radial-gradient(ellipse at 12% 0%, rgba(41, 112, 133, .18), transparent 34%),
            radial-gradient(ellipse at 92% 8%, rgba(72, 105, 181, .15), transparent 30%),
            var(--sk-bg);
        color: var(--sk-text);
    }
    [data-testid="stHeader"] {
        background: rgba(11, 18, 32, .78);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #101b2c 0%, #0d1727 100%);
        border-right: 1px solid var(--sk-border);
    }
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 1.4rem;
    }
    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, h4 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--sk-text) !important;
        letter-spacing: -.035em;
    }
    p, label, li, .stMarkdown {
        color: #d4deeb;
    }
    .sk-brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 5px 0 24px;
    }
    .sk-brand-mark {
        width: 42px;
        height: 42px;
        display: grid;
        place-items: center;
        border-radius: 13px;
        color: #071a20;
        font-size: 22px;
        font-weight: 900;
        background: linear-gradient(135deg, var(--sk-cyan), #86f0d5);
        box-shadow: 0 8px 28px rgba(69, 214, 197, .2);
    }
    .sk-brand-name {
        font: 800 18px 'Manrope', sans-serif;
        color: #f5f8fc;
        line-height: 1.1;
    }
    .sk-brand-caption {
        color: var(--sk-muted);
        font-size: 11px;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-top: 4px;
    }
    .sk-hero {
        position: relative;
        overflow: hidden;
        padding: 34px 36px;
        border: 1px solid rgba(118, 176, 202, .24);
        border-radius: 24px;
        background:
            radial-gradient(circle at 85% 15%, rgba(69, 214, 197, .18), transparent 28%),
            linear-gradient(115deg, rgba(20, 48, 67, .98), rgba(21, 36, 62, .96) 58%, rgba(29, 49, 79, .96));
        box-shadow: 0 18px 55px rgba(0, 0, 0, .18);
        margin-bottom: 26px;
    }
    .sk-eyebrow {
        color: var(--sk-cyan);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .17em;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .sk-hero h1 {
        font-size: clamp(30px, 4vw, 43px);
        line-height: 1.12;
        margin: 0 0 12px;
        max-width: 720px;
    }
    .sk-hero p {
        color: #b9c9dc;
        font-size: 15px;
        margin: 0;
        max-width: 650px;
    }
    .sk-hero-tag {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border: 1px solid rgba(69, 214, 197, .25);
        border-radius: 999px;
        color: #b9fff1;
        background: rgba(69, 214, 197, .08);
        font-size: 12px;
        margin-top: 22px;
    }
    .sk-section-kicker {
        color: var(--sk-cyan);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: .15em;
        text-transform: uppercase;
        margin: 25px 0 7px;
    }
    .sk-panel {
        background: linear-gradient(145deg, rgba(21, 34, 55, .94), rgba(15, 27, 44, .94));
        border: 1px solid var(--sk-border);
        border-radius: 18px;
        padding: 18px 20px;
    }
    .sk-muted {
        color: var(--sk-muted);
        font-size: 13px;
    }
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(21, 34, 55, .96), rgba(15, 27, 44, .96));
        border: 1px solid var(--sk-border);
        border-radius: 16px;
        padding: 17px 19px;
    }
    div[data-testid="stMetric"] label {
        color: var(--sk-muted) !important;
        font-size: 12px;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #f4f8fd;
        font-family: 'Manrope', sans-serif;
        font-weight: 800;
    }
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div,
    .stTextArea textarea, .stDateInput input {
        background: #101d30 !important;
        color: #edf3fb !important;
        border-color: rgba(148, 163, 184, .24) !important;
        border-radius: 10px !important;
    }
    div[data-baseweb="popover"] {
        background: #152238;
    }
    .stButton > button, .stDownloadButton > button {
        border: 1px solid rgba(69, 214, 197, .35);
        border-radius: 10px;
        color: #071a20;
        background: linear-gradient(110deg, #45d6c5, #8ae9d5);
        font-weight: 700;
        padding: .58rem 1.15rem;
        transition: transform .18s ease, box-shadow .18s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        color: #071a20;
        border-color: #8ae9d5;
        box-shadow: 0 7px 22px rgba(69, 214, 197, .16);
        transform: translateY(-1px);
    }
    div[role="radiogroup"] label {
        background: rgba(255,255,255,.035);
        border: 1px solid var(--sk-border);
        border-radius: 10px;
        padding: 10px 12px;
        margin: 4px 0;
    }
    [data-testid="stFileUploader"] {
        background: rgba(16, 29, 48, .65);
        border: 1px dashed rgba(111, 166, 190, .4);
        border-radius: 14px;
        padding: 12px;
    }
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        border: 1px solid var(--sk-border);
        border-radius: 12px;
        overflow: hidden;
    }
    div[data-testid="stAlert"] {
        border-radius: 12px;
    }
    hr {
        border-color: var(--sk-border);
    }
    .sk-footer {
        color: #71839b;
        text-align: center;
        font-size: 12px;
        padding: 28px 0 8px;
    }
    @media (max-width: 700px) {
        .block-container { padding: 1rem 1rem 2rem; }
        .sk-hero { padding: 25px 22px; border-radius: 18px; }
        .sk-hero h1 { font-size: 29px; }
    }
    </style>
    """
