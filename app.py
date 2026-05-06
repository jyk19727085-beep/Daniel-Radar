import streamlit as st
import pandas as pd
import time
import urllib.parse

# 1. Daniel 전용 다크 인텔리전스 디자인
st.set_page_config(page_title="Daniel's Alpha Fisher v11", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    /* 자동 가동 중인 레이더 효과 */
    .radar-active { color: #10B981; font-weight: bold; animation: blink 2s infinite; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0.3; } 100% { opacity: 1; } }
    .stButton>button { border-radius: 12px; font-weight: bold; }
    .fact-box { border: 1px solid #10B981; padding: 15px; border-radius: 10px; margin-bottom: 10px; background-color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# 2. 데이터 메모리 (상태 유지)
if 'ocean_data' not in st.session_state: st.session_state.ocean_data = []
if 'fact_net' not in st.session_state: st.session_state.fact_net = []
if 'rumor_net' not in st.session_state: st.session_state.rumor_net = []
if 'auto_scanned' not in st.session_state: st.session_state.auto_scanned = False

# [핵심 1] 최초 접속 시 자동(Auto) 낚시 기능
if not st.session_state.auto_scanned:
    with st.status("🚀 대시보드 접속: 실시간 오토 레이더 가동 중...", expanded=False) as status:
        time.sleep(1)
        st.session_state.ocean_data = [
            {"종목": "삼성전자", "내용": "HBM4 단독 공급 임박 루머", "반응도": 12.4, "유형": "Fact"},
            {"종목": "SK하이닉스", "내용": "엔비디아 추가 물량 배정설", "반응도": 7.8, "유형": "Fact"},
            {"종목": "A종목", "내용": "대규모 횡령 발생 찌라시", "반응도": -18.2, "유형": "Rumor"}
        ]
        st.session_state.auto_scanned = True
        status.update(label="✅ 실시간 찌라시 자동 포착 완료!", state="complete")
    st.rerun()

# 3. 메인 화면 구성
st.title("🛡️ Daniel's Alpha Fisher")
st.markdown("상태: <span class='radar-active'>● 실시간 AUTO 레이더 작동 중</span>", unsafe_allow_html=True)

# [핵심 2] 수동 낚시 버튼 (언제든 추가 낚시 가능)
if st.button("🎣 추가 수동 낚시 (심해 찌라시 낚아올리기)"):
    with st.spinner("낚싯줄을 던졌습니다..."):
        time.sleep(1)
        new_fish = {"종목": "신규주", "내용": "외인 대량 수급 포착", "반응도": 5.5, "유형": "Fact"}
        st.session_state.ocean_data.append(new_fish)
        st.toast("대어 한 마리를 추가로 낚았습니다!", icon="🐟")

st.divider()

# 4. 정보 탭
tab1, tab2, tab3 = st.tabs(["🐟 대기망", "✅ 사실확정망", "🚫 루머격리망"])

with tab1:
    if st.session_state.ocean_data:
        st.subheader("⚠️ 미검증 정보 (터치하여 내용 확인)")
        
        # [핵심 3] 종목 내용 바로 확인 가능한 연동 표
        df_ocean = pd.DataFrame(st.session_state.ocean_data)
        selected = st.data_editor(
            df_ocean[["종목", "내용", "반응도"]],
            hide_index=True, use_container_width=True,
            column_config={"내용": st.column_config.TextColumn("찌라시 내용 (편집가능)")}
        )
        
        # [핵심 4] 자동 검증 및 수동 이동 확정 버튼
        c1, c2 = st.columns(2)
        if c1.button("🤖 Auto 검증 및 이동", use_container_width=True):
            for item in st.session_state.ocean_data:
                if item["유형"] == "Fact": st.session_state.fact_net.append(item)
                else: st.session_state.rumor_net.append(item)
            st.session_state.ocean_data = []
            st.toast("AI가 사실과 루머를 자동 분류했습니다.", icon="🤖")
            st.rerun()
            
        if c2.button("✋ 수동 확정 이동", use_container_width=True):
            st.info("데이터 에디터에서 직접 판정 후 이동하는 모드입니다. (준비 중)")

    else:
        st.info("현재 대기망이 비어있습니다. 추가 낚시를 시도하세요.")

with tab2:
    if st.session_state.fact_net:
        for item in st.session_state.fact_net:
            with st.container(border=True):
                st.markdown(f"**{item['종목']}** (에너지: {item['반응도']}%)")
                st.caption(item['내용'])
                
                # 실체 확인 연동 링크
                q = urllib.parse.quote(item['종목'])
                col_a, col_b = st.columns(2)
                col_a.link_button("📄 뉴스 실체", f"https://search.naver.com/search.naver?query={q}+특징주")
                col_b.link_button("🏛️ DART 공시", f"https://dart.fss.or.kr/dsab001/main.do?text={q}")
    else:
        st.write("사실로 확정된 정보가 없습니다.")

with tab3:
    for item in st.session_state.rumor_net:
        st.error(f"🚫 {item['종목']}: {item['내용']}")
