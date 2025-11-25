# streamlit Code

# ==================================================
# 🚗 교통사고 데이터 분석 Streamlit 앱 (디자인 강화 + 주석 포함)
# ==================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------
# ✅ Streamlit 페이지 기본 설정
# -------------------------------
st.set_page_config(
    page_title="교통사고 통계 분석",   # 브라우저 탭 제목
    page_icon="🚗",                  # 탭 아이콘
    layout="wide"                    # 와이드 레이아웃
)

# -------------------------------
# 🎨 사용자 정의 CSS 스타일
# -------------------------------
st.markdown("""
    <style>
    /* ====== 전체 페이지 배경 ====== */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(180deg, #eaf4fc 0%, #ffffff 80%);
    }

    /* ====== 사이드바 스타일 ====== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1f3b73, #3a7bd5);
        color: #0d47a1;  /* 글씨 파란색 계열로 변경 */
    }

    /* 사이드바 안의 텍스트 및 선택 항목 색상 수정 */
    [data-testid="stSidebar"] * {
        color: black !important;  /* 전체 사이드바 텍스트 파란색 */
        font-weight: bold;
    }

    /* selectbox, radio, multiselect 배경 흰색으로 지정 */
    [data-testid="stSidebar"] .stSelectbox div,
    [data-testid="stSidebar"] .stMultiSelect div,
    [data-testid="stSidebar"] .stRadio div {
        background-color: #f5f5f5 !important;
        color: #0d47a1;
        border-radius: 5px;
        padding: 3px 5px;
    }

    /* ====== 제목 색상 ====== */
    h1, h2, h3 {
        color: #2C3E50;
    }

    /* ====== 데이터프레임 영역 ====== */
    .stDataFrame {
        border: 1px solid #ccddee;
        border-radius: 10px;
        overflow: hidden;
    }

    /* ====== 성공 메시지 색상 변경 ====== */
    .stSuccess {
        background-color: #eaf8f0 !important;
        border-left: 6px solid #34c759 !important;
    }

    /* ====== 구분선 스타일 ====== */
    hr {
        border: 1px solid #d3d3d3;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
# 📂 CSV 파일 로드
# -------------------------------
DATA_PATH = "한국도로교통공단_시도 시군구별 교통사고 통계_20241231.csv"

# 파일 존재 여부 확인
if not os.path.exists(DATA_PATH):
    st.error(f"🚨 '{DATA_PATH}' 파일이 없습니다.\n같은 폴더에 CSV 파일을 넣어주세요.")
    st.stop()

# 인코딩 자동 감지 (cp949 또는 utf-8)
try:
    df = pd.read_csv(DATA_PATH, encoding="cp949")
except:
    df = pd.read_csv(DATA_PATH, encoding="utf-8")

# -------------------------------
# ➕ 총 피해자수 컬럼 생성
# -------------------------------
df["총 피해자수"] = df["사망자수"] + df["중상자수"] + df["경상자수"] + df["부상신고자수"]

# -------------------------------
# 🚦 사이드바 메뉴 구성
# -------------------------------
st.sidebar.title("🚦 교통사고 데이터 분석")
# 사이드바 상단 아이콘 이미지
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3182/3182767.png", use_container_width=True)

# 메뉴 선택 박스
menu = st.sidebar.selectbox(
    "메뉴를 선택하세요",
    ["🏠 홈", "📊 시도별 비교", "🏙️ 시군구별 비교", "⚰️ 사망률 분석"]
)

# -------------------------------
# 🏠 홈 화면
# -------------------------------
if menu == "🏠 홈":
    st.title("🚗 교통사고 데이터 분석 대시보드")

    # 유튜브 영상 직접 삽입 (주신 링크)
    st.video("https://youtu.be/lnEmRXFU_Yo?si=PmF5lLQnNYvd9JK4")

    # 대시보드 소개
    st.markdown("""
    <br>
    이 대시보드는 **2024년 한국 도로교통공단 교통사고 통계**를 기반으로  
    전국 **시도 및 시군구별 교통사고 현황**을 분석하고 시각화합니다.

    ---
    ### 🧭 주요 기능 안내
    - 📊 **시도별 비교** : 전국 각 시도의 사고 건수, 사망자수, 피해자수 비교  
    - 🏙️ **시군구별 비교** : 특정 시도의 시군구별 교통사고 현황 분석  
    - ⚰️ **사망률 분석** : 사고 대비 사망자 비율로 위험 지역 파악  

    """, unsafe_allow_html=True)

    st.success("💡 왼쪽 메뉴에서 분석 항목을 선택하세요!")


# -------------------------------
# 📊 시도별 비교 화면
# -------------------------------
elif menu == "📊 시도별 비교":
    st.title("📊 시도별 교통사고 통계 비교")
    st.markdown("---")

    # y축 선택
    y_option = st.selectbox("y축으로 표시할 데이터 선택", ["총 피해자수", "사고건수", "사망자수"])
    # 정렬 옵션 선택
    sort_mode = st.radio("정렬 방식 선택", ["입력 순서대로", "오름차순", "내림차순"])

    # 시도 선택
    selected_cities = st.multiselect(
        "비교할 시도를 선택하세요",
        options=df["시도"].unique(),
        default=df["시도"].unique()
    )

    # 선택한 시도들만 필터링
    if selected_cities:
        filtered = df[df["시도"].isin(selected_cities)]
        grouped = filtered.groupby("시도")[["사고건수", "사망자수", "총 피해자수"]].sum().reset_index()

        # 데이터 테이블 표시
        st.dataframe(grouped)

        # 정렬 리스트 생성
        if sort_mode == "입력 순서대로":
            sort_list = selected_cities
        elif sort_mode == "오름차순":
            sort_list = grouped.sort_values(y_option, ascending=True)["시도"].tolist()
        else:
            sort_list = grouped.sort_values(y_option, ascending=False)["시도"].tolist()

        # Plotly 막대그래프
        fig = px.bar(
            grouped,
            x="시도",
            y=y_option,
            color="사망자수",
            color_continuous_scale="Reds",
            text=y_option,
            labels={y_option: y_option, "시도": "시도"},
            title=f"시도별 {y_option} 비교"
        )
        # x축 정렬
        fig.update_xaxes(categoryorder='array', categoryarray=sort_list)
        # 그래프 배경 스타일
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(size=14)
        )
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# 🏙️ 시군구별 비교 화면
# -------------------------------
elif menu == "🏙️ 시군구별 비교":
    st.title("🏙️ 시군구별 교통사고 비교")
    st.markdown("---")

    # y축 선택
    y_option = st.selectbox("y축으로 표시할 데이터 선택", ["총 피해자수", "사고건수", "사망자수"], key="y_district")
    # 정렬 옵션
    sort_mode = st.radio("정렬 방식 선택", ["입력 순서대로", "오름차순", "내림차순"], key="district_sort")

    # 시도 선택
    selected_city = st.selectbox("시도를 선택하세요", df["시도"].unique())
    filtered_city = df[df["시도"] == selected_city]

    # 시군구 선택
    selected_districts = st.multiselect(
        "비교할 시군구를 선택하세요",
        options=filtered_city["시군구"].unique(),
        default=filtered_city["시군구"].unique()
    )

    # 선택된 시군구 데이터 필터링
    if selected_districts:
        filtered = filtered_city[filtered_city["시군구"].isin(selected_districts)]

        # 데이터 표시
        st.dataframe(filtered[["시군구", "사고건수", "사망자수", "총 피해자수"]])

        # 정렬 리스트 생성
        if sort_mode == "입력 순서대로":
            sort_list = selected_districts
        elif sort_mode == "오름차순":
            sort_list = filtered.sort_values(y_option, ascending=True)["시군구"].tolist()
        else:
            sort_list = filtered.sort_values(y_option, ascending=False)["시군구"].tolist()

        # Plotly 그래프
        fig = px.bar(
            filtered,
            x="시군구",
            y=y_option,
            color="사망자수",
            color_continuous_scale="Reds",
            text=y_option,
            labels={y_option: y_option, "시군구": "시군구"},
            title=f"{selected_city} 시군구별 {y_option} 비교"
        )
        fig.update_xaxes(categoryorder='array', categoryarray=sort_list)
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# ⚰️ 사망률 분석 화면
# -------------------------------
elif menu == "⚰️ 사망률 분석":
    st.title("⚰️ 시도별 사망률 분석")
    st.markdown("---")

    # 시도별 사고건수 및 사망자수 집계
    df_grouped = df.groupby("시도", as_index=False)[["사고건수", "사망자수"]].sum()
    df_grouped["사망률(%)"] = (df_grouped["사망자수"] / df_grouped["사고건수"]) * 100
    df_sorted = df_grouped.sort_values("사망률(%)", ascending=False)

    # 데이터 표시
    st.dataframe(df_sorted)

    # 막대그래프 시각화
    fig = px.bar(
        df_sorted,
        x="시도",
        y="사망률(%)",
        color="사망률(%)",
        color_continuous_scale="Reds",
        text="사망률(%)",
        labels={"사망률(%)": "사망률(%)", "시도": "시도"},
        title="시도별 사망률"
    )
    fig.update_layout(plot_bgcolor="white", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

    # 최고 사망률 지역 표시
    top = df_sorted.iloc[0]
    st.success(f"📍 **사망률이 가장 높은 지역:** {top['시도']} ({top['사망률(%)']:.2f}%)")
