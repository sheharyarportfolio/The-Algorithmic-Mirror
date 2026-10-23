from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="The Algorithmic Mirror | AI Hiring Audits",
    page_icon="⚖️",
    layout="wide"
)

# Stylized Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1e3d59;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        font-size: 1.3rem;
        color: #17b978;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 500;
    }
    .section-header {
        font-size: 1.8rem;
        color: #1e3d59;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    dataset_path = Path(__file__).resolve().parent / 'AI_Hiring_Bias_Dataset.csv'
    df = pd.read_csv(dataset_path)

    # Map continuous variables to descriptive bins
    df['experience_group'] = pd.cut(
        df['years_experience'],
        bins=[-np.inf, 2, 5, 10, np.inf],
        labels=['Entry-level', 'Junior', 'Mid-level', 'Senior']
    )
    df['employment_gap_group'] = pd.cut(
        df['employment_gap_months'],
        bins=[-np.inf, 0, 3, 6, 12, np.inf],
        labels=['No gap', 'Short gap', 'Moderate gap', 'Long gap', 'Very long gap']
    )
    df['salary_group'] = pd.cut(
        df['expected_salary'],
        bins=[-np.inf, 75000, 110000, 150000, 200000, np.inf],
        labels=['Low', 'Lower-middle', 'Upper-middle', 'High', 'Very high']
    )

    # Flag and categorize statistical outliers
    for col, group_col in [
        ('years_experience', 'experience_group'),
        ('employment_gap_months', 'employment_gap_group'),
        ('expected_salary', 'salary_group')
    ]:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        if 'Outlier' not in df[group_col].cat.categories:
            df[group_col] = df[group_col].cat.add_categories(['Outlier'])
        df.loc[outlier_mask, group_col] = 'Outlier'

    df['high_performer'] = df['technical_skill_score'] >= df['technical_skill_score'].quantile(0.75)
    return df

try:
    df = load_data()
except FileNotFoundError as e:
    st.error(f"Dataset file was not found next to this app: {e}")
    st.stop()
except Exception as e:
    st.error(f"Could not load the hiring dataset: {e}")
    st.stop()

# Custom App Header
st.markdown('<div class="main-title">⚖️ The Algorithmic Mirror</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A Data-Driven Story of AI Recruiting, Human Metrics, and Unintended Bias</div>', unsafe_allow_html=True)

# Tabs
tab_home, tab_act1, tab_act2, tab_act3, tab_act4 = st.tabs([
    "📖 The Prologue",
    "Act I: The Parity Paradox",
    "Act II: Credentials & Expectations",
    "Act III: The Career Break Penalty",
    "💡 Key Takeaways"
])

with tab_home:
    st.markdown('<div class="section-header">The Auditing of TechVantage Corp.</div>', unsafe_allow_html=True)
    st.markdown("""
    **The Backdrop:**  
    To streamline hiring and eliminate human subjectivity, **TechVantage Corp** deployed an advanced machine-learning screening engine. 
    The system was designed to evaluate candidates on merit, outputting an **AI Resume Score** alongside an **AI Bias Score** meant to flag potential discrepancies.
    
    However, human resource metrics soon showed unexpected hiring drops among key demographics. Is our math neutral, or does it perpetuate existing systemic patterns?
    
    *Explore the tabs above to reveal how AI algorithms interact with gender parity, educational backgrounds, and employment breaks.*
    """)
    st.info("💡 **Navigation Tip:** Walk through the story chronologically from Act I to Act III using the tab bar at the top of your page.")

with tab_act1:
    st.markdown('<div class="section-header">Act I: The 80% Rule and Adverse Impact</div>', unsafe_allow_html=True)
    st.markdown("""
    The **4/5ths Rule (80% rule)** is the standard benchmark used to identify potential demographic bias. 
    If a group's selection rate falls below **80%** of the highest group's rate, it signals adverse impact.
    """)

    # Calculate parity metrics
    hiring_rate = df.groupby('gender')['hired'].mean()
    highest_rate = hiring_rate.max()
    impact_ratio = (hiring_rate / highest_rate) * 100
    parity_df = pd.DataFrame({
        'Hiring Rate (%)': (hiring_rate * 100).round(2),
        'Impact Ratio (%)': impact_ratio.round(2),
        'Potential Adverse Impact': impact_ratio < 80
    })

    col_table, col_desc = st.columns([2, 3])
    with col_table:
        st.dataframe(parity_df.style.highlight_max(subset=['Hiring Rate (%)'], color='#c8f7c5'))
    with col_desc:
        st.markdown("""
        **What the Data Tells Us:**
        - **Male Applicants:** Highest selection rate (**35.34%**), setting our 100% baseline.
        - **Female Applicants:** Standard of **30.91%** hiring rate (**87.48%** relative impact) represents compliant parity.
        - **Non-Binary Applicants:** Selection rate drops to **26.56%** (**75.16%** relative impact), actively triggering the **Adverse Impact Flag**.
        """)

    # Parity Chart
    fig_parity = go.Figure()
    fig_parity.add_trace(go.Bar(x=parity_df.index, y=parity_df['Hiring Rate (%)'], name='Hiring Rate (%)', marker_color='#34495e'))
    fig_parity.add_trace(go.Bar(x=parity_df.index, y=parity_df['Impact Ratio (%)'], name='Impact Ratio (%)', marker_color='#1abc9c'))
    fig_parity.add_shape(type="line", x0=-0.5, y0=80, x1=2.5, y1=80, line=dict(color="#e74c3c", width=3, dash="dash"))
    fig_parity.add_annotation(x=1.8, y=86, text="80% Adverse Impact Line", showarrow=False, font=dict(color="#e74c3c", size=12))
    fig_parity.update_layout(title="Hiring Rates and Relative Impact Ratios by Gender", template='plotly_white', barmode='group')
    st.plotly_chart(fig_parity, width="stretch")

with tab_act2:
    st.markdown('<div class="section-header">Act II: The Institutional Pedigree Premium</div>', unsafe_allow_html=True)
    st.markdown("Does background credentialing override raw performance metrics? Let's analyze how university tiers and educational levels shape salary profiles and hiring rates.")

    group_analysis = df.groupby(['education_level', 'university_tier']).agg(
        avg_expected_salary=('expected_salary', 'mean'),
        total_applicants=('hired', 'size'),
        hired_applicants=('hired', lambda x: (x == 1).sum())
    )
    group_analysis['hiring_rate'] = (group_analysis['hired_applicants'] / group_analysis['total_applicants'] * 100).round(2)
    group_analysis = group_analysis.reset_index()

    pivot_salary = group_analysis.pivot(index='education_level', columns='university_tier', values='avg_expected_salary')
    pivot_hiring = group_analysis.pivot(index='education_level', columns='university_tier', values='hiring_rate')

    col_m1, col_m2 = st.columns(2)
    with col_m1:
        fig_sal = px.imshow(pivot_salary, text_auto='.0f', color_continuous_scale='Viridis', title="Mean Expected Salary ($)")
        st.plotly_chart(fig_sal, width="stretch")
    with col_m2:
        fig_hir = px.imshow(pivot_hiring, text_auto='.1f', color_continuous_scale='Mint', title="Actual Hiring Rate (%)")
        st.plotly_chart(fig_hir, width="stretch")

with tab_act3:
    st.markdown('<div class="section-header">Act III: The Heavy Price of Career Breaks</div>', unsafe_allow_html=True)
    st.markdown("For individuals taking time off for caregiving, medical, or personal reasons, returning to the field can be difficult. How does the screening engine treat career gaps?")

    gap_analysis = df.groupby('employment_gap_group', observed=False).agg(
        total_applicants=('hired', 'size'),
        hired_applicants=('hired', lambda x: (x == 1).sum())
    )
    gap_analysis['hiring_rate'] = (gap_analysis['hired_applicants'] / gap_analysis['total_applicants'] * 100).round(2)

    fig_gap = px.bar(
        gap_analysis.reset_index(),
        x='employment_gap_group',
        y='hiring_rate',
        text='hiring_rate',
        color='employment_gap_group',
        color_discrete_sequence=px.colors.sequential.YlOrRd_r,
        title="Hiring Success Rate vs. Length of Career Breaks"
    )
    fig_gap.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    fig_gap.update_layout(yaxis=dict(range=[0, 45]), template='plotly_white', showlegend=False)
    st.plotly_chart(fig_gap, width="stretch")

with tab_act4:
    st.markdown('<div class="section-header">💡 Key Operational Auditing Steps</div>', unsafe_allow_html=True)
    st.markdown("""
    To resolve these algorithmic discrepancies, we recommend the following engineering changes:
    1. **Normalize Career Gap Penalties:** Remove career gap variables as hard filters in resume assessment models to avoid penalizing return-to-work professionals.
    2. **Mitigate University Tier Bias:** Standardize weights across University Tiers 1-3. Rely more on programmatic technical achievements.
    3. **Enforce Equal Opportunity Constraints:** Apply post-processing demographic parity rules to correct under-representation in selection algorithms.
    """)
