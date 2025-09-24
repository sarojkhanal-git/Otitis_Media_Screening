import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

def render():
    st.markdown("""
    <style>
    .history-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .history-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2.5rem;
    }
    .history-header p {
        color: #f0f4ff;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    .analysis-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease;
    }
    .analysis-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .status-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    .status-normal { background: #dcfce7; color: #166534; }
    .status-abnormal { background: #fecaca; color: #991b1b; }
    .status-earwax { background: #fef3c7; color: #92400e; }
    .status-urgent { background: #fecaca; color: #991b1b; }
    .status-routine { background: #fef3c7; color: #92400e; }
    .status-no-referral { background: #dcfce7; color: #166534; }
    .filter-container {
        background: #f8faff;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #e0e7ff;
    }
    .summary-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        text-align: center;
        margin: 0.5rem;
    }
    .summary-number {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    .summary-label {
        font-size: 0.9rem;
        color: #666;
        margin: 0.3rem 0 0 0;
    }
    .action-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.9rem;
        cursor: pointer;
        margin: 0.2rem;
        transition: all 0.2s ease;
    }
    .action-button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    .confidence-bar {
        background: #e5e7eb;
        height: 6px;
        border-radius: 3px;
        margin: 0.5rem 0;
        overflow: hidden;
    }
    .confidence-fill {
        height: 100%;
        border-radius: 3px;
        background: linear-gradient(90deg, #10b981 0%, #34d399 100%);
        transition: width 0.3s ease;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="history-header">
        <h1>🕒 Analysis History</h1>
        <p>Review past analyses and track patient outcomes</p>
    </div>
    """, unsafe_allow_html=True)

    # Generate mock historical data
    def generate_mock_history():
        conditions = ["Normal", "AOM", "COM", "Earwax"]
        referrals = ["No Referral", "Routine", "Urgent"]

        history_data = []
        for i in range(25):
            days_ago = random.randint(0, 30)
            analysis_date = datetime.now() - timedelta(days=days_ago)

            condition = random.choice(conditions)
            if condition == "Normal":
                referral = random.choice(["No Referral", "Routine"])
                confidence = random.uniform(0.85, 0.98)
            elif condition == "Earwax":
                referral = random.choice(["Routine", "No Referral"])
                confidence = random.uniform(0.75, 0.95)
            else:  # AOM or COM
                referral = random.choice(["Urgent", "Routine"])
                confidence = random.uniform(0.80, 0.95)

            history_data.append({
                "id": f"A-{1000 + i}",
                "patient_id": f"P-{2000 + i}",
                "date": analysis_date,
                "time": analysis_date.strftime("%H:%M"),
                "filename": f"otoscopy_{i+1:03d}.jpg",
                "condition": condition,
                "confidence": confidence,
                "referral": referral,
                "processed_by": random.choice(["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown"]),
                "batch_id": f"B-{random.randint(100, 999)}" if random.random() > 0.7 else None
            })

        return sorted(history_data, key=lambda x: x["date"], reverse=True)

    # Initialize session state for history data
    if "history_data" not in st.session_state:
        st.session_state.history_data = generate_mock_history()

    history_data = st.session_state.history_data

    # Summary Statistics
    st.markdown("### 📊 Summary Statistics")

    total_analyses = len(history_data)
    urgent_cases = len([h for h in history_data if h["referral"] == "Urgent"])
    avg_confidence = sum([h["confidence"] for h in history_data]) / len(history_data) if history_data else 0
    recent_analyses = len([h for h in history_data if h["date"] >= datetime.now() - timedelta(days=7)])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-number" style="color: #667eea;">{total_analyses}</div>
            <div class="summary-label">Total Analyses</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-number" style="color: #ef4444;">{urgent_cases}</div>
            <div class="summary-label">Urgent Cases</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-number" style="color: #10b981;">{avg_confidence:.1%}</div>
            <div class="summary-label">Avg Confidence</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="summary-card">
            <div class="summary-number" style="color: #8b5cf6;">{recent_analyses}</div>
            <div class="summary-label">This Week</div>
        </div>
        """, unsafe_allow_html=True)

    # Filters
    st.markdown("### 🔍 Filter & Search")

    with st.container():
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            date_filter = st.selectbox(
                "📅 Date Range",
                ["All Time", "Today", "This Week", "This Month", "Last 30 Days"]
            )

        with col2:
            condition_filter = st.selectbox(
                "🔬 Condition",
                ["All Conditions", "Normal", "AOM", "COM", "Earwax"]
            )

        with col3:
            referral_filter = st.selectbox(
                "📋 Referral",
                ["All Referrals", "No Referral", "Routine", "Urgent"]
            )

        with col4:
            search_term = st.text_input("🔍 Search", placeholder="Patient ID, Analysis ID...")

        st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_data = history_data.copy()

    # Date filter
    now = datetime.now()
    if date_filter == "Today":
        filtered_data = [h for h in filtered_data if h["date"].date() == now.date()]
    elif date_filter == "This Week":
        week_start = now - timedelta(days=now.weekday())
        filtered_data = [h for h in filtered_data if h["date"] >= week_start]
    elif date_filter == "This Month":
        month_start = now.replace(day=1)
        filtered_data = [h for h in filtered_data if h["date"] >= month_start]
    elif date_filter == "Last 30 Days":
        thirty_days_ago = now - timedelta(days=30)
        filtered_data = [h for h in filtered_data if h["date"] >= thirty_days_ago]

    # Condition filter
    if condition_filter != "All Conditions":
        filtered_data = [h for h in filtered_data if h["condition"] == condition_filter]

    # Referral filter
    if referral_filter != "All Referrals":
        filtered_data = [h for h in filtered_data if h["referral"] == referral_filter]

    # Search filter
    if search_term:
        filtered_data = [h for h in filtered_data if
                        search_term.lower() in h["patient_id"].lower() or
                        search_term.lower() in h["id"].lower() or
                        search_term.lower() in h["filename"].lower()]

    # Results header
    st.markdown(f"### 📋 Analysis Records ({len(filtered_data)} results)")

    # Bulk actions
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        if st.button("📥 Export to CSV"):
            df = pd.DataFrame(filtered_data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"analysis_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

    with col2:
        if st.button("📄 Generate Report"):
            st.success("📄 Comprehensive report generation initiated!")

    with col3:
        if st.button("🔄 Refresh Data"):
            st.session_state.history_data = generate_mock_history()
            st.rerun()

    # Analysis records
    if filtered_data:
        for i, analysis in enumerate(filtered_data[:15]):  # Show first 15 results

            # Determine status badge classes
            condition_class = f"status-{analysis['condition'].lower()}"
            referral_class = f"status-{analysis['referral'].lower().replace(' ', '-')}"

            st.markdown(f"""
            <div class="analysis-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <div>
                        <h4 style="margin: 0; color: #374151;">Analysis {analysis['id']}</h4>
                        <p style="margin: 0.2rem 0 0 0; color: #6b7280; font-size: 0.9rem;">
                            Patient: {analysis['patient_id']} | {analysis['date'].strftime('%Y-%m-%d')} at {analysis['time']}
                        </p>
                    </div>
                    <div style="text-align: right;">
                        <span class="status-badge {condition_class}">{analysis['condition']}</span>
                        <span class="status-badge {referral_class}">{analysis['referral']}</span>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 1rem; margin-bottom: 1rem;">
                    <div>
                        <strong>File:</strong> {analysis['filename']}<br>
                        <strong>Processed by:</strong> {analysis['processed_by']}
                    </div>
                    <div>
                        <strong>Confidence:</strong> {analysis['confidence']:.1%}<br>
                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: {analysis['confidence']*100}%"></div>
                        </div>
                    </div>
                    <div>
                        <strong>Batch ID:</strong> {analysis['batch_id'] or 'Single Analysis'}<br>
                        <strong>Status:</strong> <span style="color: #10b981;">✅ Completed</span>
                    </div>
                </div>

                <div style="text-align: right;">
                    <button class="action-button">👁️ View Details</button>
                    <button class="action-button">📄 Download Report</button>
                    <button class="action-button">🔄 Reprocess</button>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Pagination info
        if len(filtered_data) > 15:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem; color: #6b7280;">
                Showing 15 of {len(filtered_data)} results.
                <a href="#" style="color: #667eea;">Load more results</a>
            </div>
            """, unsafe_allow_html=True)

    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #6b7280;">
            <h3>📭 No Analysis Records Found</h3>
            <p>Try adjusting your filters or search terms.</p>
        </div>
        """, unsafe_allow_html=True)

    # Historical Trends
    if filtered_data:
        st.markdown("### 📈 Historical Trends")

        # Create trend data
        df = pd.DataFrame(filtered_data)
        df['date_only'] = df['date'].dt.date

        # Group by date and condition
        trend_data = df.groupby(['date_only', 'condition']).size().unstack(fill_value=0)

        # Create a simple chart using Streamlit's built-in charting
        if not trend_data.empty:
            st.line_chart(trend_data, height=300)

        # Condition distribution
        col1, col2 = st.columns(2)

        with col1:
            condition_counts = df['condition'].value_counts()
            st.bar_chart(condition_counts, height=300)
            st.caption("Condition Distribution")

        with col2:
            referral_counts = df['referral'].value_counts()
            st.bar_chart(referral_counts, height=300)
            st.caption("Referral Distribution")