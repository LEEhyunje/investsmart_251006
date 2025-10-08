# -*- coding: utf-8 -*-
"""
종목 데이터 모듈
"""

STOCK_CATEGORIES = {
    "Major Indices": {
        "🇰🇷 KOSPI": "^KS11",
        "🇺🇸 NASDAQ": "^IXIC",
        "🇺🇸 S&P 500": "^GSPC",
        "🇺🇸 Dow Jones 30 (DIA)": "DIA",
        "🇺🇸 Russell 2000 (IWM)": "IWM",
        "🇮🇳 NIFTY 50": "^NSEI",
        "🇯🇵 Nikkei 225": "^N225",
        "🇭🇰 Hang Seng": "^HSI",
        "🇭🇰 Hong Kong H-shares": "^HSCE",
        "🌐 Dollar Index": "DX-Y.NYB",
        "🇺🇸 US Semiconductor Index": "^SOX",
    },
    "US Stocks": {
        "🇺🇸 Apple (AAPL)": "AAPL", "🇺🇸 Microsoft (MSFT)": "MSFT", "🇺🇸 Google (GOOGL)": "GOOGL", "🇺🇸 Amazon (AMZN)": "AMZN", "🇺🇸 NVIDIA (NVDA)": "NVDA", "🇺🇸 Tesla (TSLA)": "TSLA", "🇺🇸 Bank of America (BAC)": "BAC", "🇺🇸 JPMorgan (JPM)": "JPM", "🇺🇸 Starbucks (SBUX)": "SBUX", "🇺🇸 Verizon (VZ)": "VZ", "🇺🇸 Netflix (NFLX)": "NFLX", "🇺🇸 Visa (V)": "V", "🇺🇸 Chevron (CVX)": "CVX", "🇺🇸 Lowe's (LOW)": "LOW", "🇺🇸 UnitedHealth (UNH)": "UNH", "🇺🇸 Oracle (ORCL)": "ORCL", "🇺🇸 Broadcom (AVGO)": "AVGO", "🇺🇸 Palantir (PLTR)": "PLTR", "🇺🇸 AMD": "AMD", "🇳🇱 ASML": "ASML", "🇺🇸 Eli Lilly (LLY)": "LLY", "🇺🇸 Home Depot (HD)": "HD", "🇺🇸 Qualcomm (QCOM)": "QCOM", "🇺🇸 Micron (MU)": "MU", "🇺🇸 Intel (INTC)": "INTC", "🇺🇸 Nike (NKE)": "NKE", "🇺🇸 Johnson & Johnson (JNJ)": "JNJ", "🇺🇸 Pfizer (PFE)": "PFE", "🇩🇰 Novo Nordisk (NVO)": "NVO", "🇺🇸 AbbVie (ABBV)": "ABBV", "🇺🇸 AeroVironment (AVAV)": "AVAV", "🇮🇪 AerCap Holdings (AER)": "AER", "🇺🇸 Lockheed Martin (LMT)": "LMT", "🇺🇸 D.R. Horton (DHI)": "DHI", "🇺🇸 Lennar (LEN)": "LEN", "🇺🇸 Occidental (OXY)": "OXY", "🇮🇱 Teva (TEVA)": "TEVA", "🇺🇸 Vistra (VST)": "VST", "🇺🇸 Realty Income (O)": "O",
    },
    "US ETFs": {
        "🇺🇸 US Bonds (AGG)": "AGG", "🇺🇸 Semiconductor ETF (SOXX)": "SOXX", "🇺🇸 Consumer Staples ETF (XLP)": "XLP", "🇺🇸 Healthcare ETF (XLV)": "XLV", "🇺🇸 Consumer Discretionary ETF (XLY)": "XLY", "🇺🇸 Communication ETF (XLC)": "XLC", "🇺🇸 Financial ETF (XLF)": "XLF", "🇺🇸 Utility ETF (XLU)": "XLU", "🇺🇸 Gas ETF (XOP)": "XOP", "🇺🇸 Industrial ETF (XLI)": "XLI", "🇺🇸 Homebuilders ETF (ITB)": "ITB", "🇺🇸 Transformer ETF (GEV)": "GEV", "🇺🇸 Genomics ETF (GNOM)": "GNOM", "🇺🇸 Genomics ETF (IDNA)": "IDNA", "🇺🇸 Genomics ETF (ARKG)": "ARKG", "🇺🇸 Innovation ETF (ARKK)": "ARKK", "🇺🇸 Fintech ETF (FINX)": "FINX", "🇺🇸 Dow Jones Dividend (SCHD)": "SCHD", "🇺🇸 Value ETF (VTV)": "VTV", "🌐 Developed Markets (EFA)": "EFA", "🌐 Emerging Markets (EEM)": "EEM", "🇺🇸 Long-Term Bonds (TLT)": "TLT", "🇺🇸 TIPS Bond (TIPS)": "TIPS", "🇺🇸 Short-Term Bonds (SHY)": "SHY", "🇺🇸 Corporate Bonds (LQD)": "LQD", "🌐 Commodities Active (PDBC)": "PDBC", "🇺🇸 US REITs (VNQ)": "VNQ", "🇺🇸 JEPI": "JEPI", "🇺🇸 Natural Gas Futures (UNG)": "UNG", "🇺🇸 Natural Gas Companies (FCG)": "FCG", "🌐 Lithium (LIT)": "LIT", "🇺🇸 Energy/Oil (XLE)": "XLE",
    },
    "Commodities / Crypto / FX": {
        "💎 Palladium": "PA=F", "🌐 Rare Earth": "REMX", "🌐 S&P Commodities": "GSG", "🥇 Gold": "GC=F", "🥈 Silver": "SI=F", "🛢️ WTI Crude Oil": "CL=F", "🥉 Copper": "HG=F",
        "₿ Bitcoin (BTC-USD)": "BTC-USD", "Ξ Ethereum (ETH-USD)": "ETH-USD", "◎ Solana (SOL-USD)": "SOL-USD",
        "💱 USD/KRW": "USDKRW=X", "💱 JPY/KRW": "JPYKRW=X", "💱 USD/JPY": "USDJPY=X", "💱 EUR/KRW": "EURKRW=X", "💱 USD/CNY": "CNY=X",
    },
    "Other International": {
        "🇩🇪 Siemens (SIE.DE)": "SIE.DE", "🇺🇸 Redwire (RDW)": "RDW", "🇺🇸 Templeton Emerging (TEM)": "TEM", "🇺🇸 Hallivax (HLVX)": "HLVX",
        "🇰🇷 Korea Treasury 10Y": "148070.KS", "🇻🇳 VN30": "245710.KS", "🇯🇵 Japan REIT (1343.T)": "1343.T", "🇺🇸 US REIT (1659.T)": "1659.T", "🇯🇵 GLOBAL X High Dividend (2253.T)": "2253.T", "🇯🇵 Japan Bank ETF (1615.T)": "1615.T", "🇯🇵 Japan Trading Co. ETF (1629.T)": "1629.T", "🇭🇰 China Hang Seng Tech": "371160.KS", "🇯🇵 Japan High Dividend (1489.T)": "1489.T", "🇯🇵 Japan Dividend Aristocrats (1494.T)": "1494.T"
    }
}