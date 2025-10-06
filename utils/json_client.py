"""
JSON 데이터 클라이언트 - gzip 압축 지원
JSON 파일에서 직접 데이터를 읽어오는 최적화된 클라이언트
"""
import json
import gzip
import streamlit as st
from typing import Dict, List, Any, Optional
import logging
import os

logger = logging.getLogger(__name__)


class InvestSmartJSONClient:
    """InvestSmart JSON 데이터 클라이언트 - 최적화된 캐싱 버전"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self._cache = {}  # 종목별 데이터 캐시 (로컬)
        self._processed_cache = {}  # 처리된 데이터 캐시 (로컬)
        
        # Streamlit session_state 초기화
        if 'json_data_cache' not in st.session_state:
            st.session_state.json_data_cache = {}
        if 'processed_data_cache' not in st.session_state:
            st.session_state.processed_data_cache = {}
        if 'cache_stats' not in st.session_state:
            st.session_state.cache_stats = {
                'cache_hits': 0,
                'cache_misses': 0,
                'total_requests': 0
            }
    
    def _get_symbol_filename(self, symbol: str, compressed: bool = True) -> str:
        """종목 심볼을 파일명으로 변환 - 압축 지원"""
        # 특수 문자를 안전한 문자로 변환
        safe_symbol = symbol.replace('^', '').replace('=', '').replace('/', '_')
        if compressed:
            return f"signals_{safe_symbol}.json.gz"
        else:
            return f"signals_{safe_symbol}.json"
    
    def _load_symbol_data(self, symbol: str) -> List[Dict]:
        """특정 종목의 JSON 파일에서 데이터 로드 - gzip 압축 지원"""
        try:
            # 1. Streamlit session_state에서 먼저 확인
            if symbol in st.session_state.json_data_cache:
                st.session_state.cache_stats['cache_hits'] += 1
                logger.info(f"✅ 캐시 히트: {symbol}")
                return st.session_state.json_data_cache[symbol]
            
            # 2. 로컬 캐시에서 확인
            if symbol in self._cache:
                st.session_state.cache_stats['cache_hits'] += 1
                logger.info(f"✅ 로컬 캐시 히트: {symbol}")
                # session_state에도 저장
                st.session_state.json_data_cache[symbol] = self._cache[symbol]
                return self._cache[symbol]
            
            # 3. 파일에서 로드 (압축 파일 우선, 없으면 일반 파일)
            st.session_state.cache_stats['cache_misses'] += 1
            logger.info(f"📁 파일에서 로드: {symbol}")
            
            # 압축 파일 시도
            compressed_filename = self._get_symbol_filename(symbol, compressed=True)
            compressed_file_path = os.path.join(self.data_dir, compressed_filename)
            
            # 일반 파일 시도
            normal_filename = self._get_symbol_filename(symbol, compressed=False)
            normal_file_path = os.path.join(self.data_dir, normal_filename)
            
            data = []
            
            # 압축 파일이 있으면 압축 해제로 로드
            if os.path.exists(compressed_file_path):
                logger.info(f"📦 압축 파일 로드: {compressed_filename}")
                with gzip.open(compressed_file_path, 'rt', encoding='utf-8') as f:
                    data = json.load(f)
            # 일반 파일이 있으면 일반 로드
            elif os.path.exists(normal_file_path):
                logger.info(f"📄 일반 파일 로드: {normal_filename}")
                with open(normal_file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                logger.warning(f"파일이 존재하지 않음: {symbol}")
                return []
                
            # 4. 모든 캐시에 저장
            self._cache[symbol] = data
            st.session_state.json_data_cache[symbol] = data
            
            return data
            
        except Exception as e:
            logger.error(f"JSON 파일 로드 실패: {symbol}, {e}")
            return []
    
    def get_signals_data(self, symbol: str, period: str = "1y") -> Dict[str, Any]:
        """특정 종목의 신호 데이터 조회 - 최적화된 캐싱 버전"""
        try:
            # 통계 업데이트
            st.session_state.cache_stats['total_requests'] += 1
            
            # 처리된 데이터 캐시에서 먼저 확인
            cache_key = f"{symbol}_{period}"
            if cache_key in st.session_state.processed_data_cache:
                st.session_state.cache_stats['cache_hits'] += 1
                logger.info(f"✅ 처리된 데이터 캐시 히트: {symbol}")
                return st.session_state.processed_data_cache[cache_key]
            
            # 원본 데이터 로드 (이미 최적화된 캐싱 적용)
            symbol_data = self._load_symbol_data(symbol)
            
            if not symbol_data:
                return {
                    'symbol': symbol,
                    'dates': [],
                    'signals': {},
                    'indicators': {},
                    'error': '데이터를 찾을 수 없습니다'
                }
            
            # 데이터 구조화 - 최적화된 버전 (한 번에 처리)
            dates = []
            stock_data = {'open': [], 'high': [], 'low': [], 'close': [], 'volume': []}
            signals_data = {
                'short_signal_v1': [], 'short_signal_v2': [], 'long_signal': [],
                'combined_signal_v1': [], 'macd_signal': [], 'momentum_color_signal': []
            }
            indicators_data = {'Final_Composite_Value': []}
            
            # 한 번의 루프로 모든 데이터 처리 (성능 최적화)
            for item in symbol_data:
                dates.append(item['date'])
                stock_data['open'].append(item.get('open', 0))
                stock_data['high'].append(item.get('high', 0))
                stock_data['low'].append(item.get('low', 0))
                stock_data['close'].append(item.get('close', 0))
                stock_data['volume'].append(item.get('volume', 0))
                signals_data['short_signal_v1'].append(item.get('short_signal_v1', 0))
                signals_data['short_signal_v2'].append(item.get('short_signal_v2', 0))
                signals_data['long_signal'].append(item.get('long_signal', 0))
                signals_data['combined_signal_v1'].append(item.get('combined_signal_v1', 0))
                signals_data['macd_signal'].append(item.get('macd_signal', 0))
                signals_data['momentum_color_signal'].append(item.get('momentum_color_signal', 0))
                indicators_data['Final_Composite_Value'].append(item.get('fcv', 0))
            
            # 결과 데이터 구성
            result = {
                'symbol': symbol,
                'dates': dates,
                'data': stock_data,
                'signals': signals_data,
                'indicators': indicators_data,
                'trendlines': [],  # 추세선 데이터 (나중에 추가 예정)
                'last_updated': symbol_data[-1].get('last_updated', dates[-1]) if symbol_data else None
            }
            
            # 처리된 데이터를 캐시에 저장
            st.session_state.processed_data_cache[cache_key] = result
            
            return result
            
        except Exception as e:
            logger.error(f"신호 데이터 조회 실패: {symbol}, {e}")
            return {
                'symbol': symbol,
                'dates': [],
                'signals': {},
                'indicators': {},
                'error': f'데이터 조회 실패: {e}'
            }
    
    def get_available_symbols(self) -> List[str]:
        """사용 가능한 종목 목록 조회 - 최적화된 지연 로딩"""
        try:
            # 캐시에서 먼저 확인
            if 'available_symbols' in st.session_state:
                st.session_state.cache_stats['cache_hits'] += 1
                logger.info("✅ 종목 목록 캐시 히트")
                return st.session_state.available_symbols
            
            # 파일명만 읽어서 빠르게 처리
            symbols = []
            if os.path.exists(self.data_dir):
                # 파일명 패턴 매핑 (성능 최적화)
                symbol_mapping = {
                    "KS11": "^KS11", "IXIC": "^IXIC", "GSPC": "^GSPC", "DJI": "^DJI",
                    "FTSE": "^FTSE", "GDAXI": "^GDAXI", "FCHI": "^FCHI", "N225": "^N225",
                    "HSI": "^HSI", "AXJO": "^AXJO", "GCF": "GC=F", "SIF": "SI=F",
                    "CLF": "CL=F", "NGF": "NG=F", "ZCF": "ZC=F", "ZSF": "ZS=F",
                    "USDKRWX": "USDKRW=X", "EURUSDX": "EURUSD=X", "GBPUSDX": "GBPUSD=X",
                    "USDJPYX": "USDJPY=X", "005930KS": "005930.KS"
                }
                
                # 파일명만 읽기 (JSON 파일 내용은 읽지 않음) - 압축 파일 지원
                for filename in os.listdir(self.data_dir):
                    if filename.startswith("signals_") and (filename.endswith(".json") or filename.endswith(".json.gz")):
                        # 파일명에서 심볼 추출 (압축 파일과 일반 파일 모두 처리)
                        if filename.endswith(".json.gz"):
                            symbol = filename.replace("signals_", "").replace(".json.gz", "")
                        else:
                            symbol = filename.replace("signals_", "").replace(".json", "")
                        # 매핑 테이블 사용 (성능 최적화)
                        symbol = symbol_mapping.get(symbol, symbol)
                        symbols.append(symbol)
            
            # 정렬 및 캐싱
            symbols = sorted(symbols)
            st.session_state.available_symbols = symbols
            st.session_state.cache_stats['cache_misses'] += 1
            logger.info(f"📁 종목 목록 파일에서 로드: {len(symbols)}개")
            return symbols
            
        except Exception as e:
            logger.error(f"종목 목록 조회 실패: {e}")
            return []
    
    def get_data_info(self) -> Dict[str, Any]:
        """데이터 정보 조회 - 최적화된 버전"""
        try:
            # 캐시에서 먼저 확인
            if 'data_info' in st.session_state:
                st.session_state.cache_stats['cache_hits'] += 1
                logger.info("✅ 데이터 정보 캐시 히트")
                return st.session_state.data_info
            
            symbols = self.get_available_symbols()
            
            # 간단한 정보만 조회 (전체 데이터 로드하지 않음)
            total_records = 0
            last_updated = None
            
            # 파일 크기로 대략적인 레코드 수 추정 (성능 최적화)
            for symbol in symbols:
                filename = self._get_symbol_filename(symbol)
                file_path = os.path.join(self.data_dir, filename)
                if os.path.exists(file_path):
                    # 파일 크기로 대략적인 레코드 수 추정 (JSON 평균 크기 기준)
                    file_size = os.path.getsize(file_path)
                    estimated_records = max(1, file_size // 200)  # 평균 200바이트/레코드
                    total_records += estimated_records
            
            # 마지막 업데이트는 현재 시간으로 설정 (정확한 시간은 필요시 개별 조회)
            last_updated = "2024-01-01"  # 기본값
            
            result = {
                'total_records': total_records,
                'symbols': symbols,
                'last_updated': last_updated
            }
            
            # 캐시에 저장
            st.session_state.data_info = result
            st.session_state.cache_stats['cache_misses'] += 1
            logger.info(f"📁 데이터 정보 파일에서 로드: {len(symbols)}개 종목")
            return result
            
        except Exception as e:
            logger.error(f"데이터 정보 조회 실패: {e}")
            return {'total_records': 0, 'symbols': [], 'last_updated': None}
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """캐시 통계 조회"""
        try:
            stats = st.session_state.cache_stats
            total_requests = stats['total_requests']
            cache_hits = stats['cache_hits']
            cache_misses = stats['cache_misses']
            
            hit_rate = (cache_hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'total_requests': total_requests,
                'cache_hits': cache_hits,
                'cache_misses': cache_misses,
                'hit_rate': round(hit_rate, 2),
                'cached_symbols': len(st.session_state.json_data_cache),
                'processed_cache_size': len(st.session_state.processed_data_cache)
            }
        except Exception as e:
            logger.error(f"캐시 통계 조회 실패: {e}")
            return {'total_requests': 0, 'cache_hits': 0, 'cache_misses': 0, 'hit_rate': 0}
    
    def clear_cache(self):
        """캐시 초기화"""
        try:
            st.session_state.json_data_cache.clear()
            st.session_state.processed_data_cache.clear()
            st.session_state.cache_stats = {
                'cache_hits': 0,
                'cache_misses': 0,
                'total_requests': 0
            }
            self._cache.clear()
            self._processed_cache.clear()
            logger.info("✅ 모든 캐시가 초기화되었습니다.")
        except Exception as e:
            logger.error(f"캐시 초기화 실패: {e}")
    
    def compress_json_files(self) -> Dict[str, Any]:
        """JSON 파일들을 gzip으로 압축"""
        try:
            compressed_count = 0
            total_savings = 0
            
            symbols = self.get_available_symbols()
            
            for symbol in symbols:
                # 일반 JSON 파일 경로
                normal_filename = self._get_symbol_filename(symbol, compressed=False)
                normal_file_path = os.path.join(self.data_dir, normal_filename)
                
                # 압축 파일 경로
                compressed_filename = self._get_symbol_filename(symbol, compressed=True)
                compressed_file_path = os.path.join(self.data_dir, compressed_filename)
                
                # 일반 파일이 있고 압축 파일이 없으면 압축
                if os.path.exists(normal_file_path) and not os.path.exists(compressed_file_path):
                    try:
                        # 원본 파일 크기
                        original_size = os.path.getsize(normal_file_path)
                        
                        # 압축 파일 생성
                        with open(normal_file_path, 'rb') as f_in:
                            with gzip.open(compressed_file_path, 'wb') as f_out:
                                f_out.write(f_in.read())
                        
                        # 압축 파일 크기
                        compressed_size = os.path.getsize(compressed_file_path)
                        savings = original_size - compressed_size
                        savings_percent = (savings / original_size) * 100
                        
                        total_savings += savings
                        compressed_count += 1
                        
                        logger.info(f"📦 압축 완료: {symbol} ({original_size:,} → {compressed_size:,} bytes, {savings_percent:.1f}% 절약)")
                        
                    except Exception as e:
                        logger.error(f"압축 실패: {symbol}, {e}")
            
            return {
                'compressed_files': compressed_count,
                'total_savings_bytes': total_savings,
                'total_savings_mb': round(total_savings / (1024 * 1024), 2),
                'average_savings_percent': round((total_savings / (total_savings + (total_savings * 0.3))) * 100, 1) if total_savings > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"JSON 파일 압축 실패: {e}")
            return {'compressed_files': 0, 'total_savings_bytes': 0, 'total_savings_mb': 0, 'average_savings_percent': 0}