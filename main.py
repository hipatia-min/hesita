import streamlit as st
import math
import random
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="다기능 웹앱", page_icon="🧮")


# -----------------------------
# 1. 계산기 앱
# -----------------------------
def calculator_app():
    st.title("🧮 다기능 계산기")
    st.write("사칙연산, 모듈러, 지수, 로그 연산을 지원하는 웹 계산기입니다.")

    # 연산 선택
    operation = st.selectbox(
        "연산을 선택하세요",
        (
            "덧셈 (+)",
            "뺄셈 (-)",
            "곱셈 (×)",
            "나눗셈 (÷)",
            "모듈러 (%)",
            "지수 (a^b)",
            "로그 (log_b(a))",
        ),
    )

    col1, col2 = st.columns(2)

    # 로그 연산은 진수(a)와 밑(b) 의미가 있으므로 라벨을 다르게 표시
    if operation == "로그 (log_b(a))":
        with col1:
            a = st.number_input("진수 a (log_b(a)에서 a)", value=1.0)
        with col2:
            b = st.number_input("밑 b (log_b(a)에서 b)", value=10.0)
    else:
        with col1:
            a = st.number_input("첫 번째 숫자 a", value=0.0)
        with col2:
            b = st.number_input("두 번째 숫자 b", value=0.0)

    if st.button("계산하기"):
        result = None

        # 연산별 처리
        if operation == "덧셈 (+)":
            result = a + b

        elif operation == "뺄셈 (-)":
            result = a - b

        elif operation == "곱셈 (×)":
            result = a * b

        elif operation == "나눗셈 (÷)":
            if b == 0:
                st.error("0으로 나눌 수 없습니다.")
            else:
                result = a / b

        elif operation == "모듈러 (%)":
            if b == 0:
                st.error("0으로 모듈러 연산을 할 수 없습니다.")
            else:
                result = a % b

        elif operation == "지수 (a^b)":
            try:
                result = a ** b
            except OverflowError:
                st.error("지수 연산 결과가 너무 커서 계산할 수 없습니다.")

        elif operation == "로그 (log_b(a))":
            # 로그 정의역 검증
            if a <= 0:
                st.error("진수 a는 0보다 커야 합니다.")
            elif b <= 0 or b == 1:
                st.error("밑 b는 0보다 크고 1이 아니어야 합니다.")
            else:
                try:
                    result = math.log(a, b)
                except ValueError:
                    st.error("로그를 계산할 수 없는 값입니다.")
                except OverflowError:
                    st.error("로그 연산 중 오버플로우가 발생했습니다.")

        # 결과 출력
        if result is not None:
            st.success(f"결과: {result}")


# -----------------------------
# 2. 확률 시뮬레이터 앱
# -----------------------------
def probability_simulator_app():
    st.title("🎲 확률 시뮬레이터")
    st.write("동전/주사위를 여러 번 던져 보고, 실제 결과 분포를 그래프로 확인해 보세요.")

    exp_type = st.selectbox("실험 종류를 선택하세요", ("동전 던지기", "주사위 던지기"))
    n_trials = st.number_input(
        "시행 횟수(양의 정수)",
        min_value=1,
        max_value=100_000,
        value=1_000,
        step=1,
    )

    if st.button("시뮬레이션 실행"):
        n_trials = int(n_trials)

        # 시뮬레이션 실행
        if exp_type == "동전 던지기":
            outcomes = [random.choice(["앞면", "뒷면"]) for _ in range(n_trials)]
            labels = ["앞면", "뒷면"]  # 이 순서대로 그래프에 표시
        else:  # 주사위 던지기
            outcomes = [random.randint(1, 6) for _ in range(n_trials)]
            labels = [1, 2, 3, 4, 5, 6]

        # 결과 집계
        counts = {label: 0 for label in labels}
        for o in outcomes:
            counts[o] += 1

        # 데이터프레임 생성
        df = pd.DataFrame(
            {
                "결과": [str(l) for l in labels],
                "횟수": [counts[l] for l in labels],
            }
        )
        df["상대도수"] = df["횟수"] / n_trials

        st.subheader("📊 결과 요약")
        st.dataframe(df, use_container_width=True)

        # 막대그래프 (횟수 기준)
        fig = px.bar(
            df,
            x="결과",
            y="횟수",
            text="횟수",
            title=f"{exp_type} 시뮬레이션 결과 분포 (시행 {n_trials}회)",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(yaxis_title="횟수")

        st.plotly_chart(fig, use_container_width=True)

        # 상대도수 그래프도 보고 싶을 수 있으니 옵션 제공
        with st.expander("상대도수(확률) 그래프 보기"):
            fig_rel = px.bar(
                df,
                x="결과",
                y="상대도수",
                text="상대도수",
                title=f"{exp_type} 상대도수 분포 (시행 {n_trials}회)",
            )
            fig_rel.update_traces(texttemplate="%{text:.3f}", textposition="outside")
            fig_rel.update_layout(yaxis_title="상대도수")
            st.plotly_chart(fig_rel, use_container_width=True)


# -----------------------------
# 3. 메인 함수: 사이드바에서 앱 선택
# -----------------------------
def main():
    st.sidebar.title("🔧 앱 선택")
    app_choice = st.sidebar.radio(
        "사용할 기능을 선택하세요",
        ("계산기", "확률 시뮬레이터"),
    )

    if app_choice == "계산기":
        calculator_app()
    else:
        probability_simulator_app()

    st.sidebar.markdown("---")
    st.sidebar.caption("Powered by Streamlit · main.py로 실행")


if __name__ == "__main__":
    main()
