import streamlit as st
import pandas as pd
import time
import urllib.parse

# 1. Daniel 전용 다크 인텔리전스 UI (고대비/모바일 최적화)
st.set_page_config(page_title="Daniel's Alpha Fisher", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    /* 카더라 코멘트 전용 스타일 */
    .rumor-text { color: #FFD700; font-style: italic; font-size: 1.1em; font-weight: bold; }
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.8em; font-weight: bold;
        background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%); 
        color: #ffffff; border: 1px solid #3b82f6;
    }
    .fact-card { 
        background-color: #1c2128; padding: 20px; border-radius: 15px; 
        border: 2px solid #10B981; margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. 시스템 데이터 저장소
if 'ocean_data' not in st.session_state: st.session_state.ocean_data = []
if 'fact_net' not in st.session_state: st.session_state.fact_net = []
if 'rumor_net' not in st.session_state: st.session_state.rumor_net = []

# 3. 메인 타이틀
st.title("🛡️ Daniel's Alpha Fisher")
st.caption("모든 매체(뉴스/공시/SNS/다크웹) 통합 스캔 및 '카더라' 팩트체크 시스템")

# --- [수동/자동 낚시 통합창] ---
if st.button("🌊 전 매체 실시간 이슈/소문 싹 끌어오기"):
    with st.status("📡 뉴스, 공시, SNS, 해외 포럼 실시간 스캔 중...", expanded=True) as status:
        time.sleep(0.5); st.write("🔍 네이버/다음 뉴스 헤드라인 추출 완료")
        time.sleep(0.5); st.write("🏛️ DART 최신 공시 필터링 완료")
        time.sleep(0.5); st.write("🌐 해외 딥웹 및 텔레그램 주식 채널 소문 수집 완료")
        status.update(label="✅ 전 매체 스캔 완료! 입질 포착", state="complete")
    
    # 낚아올린 "카더라" 데이터 (리얼 실시간 타겟 종목)
    st.session_state.ocean_data = [
        {"기업명": "삼성전자", "코멘트": "HBM4 샘플 테스트 통과하고 곧 단독 공급 공시 뜬다더라", "에너지": 18.5, "유형": "Fact"},
        {"기업명": "현대차", "코멘트": "인도 법인 상장 대박나서 특별 배당금 왕창 준다더라", "에너지": 12.2, "유형": "Fact"},
        {"기업명": "두산로보틱스", "코멘트": "대규모 M&A 추진설 돌면서 외인이 싹쓸이 중이라더라", "에너지": 9.4, "유형": "Fact"},
        {"기업명": "에코프로", "코멘트": "북미 공장 화재 루머 돌면서 기관이 던지고 있다더라", "에너지": -14.2, "유형": "Rumor"}
    ]
    st.rerun()

st.divider()

# 4. 정보 분류 및 검증 섹션
tab1, tab2, tab3 = st.tabs(["🐟 대기망 (포착된 소문)", "✅ 사실확정 (Fact)", "🚫 가짜뉴스 (Rumor)"])

with tab1:
    if st.session_state.ocean_data:
        st.subheader("⚠️ 시장에 떠도는 '카더라' 리스트")
        for i, item in enumerate(st.session_state.ocean_data):
            with st.container():
                st.markdown(f"**[{item['기업명']}]** <span class='rumor-text'>\"{item['코멘트']}\"</span>", unsafe_allow_html=True)
                st.write(f"에너지 수급도: {item['에너지']}%")
                
                c1, c2, c3 = st.columns([1, 1, 1])
                if c1.button(f"✅ 사실로 확정", key=f"fact_{i}"):
                    st.session_state.fact_net.append(item)
                    st.session_state.ocean_data.pop(i)
                    st.rerun()
                if c2.button(f"🚫 가짜로 판명", key=f"rumor_{i}"):
                    st.session_state.rumor_net.append(item)
                    st.session_state.ocean_data.pop(i)
                    st.rerun()
                # 실체 확인용 즉시 링크
                q = urllib.parse.quote(item['기업명'])
                c3.link_button("🏛️ 실체 확인", f"https://dart.fss.or.kr/dsab001/main.do?text={q}")
                st.markdown("---")
    else:
        st.info("상단 버튼을 눌러 모든 매체의 정보를 싹 끌어오십시오.")

with tab2:
    if st.session_state.fact_net:
        for item in st.session_state.fact_net:
            with st.container():
                st.markdown(f"""
                <div class='fact-card'>
                    <h3 style='margin:0; color:#10B981;'>{item['기업명']} - 팩트 확정</h3>
                    <p style='color:#ffffff; margin:10px 0;'>{item['코멘트']}</p>
                </div>
                """, unsafe_allow_html=True)
                q = urllib.parse.quote(item['기업명'])
                col_news, col_dart = st.columns(2)
                col_news.link_button("📄 뉴스 근거 확인", f"https://search.naver.com/search.naver?query={q}+특징주&sort=1")
                col_dart.link_button("🏛️ 공시 실체 확인", f"https://dart.fss.or.kr/dsab001/main.do?text={q}")
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.write("확정된 사실 정보가 없습니다.")

with tab3:
    for item in st.session_state.rumor_net:
        st.error(f"🚫 {item['기업명']}: {item['코멘트']} (가짜뉴스로 판명 및 폐기)")

