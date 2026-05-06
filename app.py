import streamlit as st
import pandas as pd
import time
import urllib.parse
import plotly.graph_objects as go

# 1. 디자인 및 테마 설정
st.set_page_config(page_title="Daniel's Alpha Fisher v14", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; font-weight: bold; background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%); color: white; }
    .status-text { text-align: center; font-weight: bold; font-size: 1.2rem; }
    </style>
    """, unsafe_allow_html=True)

# 2. 시스템 데이터 엔진
if 'ocean_data' not in st.session_state: st.session_state.ocean_data = []
if 'fact_net' not in st.session_state: st.session_state.fact_net = []
if 'rumor_net' not in st.session_state: st.session_state.rumor_net = []

# --- [신규 섹션] 한국형 공포·탐욕 지수 계산 (가상 알고리즘 연동) ---
def get_k_fear_greed():
    # 실제 환경에서는 코스피 변동성, 거래량 등을 수집하여 계산
    # 현재는 예시로 '58(중립/탐욕 사이)' 세팅
    score = 58 
    if score < 25: label, color = "극심한 공포 (매수 찬스)", "#EF4444"
    elif score < 45: label, color = "공포", "#F59E0B"
    elif score < 55: label, color = "중립", "#6B7280"
    elif score < 75: label, color = "탐욕", "#10B981"
    else: label, color = "극심한 탐욕 (분할 매도)", "#059669"
    return score, label, color

score, label, color = get_k_fear_greed()

# --- 최상단 지수 레이아웃 ---
st.markdown(f"<h3 style='text-align: center;'>🇰🇷 K-공포·탐욕 지수</h3>", unsafe_allow_html=True)
fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = score,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': label, 'font': {'size': 20, 'color': color}},
    gauge = {
        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
        'bar': {'color': color},
        'bgcolor': "white",
        'borderwidth': 2,
        'bordercolor': "gray",
        'steps': [
            {'range': [0, 25], 'color': '#EF4444'},
            {'range': [25, 45], 'color': '#F59E0B'},
            {'range': [45, 55], 'color': '#6B7280'},
            {'range': [55, 75], 'color': '#10B981'},
            {'range': [75, 100], 'color': '#059669'}],
    }
))
fig_gauge.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Arial"}, height=300, margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# --- [기존] 접속 시 최초 Auto 구동 및 수동 낚시 ---
if not st.session_state.ocean_data and not st.session_state.fact_net:
    with st.status("🚀 실시간 시장 레이더 자동 가동 중...", expanded=False) as status:
        time.sleep(1)
        st.session_state.ocean_data = [
            {"기업명": "삼성전자", "코멘트": "HBM4 퀄테스트 통과 임박설 돌며 외인 순매수 전환 중이라더라", "에너지": 14.5, "유형": "Fact"},
            {"기업명": "LG에너지솔루션", "코멘트": "테슬라 신형 배터리 수주 확정 기사 곧 뜬다더라", "에너지": 9.2, "유형": "Fact"},
            {"기업명": "고려아연", "코멘트": "경영권 분쟁 재점화로 오늘 한 번 더 튄다더라", "에너지": 21.0, "유형": "Fact"}
        ]
        status.update(label="✅ 실시간 찌라시 자동 포착 완료!", state="complete")

if st.button("🌊 전 매체 실시간 이슈/소문 수동 낚시 (추가)"):
    with st.spinner("낚싯대를 던졌습니다..."):
        time.sleep(0.8)
        new_item = {"기업명": "SK하이닉스", "코멘트": "엔비디아 CEO 깜짝 방문 소식에 난리났다더라", "에너지": 11.0, "유형": "Fact"}
        st.session_state.ocean_data.append(new_item)
        st.rerun()

# --- 탭 구성 및 검증 시스템 ---
tab1, tab2, tab3 = st.tabs(["🐟 포착 대기망", "✅ 사실확정 (Fact)", "🚫 가짜뉴스 (Rumor)"])

with tab1:
    if st.session_state.ocean_data:
        st.subheader("⚠️ 시장 '카더라' 리스트")
        for i, item in enumerate(st.session_state.ocean_data):
            with st.container(border=True):
                st.markdown(f"**[{item['기업명']}]** <span style='color:#FFD700;'>\"{item['코멘트']}\"</span>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns([1,1,1])
                if c1.button("✅ 사실", key=f"f_{i}"):
                    st.session_state.fact_net.append(item); st.session_state.ocean_data.pop(i); st.rerun()
                if c2.button("🚫 가짜", key=f"r_{i}"):
                    st.session_state.rumor_net.append(item); st.session_state.ocean_data.pop(i); st.rerun()
                q = urllib.parse.quote(item['기업명'])
                c3.link_button("🏛️ 실체확인", f"https://dart.fss.or.kr/dsab001/main.do?text={q}")
    else:
        st.info("새로운 소문을 낚아 올리십시오.")

with tab2:
    for item in st.session_state.fact_net:
        with st.expander(f"💎 {item['기업명']} - 사실 확정", expanded=True):
            st.write(item['코멘트'])
            q = urllib.parse.quote(item['기업명'])
            st.link_button("🏛️ DART 공시 원문 확인", f"https://dart.fss.or.kr/dsab001/main.do?text={q}", use_container_width=True)

with tab3:
    for item in st.session_state.rumor_net:
        st.error(f"🚫 {item['기업명']}: {item['코멘트']} (가짜뉴스로 판명)")
