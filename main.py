import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("영화 데이터 그래프 도감 1 - 시간")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


# -----------------------------
# 데이터 불러오기
# -----------------------------
@st.cache_data
def load_data():
    # encoding="utf-8-sig" : 파일 맨 앞의 BOM(숨은 문자) 때문에
    # 첫 번째 열 이름이 "날짜"가 아니라 "﻿날짜"로 읽히는 문제를 방지
    df = pd.read_csv(DATA_URL, encoding="utf-8-sig")

    # 혹시 모를 열 이름 앞뒤 공백도 함께 제거
    df.columns = df.columns.str.strip()

    # 날짜 열을 진짜 날짜(datetime)로 변환 (예: 20230101 -> 2023-01-01)
    df["날짜"] = pd.to_datetime(df["날짜"].astype(str).str.strip(), format="%Y%m%d")

    return df


try:
    df = load_data()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()


# -----------------------------
# 구역 1. 영화별 일별 관객수 변화
# -----------------------------
st.header("구역 1. 영화별 일별 관객수 변화")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list)

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"'{selected_movie}' 일별 관객수 변화",
    labels={"날짜": "날짜", "일관객": "일일 관객수"},
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일일 관객수: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

st.plotly_chart(fig1, use_container_width=True)

st.caption("💡 이 그래프로 알 수 있는 것: ")


st.divider()


# -----------------------------
# 구역 2. (다음 그래프를 위한 자리)
# -----------------------------
st.header("구역 2. (준비 중)")
st.info("다음 그래프가 이곳에 추가될 예정입니다.")

st.divider()


# -----------------------------
# 구역 3. (다음 그래프를 위한 자리)
# -----------------------------
st.header("구역 3. (준비 중)")
st.info("다음 그래프가 이곳에 추가될 예정입니다.")
