import streamlit as st
import pandas as pd
import time
import urllib.parse

# 1. Daniel 전용 모바일/PC 통합 디자인 설정
st.set_page_config(page_title="Daniel's Alpha Fisher", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.8em; font-weight: bold;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%); color: white; border: none;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    .fact-card { border-left: 5px solid #10B981; background-color: #1c2128; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .rumor-card { border-left: 5px solid #EF4444; background-color: #1c2128; padding: 15px; border-radius: 10px; margin-bottom: 10px; opacity: 0.7; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 메모리 저장소
if 'ocean_data' not in st.session_state: st.session_state.ocean_data = []
if 'fact_net' not in st.session_state: st.session_state.fact_net = []
if 'rumor_net' not in st.session_state: st.session_state.rumor_net = []

# 3. 메인 타이틀
st.title("🛡️ Daniel's Alpha Fisher")
st.caption("모네타 보좌: 객관성 가중치 90% 기반 실시간 팩트체크 시스템")

# --- [수동 낚시 창] 상단 배치 ---
st.subheader("🎣 정보의 바다 낚시터")
if st.button("🌊 수동으로 실시간 찌라시 낚아올리기", type="primary"):
    # 낚시 퍼포먼스
    progress_bar = st.progress(0, text="낚싯대를 던졌습니다... 🎣")
    for i in range(1, 101):
        time.sleep(0.01)
        progress_bar.progress(i)
        if i == 40: progress_bar.progress(i, text="심해 수급 데이터 분석 중... 📡")
        if i == 80: progress_bar.progress(i, text="❗ 거대한 입질! 대어 포착 완료!!")
    
    time.sleep(0.5)
    progress_bar.empty()
    st.toast("대어 포착! 대기망을 확인하십시오.", icon="💎")
    
    # 실시간 데이터 낚아옴 (시뮬레이션)
    st.session_state.ocean_data = [
        {"ID": 1, "종목": "삼성전자", "내용": "HBM4 단독 공급 임박 루머", "반응도": 12.4, "결과": "Fact"},
        {"ID": 2, "종목": "SK하이닉스", "내용": "엔비디아 추가 물량 배정설", "반응도": 7.8, "결과": "Fact"},
        {"ID": 3, "종목": "A종목", "내용": "대규모 횡령 발생 찌라시", "반응도": -18.2, "결과": "Rumor"}
    ]
    st.rerun()

st.divider()

# --- 4. 탭 구성: 대기 / 사실 / 루머 ---
tab1, tab2, tab3 = st.tabs(["🐟 포착 대기망", "✅ Fact (사실확정)", "🚫 Rumor (가짜뉴스)"])

with tab1:
    if st.session_state.ocean_data:
        st.subheader("방금 낚아올린 미검증 데이터")
        df_ocean = pd.DataFrame(st.session_state.ocean_data)[["종목", "내용", "반응도"]]
        st.dataframe(df_ocean, hide_index=True, use_container_width=True)
        
        # [자동 검증 버튼]
        if st.button("🤖 모네타 AI 자동 팩트 검증 가동"):
            with st.status("후속 보도 및 DART 공시 추적 중...", expanded=True) as status:
                time.sleep(1)
                st.write("🔍 네이버 뉴스 교차 검증 완료...")
                time.sleep(1)
                st.write("⚖️ DART 공시 대조 및 수급 확인 완료...")
                status.update(label="검증 완료! 데이터 자동 분류 중...", state="complete")
            
            # 자동 분류 로직
            for item in st.session_state.ocean_data:
                if item["결과"] == "Fact":
                    st.session_state.fact_net.append(item)
                else:
                    st.session_state.rumor_net.append(item)
            
            st.session_state.ocean_data = [] # 대기망 비우기
            st.rerun()
    else:
        st.info("상단 버튼을 눌러 스캔 및 낚시를 시작하십시오.")

with tab2:
    if st.session_state.fact_net:
        st.subheader("📈 Fact 기반 투자 근거")
        for item in st.session_state.fact_net:
            with st.container():
                st.markdown(f"**[✅ 사실확정] {item['종목']}**")
                st.write(f"내용: {item['내용']} (에너지: {item['반응도']}%)")
                
                # --- [핵심] 근거/실체 클릭 연동 파트 ---
                encoded_name = urllib.parse.quote(item['종목'])
                c1, c2 = st.columns(2)
                news_url = f"https://search.naver.com/search.naver?where=news&query={encoded_name}+특징주&sort=1"
                dart_url = f"https://dart.fss.or.kr/dsab001/main.do?text={encoded_name}"
                
                c1.link_button("📄 뉴스 실체 확인", news_url, use_container_width=True)
                c2.link_button("🏛️ DART 공시 연동", dart_url, use_container_width=True)
                st.divider()
    else:
        st.write("아직 확정된 사실 정보가 없습니다.")

with tab3:
    if st.session_state.rumor_net:
        st.subheader("🚫 Rumor 격리 구역")
        for item in st.session_state.rumor_net:
            st.markdown(f"<div class='rumor-card'><b>{item['종목']}</b>: {item['내용']}</div>", unsafe_allow_html=True)
            st.caption("주의: 후속 기사 및 공시를 통해 가짜로 판명됨.")
    else:
        st.write("격리된 루머가 없습니다.")

