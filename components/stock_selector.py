"""
Stock Selector Component - 간단한 종목 선택
"""
import streamlit as st
from typing import Optional
import sys
import os

# 현재 디렉토리를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utils.json_client import InvestSmartJSONClient


def render_stock_selector() -> Optional[str]:
    """
    종목 선택 컴포넌트 렌더링
    
    Returns:
        선택된 종목 심볼 또는 None
    """
    try:
        # data 폴더 경로 설정 (컴포넌트 기준)
        # investsmart_web/frontend/components -> investsmart_web/frontend -> data
        data_dir = os.path.join(os.path.dirname(current_dir), "data")
        data_dir = os.path.abspath(data_dir)
        json_client = InvestSmartJSONClient(data_dir)
        available_symbols = json_client.get_available_symbols()
        
        if not available_symbols:
            st.error("Cannot load stock list.")
            return None
        
        # 종목 선택
        selected_symbol = None
        
        # 실제 데이터가 있는 종목만 표시
        # 사용자 요청에 따라 종목 목록 업데이트
        symbol_display_names = {
            # 미국 주식
            "BAC": "🇺🇸 뱅크오브아메리카 (BAC)", "JPM": "🇺🇸 JP모건 (JPM)", "SBUX": "🇺🇸 스타벅스 (SBUX)", "VZ": "🇺🇸 버라이즌 (VZ)", "TSLA": "🇺🇸 테슬라 (TSLA)", "NFLX": "🇺🇸 넷플릭스 (NFLX)", "GOOGL": "🇺🇸 구글 (GOOGL)", "MSFT": "🇺🇸 마이크로소프트 (MSFT)", "V": "🇺🇸 비자 (V)", "AAPL": "🇺🇸 애플 (AAPL)", "CVX": "🇺🇸 쉐브론 (CVX)", "LOW": "🇺🇸 로우즈 (LOW)", "UNH": "🇺🇸 유나이티드헬스 (UNH)", "ORCL": "🇺🇸 오라클 (ORCL)", "AVGO": "🇺🇸 브로드컴 (AVGO)", "PLTR": "🇺🇸 팔란티어 (PLTR)", "AMD": "🇺🇸 AMD", "NVDA": "🇺🇸 엔비디아 (NVDA)", "ASML": "🇳🇱 ASML", "AMZN": "🇺🇸 아마존 (AMZN)", "LLY": "🇺🇸 일라이 릴리 (LLY)", "HD": "🇺🇸 홈디포 (HD)", "QCOM": "🇺🇸 퀄컴 (QCOM)", "MU": "🇺🇸 마이크론 (MU)", "INTC": "🇺🇸 인텔 (INTC)", "NKE": "🇺🇸 나이키 (NKE)", "JNJ": "🇺🇸 존슨앤존슨 (JNJ)", "PFE": "🇺🇸 화이자 (PFE)", "NVO": "🇩🇰 노보 노디스크 (NVO)", "ABBV": "🇺🇸 애브비 (ABBV)", "AVAV": "🇺🇸 에어로바이런먼트 (AVAV)", "AER": "🇮🇪 에어캡 홀딩스 (AER)", "LMT": "🇺🇸 록히드 마틴 (LMT)", "DHI": "🇺🇸 D.R. 호튼 (DHI)", "LEN": "🇺🇸 레나 (LEN)", "OXY": "🇺🇸 옥시덴탈 (OXY)", "TEVA": "🇮🇱 테바 (TEVA)", "VST": "🇺🇸 비스트라 (VST)", "O": "🇺🇸 리얼티인컴 (O)",
            # 미국 ETF
            "AGG": "🇺🇸 미국 채권 (AGG)", "SOXX": "🇺🇸 반도체 ETF (SOXX)", "XLP": "🇺🇸 필수재 ETF (XLP)", "XLV": "🇺🇸 헬스케어 ETF (XLV)", "XLY": "🇺🇸 경기재 ETF (XLY)", "XLC": "🇺🇸 통신 ETF (XLC)", "XLF": "🇺🇸 금융 ETF (XLF)", "XLU": "🇺🇸 유틸리티 ETF (XLU)", "XOP": "🇺🇸 가스 ETF (XOP)", "XLI": "🇺🇸 산업재 ETF (XLI)", "ITB": "🇺🇸 건설 ETF (ITB)", "GEV": "🇺🇸 변압기 ETF (GEV)", "GNOM": "🇺🇸 유전체학 ETF (GNOM)", "IDNA": "🇺🇸 유전체학 ETF (IDNA)", "ARKG": "🇺🇸 유전체학 ETF (ARKG)", "ARKK": "🇺🇸 혁신 ETF (ARKK)", "FINX": "🇺🇸 핀테크 ETF (FINX)", "SCHD": "🇺🇸 다우존스 배당 (SCHD)", "VTV": "🇺🇸 가치주 ETF (VTV)", "EFA": "🌐 선진국 주식 (EFA)", "EEM": "🌐 개도국 주식 (EEM)", "TLT": "🇺🇸 장기 채권 (TLT)", "TIPS": "🇺🇸 인플레이션 보호 채권 (TIPS)", "SHY": "🇺🇸 단기 채권 (SHY)", "LQD": "🇺🇸 미국 회사채 (LQD)", "PDBC": "🌐 원자재 액티브 (PDBC)", "VNQ": "🇺🇸 미국 리츠 (VNQ)", "JEPI": "🇺🇸 JEPI", "UNG": "🇺🇸 천연가스 선물 (UNG)", "FCG": "🇺🇸 천연가스 기업 (FCG)", "LIT": "🌐 리튬 (LIT)", "XLE": "🇺🇸 에너지/원유 (XLE)",
            # 지수
            "^KS11": "🇰🇷 코스피", "^IXIC": "🇺🇸 나스닥", "^GSPC": "🇺🇸 S&P 500", "DIA": "🇺🇸 다우존스30 (DIA)", "IWM": "🇺🇸 러셀 2000 (IWM)", "^NSEI": "🇮🇳 니프티50", "^N225": "🇯🇵 니케이225", "^HSI": "🇭🇰 항셍", "^HSCE": "🇭🇰 홍콩H", "DX-Y.NYB": "🌐 달러 인덱스", "^SOX": "🇺🇸 미국 반도체 지수",
            # 원자재
            "PA=F": "💎 팔라듐", "REMX": "🌐 희토류", "GSG": "🌐 S&P 원자재", "GC=F": "🥇 금", "SI=F": "🥈 은", "CL=F": "🛢️ 원유 WTI", "HG=F": "🥉 구리",
            # 암호화폐
            "BTC-USD": "₿ 비트코인 (BTC-USD)", "ETH-USD": "Ξ 이더리움 (ETH-USD)", "SOL-USD": "◎ 솔라나 (SOL-USD)",
            # 환율
            "USDKRW=X": "💱 USD/KRW", "JPYKRW=X": "💱 JPY/KRW", "USDJPY=X": "💱 USD/JPY", "EURKRW=X": "💱 EUR/KRW", "CNY=X": "💱 USD/CNY",
            # 기타 해외
            "SIE.DE": "🇩🇪 지멘스 (SIE.DE)", "RDW": "🇺🇸 레드와이어 (RDW)", "TEM": "🇺🇸 템플턴 이머징 (TEM)", "HLVX": "🇺🇸 할리벡스 (HLVX)",
            "148070.KS": "🇰🇷 국고채 10년", "245710.KS": "🇻🇳 VN30", "1343.T": "🇯🇵 일본 리츠 (1343.T)", "1659.T": "🇺🇸 US 리츠 (1659.T)", "2253.T": "🇯🇵 GLOBAL X 고배당 (2253.T)", "1615.T": "🇯🇵 일본 은행주 (1615.T)", "1629.T": "🇯🇵 일본 상사 (1629.T)", "371160.KS": "🇭🇰 차이나항셍테크", "1489.T": "🇯🇵 일본 고배당 (1489.T)", "1494.T": "🇯🇵 일본 귀족주 (1494.T)"
        }
        
        # 데이터가 있는 종목만 필터링
        available_options = []
        available_symbols_filtered = []
        
        for symbol in available_symbols:
            if symbol in symbol_display_names:
                available_options.append(symbol_display_names[symbol])
                available_symbols_filtered.append(symbol)
        
        if not available_options:
            st.error("Cannot load stock list.")
            return None
        
        # 종목 선택
        selected_symbol = None
        
        if available_options:
            selected_index = st.selectbox(
                "종목을 선택하세요:",
                range(len(available_options)),
                format_func=lambda x: available_options[x],
                key="stock_selector"
            )
            
            if selected_index is not None:
                selected_symbol = available_symbols_filtered[selected_index]
        
        return selected_symbol
        
    except Exception as e:
        st.error(f"종목 선택 중 오류가 발생했습니다: {e}")
        return None


def render_simple_stock_selector() -> Optional[str]:
    """
    간단한 종목 선택 (드롭다운)
    """
    try:
        # data 폴더 경로 설정 (컴포넌트 기준)
        # investsmart_web/frontend/components -> investsmart_web/frontend -> data
        data_dir = os.path.join(os.path.dirname(current_dir), "data")
        data_dir = os.path.abspath(data_dir)
        json_client = InvestSmartJSONClient(data_dir)
        available_symbols = json_client.get_available_symbols()
        
        if not available_symbols:
            st.error("Cannot load stock list.")
            return None
        
        # 실제 데이터가 있는 종목만 표시
        # 사용자 요청에 따라 종목 목록 업데이트
        symbol_display_names = {
            # 미국 주식
            "BAC": "🇺🇸 뱅크오브아메리카 (BAC)", "JPM": "🇺🇸 JP모건 (JPM)", "SBUX": "🇺🇸 스타벅스 (SBUX)", "VZ": "🇺🇸 버라이즌 (VZ)", "TSLA": "🇺🇸 테슬라 (TSLA)", "NFLX": "🇺🇸 넷플릭스 (NFLX)", "GOOGL": "🇺🇸 구글 (GOOGL)", "MSFT": "🇺🇸 마이크로소프트 (MSFT)", "V": "🇺🇸 비자 (V)", "AAPL": "🇺🇸 애플 (AAPL)", "CVX": "🇺🇸 쉐브론 (CVX)", "LOW": "🇺🇸 로우즈 (LOW)", "UNH": "🇺🇸 유나이티드헬스 (UNH)", "ORCL": "🇺🇸 오라클 (ORCL)", "AVGO": "🇺🇸 브로드컴 (AVGO)", "PLTR": "🇺🇸 팔란티어 (PLTR)", "AMD": "🇺🇸 AMD", "NVDA": "🇺🇸 엔비디아 (NVDA)", "ASML": "🇳🇱 ASML", "AMZN": "🇺🇸 아마존 (AMZN)", "LLY": "🇺🇸 일라이 릴리 (LLY)", "HD": "🇺🇸 홈디포 (HD)", "QCOM": "🇺🇸 퀄컴 (QCOM)", "MU": "🇺🇸 마이크론 (MU)", "INTC": "🇺🇸 인텔 (INTC)", "NKE": "🇺🇸 나이키 (NKE)", "JNJ": "🇺🇸 존슨앤존슨 (JNJ)", "PFE": "🇺🇸 화이자 (PFE)", "NVO": "🇩🇰 노보 노디스크 (NVO)", "ABBV": "🇺🇸 애브비 (ABBV)", "AVAV": "🇺🇸 에어로바이런먼트 (AVAV)", "AER": "🇮🇪 에어캡 홀딩스 (AER)", "LMT": "🇺🇸 록히드 마틴 (LMT)", "DHI": "🇺🇸 D.R. 호튼 (DHI)", "LEN": "🇺🇸 레나 (LEN)", "OXY": "🇺🇸 옥시덴탈 (OXY)", "TEVA": "🇮🇱 테바 (TEVA)", "VST": "🇺🇸 비스트라 (VST)", "O": "🇺🇸 리얼티인컴 (O)",
            # 미국 ETF
            "AGG": "🇺🇸 미국 채권 (AGG)", "SOXX": "🇺🇸 반도체 ETF (SOXX)", "XLP": "🇺🇸 필수재 ETF (XLP)", "XLV": "🇺🇸 헬스케어 ETF (XLV)", "XLY": "🇺🇸 경기재 ETF (XLY)", "XLC": "🇺🇸 통신 ETF (XLC)", "XLF": "🇺🇸 금융 ETF (XLF)", "XLU": "🇺🇸 유틸리티 ETF (XLU)", "XOP": "🇺🇸 가스 ETF (XOP)", "XLI": "🇺🇸 산업재 ETF (XLI)", "ITB": "🇺🇸 건설 ETF (ITB)", "GEV": "🇺🇸 변압기 ETF (GEV)", "GNOM": "🇺🇸 유전체학 ETF (GNOM)", "IDNA": "🇺🇸 유전체학 ETF (IDNA)", "ARKG": "🇺🇸 유전체학 ETF (ARKG)", "ARKK": "🇺🇸 혁신 ETF (ARKK)", "FINX": "🇺🇸 핀테크 ETF (FINX)", "SCHD": "🇺🇸 다우존스 배당 (SCHD)", "VTV": "🇺🇸 가치주 ETF (VTV)", "EFA": "🌐 선진국 주식 (EFA)", "EEM": "🌐 개도국 주식 (EEM)", "TLT": "🇺🇸 장기 채권 (TLT)", "TIPS": "🇺🇸 인플레이션 보호 채권 (TIPS)", "SHY": "🇺🇸 단기 채권 (SHY)", "LQD": "🇺🇸 미국 회사채 (LQD)", "PDBC": "🌐 원자재 액티브 (PDBC)", "VNQ": "🇺🇸 미국 리츠 (VNQ)", "JEPI": "🇺🇸 JEPI", "UNG": "🇺🇸 천연가스 선물 (UNG)", "FCG": "🇺🇸 천연가스 기업 (FCG)", "LIT": "🌐 리튬 (LIT)", "XLE": "🇺🇸 에너지/원유 (XLE)",
            # 지수
            "^KS11": "🇰🇷 코스피", "^IXIC": "🇺🇸 나스닥", "^GSPC": "🇺🇸 S&P 500", "DIA": "🇺🇸 다우존스30 (DIA)", "IWM": "🇺🇸 러셀 2000 (IWM)", "^NSEI": "🇮🇳 니프티50", "^N225": "🇯🇵 니케이225", "^HSI": "🇭🇰 항셍", "^HSCE": "🇭🇰 홍콩H", "DX-Y.NYB": "🌐 달러 인덱스", "^SOX": "🇺🇸 미국 반도체 지수",
            # 원자재
            "PA=F": "💎 팔라듐", "REMX": "🌐 희토류", "GSG": "🌐 S&P 원자재", "GC=F": "🥇 금", "SI=F": "🥈 은", "CL=F": "🛢️ 원유 WTI", "HG=F": "🥉 구리",
            # 암호화폐
            "BTC-USD": "₿ 비트코인 (BTC-USD)", "ETH-USD": "Ξ 이더리움 (ETH-USD)", "SOL-USD": "◎ 솔라나 (SOL-USD)",
            # 환율
            "USDKRW=X": "💱 USD/KRW", "JPYKRW=X": "💱 JPY/KRW", "USDJPY=X": "💱 USD/JPY", "EURKRW=X": "💱 EUR/KRW", "CNY=X": "💱 USD/CNY",
            # 기타 해외
            "SIE.DE": "🇩🇪 지멘스 (SIE.DE)", "RDW": "🇺🇸 레드와이어 (RDW)", "TEM": "🇺🇸 템플턴 이머징 (TEM)", "HLVX": "🇺🇸 할리벡스 (HLVX)",
            "148070.KS": "🇰🇷 국고채 10년", "245710.KS": "🇻🇳 VN30", "1343.T": "🇯🇵 일본 리츠 (1343.T)", "1659.T": "🇺🇸 US 리츠 (1659.T)", "2253.T": "🇯🇵 GLOBAL X 고배당 (2253.T)", "1615.T": "🇯🇵 일본 은행주 (1615.T)", "1629.T": "🇯🇵 일본 상사 (1629.T)", "371160.KS": "🇭🇰 차이나항셍테크", "1489.T": "🇯🇵 일본 고배당 (1489.T)", "1494.T": "🇯🇵 일본 귀족주 (1494.T)"
        }
        
        # 데이터가 있는 종목만 필터링
        available_options = []
        available_symbols_filtered = []
        
        for symbol in available_symbols:
            if symbol in symbol_display_names:
                available_options.append(symbol_display_names[symbol])
                available_symbols_filtered.append(symbol)
        
        if not available_options:
            st.error("Cannot load stock list.")
            return None
        
        # 드롭다운으로 선택
        selected_display = st.selectbox(
            "종목 선택",
            available_options,
            help="분석할 종목을 선택하세요."
        )
        
        # 선택된 종목의 심볼 찾기
        for i, display_name in enumerate(available_options):
            if display_name == selected_display:
                return available_symbols_filtered[i]
        
        return None
        
    except Exception as e:
        st.error(f"종목 선택 중 오류가 발생했습니다: {e}")
        return None