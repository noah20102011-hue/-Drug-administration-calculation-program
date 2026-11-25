
import streamlit as st
import pandas as pd

# 프로그램 제목
st.title("약물 투여시 투여주기 계산 프로그램")
st.subheader("환자 정보 및 약물 관련 정보 입력")

# 1. 환자 정보 입력
with st.form("patient_form"):

    st.write("### 환자 기본 정보")

    patient_name = st.text_input("환자 이름")
    age = st.number_input("나이", min_value=0, max_value=120, value=30)
    weight = st.number_input("몸무게(kg)", min_value=1.0, value=60.0)
    height = st.number_input("키(cm)", min_value=1.0, value=170.0)

    st.write("### 약물 정보")

    drug_name = st.text_input("약물 이름")
    half_life = st.number_input(
        "가상 약물 반감기(시간)",
        min_value=0.1,
        value=6.0
    )

    reference_interval = st.number_input(
        "학습용 기준 투여주기(시간)",
        min_value=0.1,
        value=12.0
    )

    elapsed_time = st.number_input(
        "마지막 투약 후 흐른 시간(시간)",
        min_value=0.0,
        value=4.0
    )

    submitted = st.form_submit_button("계산하기")


# 2. 계산 함수
def calculate_interval(weight, height, age, half_life,
                       reference_interval):

    bmi = weight / ((height / 100) ** 2)

    # 학습용 기준값 사용
    interval = reference_interval

    result = [round(bmi, 2), interval]

    return result


# 3. 남은 시간 계산 함수
def calculate_remaining_time(interval, elapsed_time):

    remaining = max(interval - elapsed_time, 0)

    return remaining


# 4. 계산 버튼 실행
if submitted:

    if not patient_name.strip() or not drug_name.strip():
        st.error("환자 이름과 약물 이름을 입력해주세요.")

    elif height <= 0 or weight <= 0:
        st.error("키와 몸무게를 확인해주세요.")

    else:

        # 환자 정보를 리스트로 정의
        patient_info = [
            patient_name,
            age,
            weight,
            height,
            drug_name,
            half_life,
            reference_interval
        ]

        # 계산 함수 실행
        calculation_result = calculate_interval(
            weight,
            height,
            age,
            half_life,
            reference_interval
        )

        bmi = calculation_result[0]
        interval = calculation_result[1]

        # 남은 시간 계산
        remaining_time = calculate_remaining_time(
            interval,
            elapsed_time
        )

        # 5. 결과 메시지 출력
        st.divider()
        st.subheader("계산 결과")

        st.success(
            f"학습용 기준 투여주기는 {interval}시간입니다."
        )

        st.info(
            f"기준 주기까지 남은 시간은 {remaining_time}시간입니다."
        )

        # 6. 65세 이상 조건 판단
        if age >= 65:
            st.warning(
                "나이가 65세 이상임으로 약물투여에 주의가 필요합니다."
            )

        # 7. 환자 차트 구성
        st.subheader("환자 차트")

        chart_titles = [
            "환자 이름",
            "나이",
            "몸무게",
            "키",
            "약물 이름",
            "약물 반감기",
            "기준 투여주기",
            "투약 후 경과시간",
            "BMI"
        ]

        chart_values = [
            patient_name,
            f"{age}세",
            f"{weight}kg",
            f"{height}cm",
            drug_name,
            f"{half_life}시간",
            f"{reference_interval}시간",
            f"{elapsed_time}시간",
            bmi
        ]

        # 리스트를 활용한 반복 출력
        chart_data = []

        for i in range(len(chart_titles)):
            chart_data.append({
                "항목": chart_titles[i],
                "입력 정보": chart_values[i]
            })

        # 표 형태로 화면 출력
        df = pd.DataFrame(chart_data)

        st.table(df)

        st.caption(
            "본 프로그램은 약동학 학습용 가상 계산 프로그램입니다. "
            "실제 약물의 투여주기나 투약 시점을 결정하는 데 사용할 수 없습니다."
        )
