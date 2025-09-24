import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import random

def render():
    st.markdown("""
    <style>
    .dashboard-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    .dashboard-header h1 {
        color: white !important;
        margin: 0;
        font-size: 2.5rem;
    }
    .dashboard-header p {
        color: #f0f4ff;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    .metric-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
    }
    .metric-label {
        font-size: 1rem;
        color: #666;
        margin: 0.5rem 0 0 0;
    }
    .status-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin: 0.5rem 0;
    }
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    .status-online { background-color: #10b981; }
    .status-warning { background-color: #f59e0b; }
    .status-offline { background-color: #ef4444; }
    .quick-action-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="dashboard-header">
        <h1>📊 EarScope AI Dashboard</h1>
        <p>Real-time insights and system overview</p>
    </div>
    """, unsafe_allow_html=True)

    # Generate mock data for demonstration
    today = datetime.now()

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-number" style="color: #667eea;">247</div>
            <div class="metric-label">Total Analyses Today</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-number" style="color: #10b981;">94.2%</div>
            <div class="metric-label">System Accuracy</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-number" style="color: #f59e0b;">18</div>
            <div class="metric-label">Urgent Cases</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-number" style="color: #8b5cf6;">1.2s</div>
            <div class="metric-label">Avg Response Time</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # System Status and Quick Actions Row
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 🔧 System Status")
        st.markdown("""
        <div class="status-card">
            <div><span class="status-indicator status-online"></span><strong>AI Model:</strong> Online</div>
            <p style="margin: 0.5rem 0 0 20px; color: #666;">Primary classification model running optimally</p>
        </div>
        <div class="status-card">
            <div><span class="status-indicator status-online"></span><strong>API Server:</strong> Online</div>
            <p style="margin: 0.5rem 0 0 20px; color: #666;">All endpoints responding normally</p>
        </div>
        <div class="status-card">
            <div><span class="status-indicator status-warning"></span><strong>Storage:</strong> 78% Used</div>
            <p style="margin: 0.5rem 0 0 20px; color: #666;">Consider archiving old analysis data</p>
        </div>
        <div class="status-card">
            <div><span class="status-indicator status-online"></span><strong>Grad-CAM:</strong> Operational</div>
            <p style="margin: 0.5rem 0 0 20px; color: #666;">Heatmap generation working correctly</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("### ⚡ Quick Actions")
        st.markdown("""
        <div style="text-align: center; padding: 1rem;">
            <a href="#" class="quick-action-btn">🔬 New Analysis</a>
            <a href="#" class="quick-action-btn">📦 Batch Upload</a>
            <a href="#" class="quick-action-btn">📊 View Reports</a>
            <a href="#" class="quick-action-btn">⚙️ Settings</a>
            <a href="#" class="quick-action-btn">📥 Export Data</a>
            <a href="#" class="quick-action-btn">🔄 Refresh</a>
        </div>
        """, unsafe_allow_html=True)

    # Analytics Charts
    st.markdown("### 📈 Analytics")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Create mock time series data for analyses over the week
        dates = [today - timedelta(days=x) for x in range(7, 0, -1)]
        analyses_count = [random.randint(180, 280) for _ in range(7)]

        df_time = pd.DataFrame({
            'Date': dates,
            'Analyses': analyses_count
        })

        fig_time = px.line(df_time, x='Date', y='Analyses',
                          title='Daily Analyses (Past 7 Days)',
                          color_discrete_sequence=['#667eea'])
        fig_time.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151'),
            title_font_size=16
        )

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_time, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # Create classification distribution pie chart
        classifications = ['Normal', 'AOM', 'COM', 'Earwax']
        counts = [142, 45, 28, 32]
        colors = ['#4facfe', '#ff6b6b', '#f093fb', '#fbbf24']

        fig_pie = go.Figure(data=[go.Pie(
            labels=classifications,
            values=counts,
            hole=0.4,
            marker_colors=colors
        )])

        fig_pie.update_layout(
            title="Today's Classifications",
            font=dict(color='#374151'),
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_size=16,
            showlegend=True
        )

        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent Activity
    st.markdown("### 🕒 Recent Activity")

    # Create mock recent activity data
    recent_activities = [
        {"time": "2 mins ago", "activity": "Batch analysis completed", "count": "15 images", "status": "✅"},
        {"time": "5 mins ago", "activity": "Urgent case detected", "count": "Patient ID: P-2847", "status": "⚠️"},
        {"time": "12 mins ago", "activity": "PDF report generated", "count": "Analysis #A-3921", "status": "📄"},
        {"time": "18 mins ago", "activity": "System performance check", "count": "All systems normal", "status": "✅"},
        {"time": "25 mins ago", "activity": "New user registration", "count": "Dr. Smith", "status": "👤"},
    ]

    for activity in recent_activities:
        st.markdown(f"""
        <div class="status-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <strong>{activity['activity']}</strong>
                    <p style="margin: 0.2rem 0 0 0; color: #666; font-size: 0.9rem;">{activity['count']}</p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.2rem;">{activity['status']}</div>
                    <div style="font-size: 0.8rem; color: #666;">{activity['time']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Performance Metrics
    st.markdown("### 🎯 Performance Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Accuracy over time
        accuracy_data = [94.1, 94.3, 94.0, 94.5, 94.2, 94.4, 94.2]
        fig_acc = go.Figure()
        fig_acc.add_trace(go.Scatter(
            x=list(range(7)),
            y=accuracy_data,
            mode='lines+markers',
            name='Accuracy',
            line=dict(color='#10b981', width=3),
            marker=dict(size=8)
        ))
        fig_acc.update_layout(
            title="Model Accuracy (%)",
            xaxis_title="Days",
            yaxis_title="Accuracy",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151'),
            title_font_size=14,
            height=250
        )
        st.plotly_chart(fig_acc, use_container_width=True)

    with col2:
        # Response time
        response_times = [1.1, 1.3, 1.0, 1.2, 1.2, 1.1, 1.2]
        fig_resp = go.Figure()
        fig_resp.add_trace(go.Scatter(
            x=list(range(7)),
            y=response_times,
            mode='lines+markers',
            name='Response Time',
            line=dict(color='#8b5cf6', width=3),
            marker=dict(size=8)
        ))
        fig_resp.update_layout(
            title="Response Time (s)",
            xaxis_title="Days",
            yaxis_title="Seconds",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151'),
            title_font_size=14,
            height=250
        )
        st.plotly_chart(fig_resp, use_container_width=True)

    with col3:
        # Throughput
        throughput = [245, 267, 223, 278, 251, 289, 247]
        fig_thru = go.Figure()
        fig_thru.add_trace(go.Bar(
            x=list(range(7)),
            y=throughput,
            name='Daily Analyses',
            marker_color='#667eea'
        ))
        fig_thru.update_layout(
            title="Daily Throughput",
            xaxis_title="Days",
            yaxis_title="Analyses",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#374151'),
            title_font_size=14,
            height=250
        )
        st.plotly_chart(fig_thru, use_container_width=True)