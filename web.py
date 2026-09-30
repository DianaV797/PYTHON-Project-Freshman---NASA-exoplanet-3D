import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="NASA Exoplanet 3D Explorer", layout="wide")
st.title("🪐 NASA Exoplanet 3D Explorer (สำรวจดาวเคราะห์นอกระบบสุริยะ)")
st.markdown("โปรเจกต์วิเคราะห์และแสดงผลข้อมูลดาวเคราะห์นอกระบบสุริยะจากฐานข้อมูลในรูปแบบ 3 มิติ")

@st.cache_data
def load_exoplanet_data():
    df = pd.read_csv('cleaned_5250.csv')
    
    df = df.head(400).copy()
    
    df['name'] = df['name'].fillna('Unnamed Planet')
    df['planet_type'] = df['planet_type'].fillna('Unknown')
    df['distance'] = df['distance'].fillna(0)
    df['orbital_radius'] = df['orbital_radius'].fillna(0)
    df['mass_multiplier'] = df['mass_multiplier'].fillna(1)
    df['radius_multiplier'] = df['radius_multiplier'].fillna(1)
    
    df['Size'] = df['radius_multiplier'] * 3
    df['Size'] = df['Size'].apply(lambda x: max(x, 2))
    
    return df

try:
    df = load_exoplanet_data()
    
    st.sidebar.header("🎛️ ตัวกรองข้อมูลดาวเคราะห์")
    planet_types = ['ทั้งหมด'] + sorted(list(df['planet_type'].unique()))
    selected_type = st.sidebar.selectbox("เลือกประเภทดาวเคราะห์ (Planet Type):", options=planet_types)

    if selected_type != 'ทั้งหมด':
        filtered_df = df[df['planet_type'] == selected_type]
    else:
        filtered_df = df

    st.write(f"✨ กำลังแสดงผลดาวเคราะห์ตัวอย่าง **{len(filtered_df)}** ดวง (โหมดประหยัดทรัพยากรเครื่อง)")

    fig = px.scatter_3d(
        filtered_df,
        x='distance',
        y='orbital_radius',
        z='mass_multiplier',
        text='name',
        size='Size',
        color='planet_type',
        hover_data=['discovery_year', 'detection_method', 'stellar_magnitude'],
        title="3D Exoplanet Space Map (พิกัดเชิงวิเคราะห์)"
    )

    fig.update_layout(
        scene=dict(
            xaxis_backgroundcolor='black',
            yaxis_backgroundcolor='black',
            zaxis_backgroundcolor='black',
            xaxis=dict(title='Distance (ระยะทาง)', gridcolor='gray'),
            yaxis=dict(title='Orbital Radius (รัศมีวงโคจร)', gridcolor='gray'),
            zaxis=dict(title='Mass Multiplier (มวลเปรียบเทียบ)', gridcolor='gray'),
        ),
        paper_bgcolor='black',
        font=dict(color='white'),
        height=650
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 ตารางข้อมูลรายละเอียดดาวเคราะห์")
    st.dataframe(filtered_df[['name', 'planet_type', 'distance', 'orbital_radius', 'mass_multiplier', 'discovery_year', 'detection_method']], use_container_width=True)

except Exception as e:
    st.error(f"เกิดข้อผิดพลาดในการโหลดไฟล์ข้อมูล: {e}")