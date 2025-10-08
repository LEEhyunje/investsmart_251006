"""
Streamlit Main App - 원본 코드와 동일한 단순한 차트 화면 (탭 없음)
"""
import streamlit.components.v1 as components
import streamlit as st
import sys
import os
import logging
from typing import Dict, Any, Optional

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# 페이지 설정 (모바일 최적화)
st.set_page_config(
    page_title="InvestSmart",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",  # 모바일에서 사이드바 기본 접힘
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "InvestSmart - Educational Chart Analysis Tool"
    }
)

# 컴포넌트 import
from components.stock_selector import render_simple_stock_selector
from utils.json_client import InvestSmartJSONClient
from components.chart import render_stock_chart

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def render_disclaimer():
    """면책조항 표시 - st.dialog를 사용하여 모달 팝업으로 변경"""
    if 'disclaimer_agreed' not in st.session_state:
        st.session_state.disclaimer_agreed = False
    
    if not st.session_state.disclaimer_agreed:
        @st.dialog("⚠️ Investment Disclaimer", dismissible=False)
        def show_disclaimer_dialog():
            st.markdown("""
            <div style='line-height: 1.5; font-size: 15px;'>
            <b>📋 Service Nature</b><br>
            - This service is for <b>investment education and information provision</b>.<br>
            - It is a learning platform providing technical analysis tools.
            <br><br>
            <b>⚠️ Investment Risk Warning</b><br>
            - <b>All investments carry the risk of principal loss</b>.<br>
            - Past performance does not guarantee future returns.<br>
            - The provided information is not investment advice.
            <br><br>
            <b>📊 Limitations of Provided Information</b><br>
            - Technical indicators and signals are for reference only.<br>
            - All investment decisions are <b>your own judgment and responsibility</b>.
            <br><br>
            <b>🔒 Disclaimer</b><br>
            - We are not responsible for investment losses from using this service.<br>
            - We recommend thorough review and expert consultation before investing.
            </div>
            """, unsafe_allow_html=True)
            
            st.write("") # 버튼 위에 여백 추가

            # 버튼을 아래에 배치
            if st.button("I understand and agree to the disclaimer", type="primary", use_container_width=True):
                st.session_state.disclaimer_agreed = True
                st.rerun()
            
            if st.button("Disagree", use_container_width=True):
                st.warning("You must agree to the disclaimer to use the service.")
                st.stop()

        show_disclaimer_dialog()

def get_json_client() -> InvestSmartJSONClient:
    """JSON 클라이언트 인스턴스 반환"""
    if 'json_client' not in st.session_state:
        # data 폴더 경로 설정 (프론트엔드 기준)
        # investsmart_web/frontend -> data
        data_dir = os.path.join(current_dir, "data")
        data_dir = os.path.abspath(data_dir)
        st.session_state.json_client = InvestSmartJSONClient(data_dir)
    return st.session_state.json_client


def test_json_connection() -> bool:
    """JSON 파일 연결 테스트"""
    try:
        client = get_json_client()
        # 디버깅 정보 출력 (주석처리)
        # st.write(f"🔍 데이터 폴더 경로: {client.data_dir}")
        # st.write(f"🔍 폴더 존재 여부: {os.path.exists(client.data_dir)}")
        
        # if os.path.exists(client.data_dir):
        #     files = os.listdir(client.data_dir)
        #     st.write(f"🔍 폴더 내 파일들: {files}")
        
        # 간단한 데이터 확인
        info = client.get_data_info()
        # st.write(f"🔍 데이터 정보: {info}")
        return info['total_records'] > 0
    except Exception as e:
        logger.error(f"JSON 파일 연결 실패: {e}")
        st.error(f"❌ 오류 상세: {e}")
        return False

def show_cache_stats():
    """캐시 통계 표시 (개발자 모드)"""
    try:
        client = get_json_client()
        stats = client.get_cache_stats()
        
        if stats['total_requests'] > 0:
            with st.expander("📊 성능 통계 (개발자 모드)", expanded=False):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("총 요청", stats['total_requests'])
                with col2:
                    st.metric("캐시 히트", stats['cache_hits'])
                with col3:
                    st.metric("캐시 미스", stats['cache_misses'])
                with col4:
                    st.metric("히트율", f"{stats['hit_rate']}%")
                
                st.caption(f"캐시된 종목: {stats['cached_symbols']}개 | 처리된 캐시: {stats['processed_cache_size']}개")
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("🗑️ 캐시 초기화", type="secondary"):
                        client.clear_cache()
                        st.rerun()
                
                with col_btn2:
                    if st.button("📦 JSON 압축", type="primary"):
                        with st.spinner("JSON 파일 압축 중..."):
                            compression_result = client.compress_json_files()
                            st.success(f"압축 완료: {compression_result['compressed_files']}개 파일, {compression_result['total_savings_mb']}MB 절약")
                        st.rerun()
    except Exception as e:
        logger.error(f"캐시 통계 표시 실패: {e}")

def main():
    """주식 분석 메인 페이지 - 단계별 사용자 인터페이스"""
    # JSON 파일 연결 테스트
    if not test_json_connection():
        st.error("🚨 Signal data files not found. Please check if signal data files exist.")
        st.stop()
    
    # 면책조항 표시 (메인 페이지 상단)
    render_disclaimer()
    
    # 세션 상태 초기화
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'selected_symbol' not in st.session_state:
        st.session_state.selected_symbol = None
    if 'selected_indicator_group' not in st.session_state:
        st.session_state.selected_indicator_group = None
    
    # 단계별 인터페이스
    if st.session_state.step == 1:
        render_step1_symbol_selection()
    elif st.session_state.step == 2:
        render_step2_indicator_selection()
    elif st.session_state.step == 3:
        render_step3_chart_display()
    
    # 하단 면책 문구 (항상 표시)
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px;'>"
        "※ This information is a data report, not investment advice. All investment decisions should be made under the investor's own responsibility."
        "</div>", 
        unsafe_allow_html=True
    )
    
    # 캐시 통계 표시 (개발자 모드)
    show_cache_stats()


def render_step1_symbol_selection():
    """1단계: 종목 선택"""
  
    st.markdown("### Step 1: Which stock(or index) are you curious about?")
    
    # 종목 선택
    symbol = render_simple_stock_selector()




def render_step2_indicator_selection():
    """2단계: 지표 그룹 선택"""
 
    st.markdown("### Step 2: How long do you prefer to invest?")
    
    # 이전 단계로 돌아가기
    if st.button("← Previous Step"):
        st.session_state.step = 1
        st.rerun()
    
    st.info(f"Selected Stock: **{st.session_state.selected_symbol}**")
    
    # 지표 그룹 선택
    indicator_groups = {
        "Long-term Analysis (Monthly)": {
            "description": "Long-term investment indicators",
            "signals": ["long_signal", "combined_signal_v1"],
            "color": "#4169E1"
        },
        "Mid-term Analysis (Weekly)": {
            "description": "Mid-term investment indicators", 
            "signals": ["short_signal_v1", "momentum_color_signal"],
            "color": "#32CD32"
        },
        "Short-term Analysis (Daily)": {
            "description": "Short-term trading indicators",
            "signals": ["short_signal_v2", "macd_signal"],
            "color": "#00FFFF"
        }
    }
    
    # 지표 그룹 선택 버튼들
    cols = st.columns(3)
    for i, (group_name, group_info) in enumerate(indicator_groups.items()):
        # 버튼에 표시할 텍스트를 동적으로 생성
        button_text = ""
        if "Long-term" in group_name:
            button_text = "Long-term (few years)"
        elif "Mid-term" in group_name:
            button_text = "Mid-term (few months)"
        elif "Short-term" in group_name:
            button_text = "Short-term (few weeks)"

        with cols[i]:
            # 각 그룹을 container로 묶고 테두리 추가
            with st.container(border=True):
                # 그룹 제목과 선택 버튼을 먼저 표시
                if st.button(
                    button_text,
                    key=f"group_{group_name}",
                    use_container_width=True,
                    type="primary"
                ):
                    st.session_state.selected_indicator_group = group_name
                    st.session_state.selected_signals = group_info['signals']
                    st.session_state.step = 3
                    st.rerun()

                # 상세 설명은 expander 안에 넣어 숨김
                with st.expander("Details"):
                    if group_name == "Long-term Analysis (Monthly)":
                        st.markdown("### 🔴 Long-term")
                        st.markdown("**Investment Period:** ██████ (few years)")
                        st.markdown("**Success Rate:** █████░")
                        st.markdown("""
                        **Analysis:** macro trends  
                        **Purpose:** Value investing and portfolio strategy development  
                        **Use Case:** Long-term investment, asset allocation, risk management
                        """)
                    elif group_name == "Mid-term Analysis (Weekly)":
                        st.markdown("### 🟡 Mid-term")
                        st.markdown("**Investment Period:** ████░░ (few months)")
                        st.markdown("**Success Rate:** █████░")
                        st.markdown("""
                        **Analysis:** Trend Analysis  
                        **Purpose:** Trend confirmation and mid-term investment direction  
                        **Use Case:** Position entry after confirming weekly uptrend reversal
                        """)
                    elif group_name == "Short-term Analysis (Daily)":
                        st.markdown("### 🔵 Short-term")
                        st.markdown("**Investment Period:** ██░░░░ (few weeks)")
                        st.markdown("**Success Rate:** ████░░")
                        st.markdown("""
                        **Analysis:** precise timing  
                        **Purpose:** Quick volatility capture and short-term trading timing  
                        **Use Case:** Fast entry/exit signals during rapid rise/fall periods
                        """)


def render_step3_chart_display():
    """3단계: 차트만 표시"""
    # 이전 단계로 돌아가기 버튼만 표시
    if st.button("← Previous Step"):
        st.session_state.step = 2
        st.rerun()

    # 차트 표시 설정
    settings = {
        'selected_signals': st.session_state.selected_signals,
        'show_buy_signals': True,
        'show_sell_signals': True,
        'show_trendlines': True,
        'selected_indicators': [],
        'selected_indicator_group': st.session_state.selected_indicator_group
    }

    # 차트 렌더링 (3년 기본 기간) - 로딩 중에만 가이드 표시
    render_stock_chart(st.session_state.selected_symbol, "3y", settings)

if __name__ == "__main__":
    main()