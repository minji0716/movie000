import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 기본 설정
# -----------------------------------------------------------------------------
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL, dtype={"날짜": str})
    # 날짜 열(하이픈 없는 여덟 자리 숫자)을 진짜 datetime으로 변환
    df["날짜"] = pd.to_datetime(df["날짜"], format="%Y%m%d")
    return df


df = load_data()

st.title("영화 데이터 그래프 도감 1 - 시간")
st.caption("일별 박스오피스 10위권 기록(1년치)을 시간의 흐름에 따라 살펴보는 그래프 모음입니다.")

st.divider()

# =============================================================================
# 구역 1. 영화별 일관객 추이
# =============================================================================
st.header("1. 영화별 일관객 추이")

movie_list = sorted(df["영화명"].unique())
selected_movie = st.selectbox("영화를 선택하세요", movie_list, key="movie_select_1")

movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    labels={"날짜": "날짜", "일관객": "일일 관객 수"},
    title=f"'{selected_movie}' 일별 관객 수 변화",
)
fig1.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra></extra>"
)
fig1.update_layout(hovermode="x unified")

st.plotly_chart(fig1, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 문장을 적어 주세요)")

st.divider()

# =============================================================================
# 구역 2. 일관객 합계 상위 5편 비교
# =============================================================================
st.header("2. 일관객 합계 상위 5편의 날짜별 추이 비교")

top5_movies = (
    df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).head(5).index
)
top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    labels={"날짜": "날짜", "일관객": "일일 관객 수", "영화명": "영화명"},
    title="일관객 합계 상위 5편 비교",
)
fig2.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>일관객: %{y:,}명<extra>%{fullData.name}</extra>"
)
fig2.update_layout(hovermode="x unified", legend_title_text="영화명 (클릭하여 켜기/끄기)")

st.plotly_chart(fig2, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 문장을 적어 주세요)")

st.divider()

# =============================================================================
# 구역 3. 날짜별 10위권 일관객 합계 추이
# =============================================================================
st.header("3. 날짜별 10위권 일관객 합계 추이")

daily_total = df.groupby("날짜", as_index=False)["일관객"].sum()
daily_total = daily_total.sort_values("날짜")

fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    labels={"날짜": "날짜", "일관객": "일관객 합계"},
    title="날짜별 10위권 일관객 합계",
)
fig3.update_traces(
    hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra></extra>"
)
fig3.update_layout(hovermode="x unified")

# 합계가 가장 컸던 날 3일 표시
top3_days = daily_total.sort_values("일관객", ascending=False).head(3)

for _, row in top3_days.iterrows():
    fig3.add_annotation(
        x=row["날짜"],
        y=row["일관객"],
        text=row["날짜"].strftime("%Y-%m-%d"),
        showarrow=True,
        arrowhead=2,
        yshift=10,
        font=dict(size=11, color="red"),
    )
    fig3.add_trace(
        px.scatter(x=[row["날짜"]], y=[row["일관객"]]).data[0].update(
            marker=dict(color="red", size=10, symbol="star"),
            showlegend=False,
            hovertemplate="날짜: %{x|%Y-%m-%d}<br>합계: %{y:,}명<extra>최고 흥행일</extra>",
        )
    )

st.plotly_chart(fig3, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 문장을 적어 주세요)")

st.divider()

# =============================================================================
# 구역 4. 일관객 합계 TOP 10 영화
# =============================================================================
st.header("4. 일관객 합계 TOP 10 영화")

movie_summary = (
    df.groupby("영화명")
    .agg(총관객=("일관객", "sum"), 등장일수=("날짜", "count"))
    .reset_index()
)
top10_movies = movie_summary.sort_values("총관객", ascending=False).head(10)
# 관객이 많은 영화가 위에 오도록 정렬 (막대그래프는 아래→위로 그려지므로 오름차순 정렬)
top10_movies = top10_movies.sort_values("총관객", ascending=True)

fig4 = px.bar(
    top10_movies,
    x="총관객",
    y="영화명",
    orientation="h",
    labels={"총관객": "일관객 합계", "영화명": "영화명"},
    title="일관객 합계 TOP 10 영화",
    custom_data=["등장일수"],
)
fig4.update_traces(
    hovertemplate="영화명: %{y}<br>일관객 합계: %{x:,}명<br>10위권 등장일수: %{customdata[0]}일<extra></extra>"
)

st.plotly_chart(fig4, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 문장을 적어 주세요)")

st.divider()

# =============================================================================
# 구역 5. 월 × 요일별 일관객 합계 히트맵
# =============================================================================
st.header("5. 월 × 요일별 일관객 합계 히트맵")

df["월"] = df["날짜"].dt.month
df["요일"] = df["날짜"].dt.dayofweek  # 0=월요일 ... 6=일요일

weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
df["요일명"] = df["요일"].map(dict(enumerate(weekday_names)))

heatmap_data = (
    df.groupby(["월", "요일명"])["일관객"].sum().reset_index()
)

# 월 1~12, 요일 월~일 순서로 피벗
heatmap_pivot = heatmap_data.pivot(index="월", columns="요일명", values="일관객")
heatmap_pivot = heatmap_pivot.reindex(columns=weekday_names)
heatmap_pivot = heatmap_pivot.reindex(index=range(1, 13))

fig5 = px.imshow(
    heatmap_pivot,
    labels=dict(x="요일", y="월", color="일관객 합계"),
    x=weekday_names,
    y=[f"{m}월" for m in range(1, 13)],
    color_continuous_scale="Reds",
    aspect="auto",
    title="월 × 요일별 일관객 합계",
)
fig5.update_traces(
    hovertemplate="월: %{y}<br>요일: %{x}<br>합계: %{z:,}명<extra></extra>"
)

st.plotly_chart(fig5, use_container_width=True)

st.info("💡 이 그래프로 알 수 있는 것: (여기에 문장을 적어 주세요)")

st.divider()

# =============================================================================
# 구역 6. (다음 그래프를 위한 자리)
# =============================================================================
st.header("6. 다음 그래프 (추가 예정)")

st.write("여기에 새로운 그래프를 추가할 예정입니다.")

# st.plotly_chart(...)
# st.info("💡 이 그래프로 알 수 있는 것: ")
