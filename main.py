import streamlit as st
import math

# 페이지 기본 설정
st.set_page_config(page_title="다기능 계산기", page_icon="🧮")

def main():
    st.title("🧮 다기능 계산기")
    st.write("사칙연산, 모듈러, 지수, 로그 연산을 지원하는 간단 웹 계산기입니다.")

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

    # 하단 안내
    st.markdown("---")
    st.caption("Powered by Streamlit & Python · 깃허브에 이 파일을 그대로 업로드하면 됩니다.")


if __name__ == "__main__":
    main()
