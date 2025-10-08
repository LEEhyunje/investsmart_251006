"""
Stock Selector Component - 카테고리 및 검색 기능 추가
"""
import streamlit as st
from typing import Optional
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.json_client import InvestSmartJSONClient
from components.stock_data import STOCK_CATEGORIES


def render_simple_stock_selector() -> Optional[str]:
    """
    카테고리 및 검색 기능이 포함된 종목 선택 UI를 렌더링합니다.
 
    Returns:
        선택된 종목의 심볼(ticker)을 반환합니다.
    """
    try:
        data_dir = os.path.join(os.path.dirname(current_dir), "data")
        data_dir = os.path.abspath(data_dir)
        json_client = InvestSmartJSONClient(data_dir)
        available_symbols = json_client.get_available_symbols()
 
        if not available_symbols:
            st.error("종목 목록을 불러올 수 없습니다. 데이터 파일을 확인해주세요.")
            return None

        # 세션 상태에 selected_symbol이 없으면 초기화
        if 'selected_symbol' not in st.session_state:
            st.session_state.selected_symbol = None

        # Expander 상태 관리를 위한 세션 상태 초기화
        if 'expanded_category' not in st.session_state:
            st.session_state.expanded_category = None

        # 카테고리별 아코디언 메뉴
        for category, stocks in STOCK_CATEGORIES.items():
            # with 구문을 사용하여 expander 내부의 요소들이 정상적으로 렌더링되도록 합니다.
            with st.expander(f"📁 {category}", expanded=(st.session_state.expanded_category == category)):
                cols = st.columns(3)
                col_idx = 0
                for name, ticker in stocks.items():
                    # 데이터가 있는 종목만 버튼으로 표시
                    if ticker in available_symbols:
                        if cols[col_idx].button(name, key=ticker, use_container_width=True):
                            # 종목이 선택되면, 선택된 심볼을 저장하고
                            # step을 2로 변경하여 다음 페이지로 즉시 이동합니다.
                            st.session_state.selected_symbol = ticker
                            st.session_state.expanded_category = None
                            st.session_state.step = 2
                            st.rerun()
                        col_idx = (col_idx + 1) % 3

        st.markdown("---")
        # 검색창 (화면 하단으로 이동)
        search_query = st.text_input("🔍 Search stocks (e.g., AAPL, KOSPI, Tesla)", "").lower()

        # 검색어에 따라 실시간으로 후보군 표시
        if search_query:
            search_results = {}
            for category, stocks in STOCK_CATEGORIES.items():
                for name, ticker in stocks.items():
                    if search_query in name.lower() or search_query in ticker.lower():
                        if ticker in available_symbols:
                            search_results[name] = ticker
            
            if search_results:
                st.markdown("##### Search Results")
                search_cols = st.columns(3)
                search_col_idx = 0
                for name, ticker in search_results.items():
                    # 검색 결과는 버튼으로 표시하고, 클릭 시 step 2로 이동
                    if search_cols[search_col_idx].button(name, key=f"search_{ticker}", use_container_width=True):
                        st.session_state.selected_symbol = ticker
                        st.session_state.expanded_category = None
                        st.session_state.step = 2
                        st.rerun()
                    search_col_idx = (search_col_idx + 1) % 3
            else:
                st.warning("No search results found.")

        return st.session_state.selected_symbol
 
    except Exception as e:
        st.error(f"종목 선택 UI 렌더링 중 오류 발생: {e}")
        import traceback
        st.error(traceback.format_exc())
        return None
 
 
def render_stock_selector() -> Optional[str]:
    """
    [DEPRECATED] 이전 버전과의 호환성을 위해 유지.
    render_simple_stock_selector를 대신 사용하세요.
    """
    st.warning("`render_stock_selector`는 더 이상 사용되지 않습니다. `render_simple_stock_selector`를 사용해주세요.")
    return render_simple_stock_selector()
