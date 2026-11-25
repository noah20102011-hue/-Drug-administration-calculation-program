
import streamlit as st
import pandas as pd
import math

# ==========================================
# 약물 투여시 투여주기 계산 프로그램
# ==========================================

st.set_page_config(
    page_title="약물 투여시 투여주기 계산 프로그램",
    page_icon="💊",
    layout="centered"
)

st.title("💊 약물 투여시 투여주기 계산 프로그램")

st.write(
    "환자 정보와 약물의 약동학적 특성을 입력하여 "
    "이론적인 혈중농도 감소 시간을 계산합니다."
)

# ==========================================
# 1. 약물 리스트 정의
# ==========================================

drug_list = [
    "아세트아미노펜 (Acetaminophen)",
    "이부프로펜 (Ibuprofen)",
    "아목시실린 (Amoxicillin)",
    "세티리진 (Cetirizine)",
    "로라타딘 (Loratadine)",
    "메트포르민 (Metformin)",
    "오메프라졸 (Omeprazole)",
    "기타 약물"
]

# ==========================================
# 2. 환자 및 약물 정보 입력
# ==========================================

st.subheader("① 환자 정보 입력")

with st.form("drug_form"):

    patient_name = st.text_input("환자 이름")

    age = st.number_input(
        "나이",
        min_value=0,
        max_value=120,
        value=30
    )

    weight = st.number_input(
        "몸무게 (kg)",
        min_value=1.0,
        value=60.0
    )

    height = st.number_input(
        "키 (cm)",
        min_value=1.0,
        value=170.0
    )

    st.divider()

    # 약물 선택
    st.subheader("② 약물 선택")

    selected_drug = st.selectbox(
        "투여 약물을 선택하세요.",
        drug_list
    )

    if selected_drug == "기타 약물":
        other_drug = st.text_input("약물 이름 입력")
    else:
        other_drug = ""

    # 약물 반감기 입력
    half_life = st.number_input(
        "약물 반감기 (시간)",
        min_value=0.01,
        value=6.0,
        help="검증된 약동학 자료에서 확인한 반감기를 입력하세요."
    )

    # 초기농도와 하한농도의 비율
    concentration_ratio = st.number_input(
        "초기농도 / 비교 하한농도 비율",
        min_value=1.01,
        value=2.0,
        help="교육용 모델에서 사용할 농도 비율입니다."
    )

    # 마지막 투약 후 경과시간
    elapsed_time = st.number_input(
        "마지막 투약 후 흐른 시간 (시간)",
        min_value=0.0,
        value=0.0
    )

    submitted = st.form_submit_button("계산하기")


# ==========================================
# 3. 약동학 계산 함수
# ==========================================

def calculate_interval(
    weight,
    height,
    age,
    half_life,
    concentration_ratio
):

    # BMI 계산
    bmi = weight / ((height / 100) ** 2)

    # 약물 제거속도상수 계산
    k = 0.693 / half_life

    # 농도 감소에 필요한 이론적 시간
    interval = math.log(concentration_ratio) / k

    # 계산 결과 리스트 반환
    result = [
        round(bmi, 2),
        round(k, 4),
        round(interval, 2)
    ]

    return result


# ==========================================
# 4. 남은 시간 계산 함수
# ==========================================

def calculate_remaining_time(interval, elapsed_time):

    remaining_time = interval - elapsed_time

    return max(remaining_time, 0)


# ==========================================
# 5. 계산하기 버튼 실행
# ==========================================

if submitted:

    if not patient_name.strip():

        st.error("환자 이름을 입력해주세요.")

    elif selected_drug == "기타 약물" and not other_drug.strip():

        st.error("약물 이름을 입력해주세요.")

    else:

        # 약물 이름 결정
        if selected_drug == "기타 약물":
            drug_name = other_drug
        else:
            drug_name = selected_drug

        # ==================================
        # 6. 환자 정보 리스트 정의
        # ==================================

        patient_info = [
            patient_name,
            age,
            weight,
            height,
            drug_name,
            half_life,
            concentration_ratio,
            elapsed_time
        ]

        # ==================================
        # 7. 약동학 계산 함수 실행
        # ==================================

        calculation_result = calculate_interval(
            weight,
            height,
            age,
            half_life,
            concentration_ratio
        )

        bmi = calculation_result[0]
        k = calculation_result[1]
        interval = calculation_result[2]

        # ==================================
        # 8. 남은 시간 계산
        # ==================================

        remaining_time = calculate_remaining_time(
            interval,
            elapsed_time
        )

        # ==================================
        # 9. 계산 결과 출력
        # ==================================

        st.divider()

        st.subheader("③ 약동학 계산 결과")

        st.metric(
            "약물 제거속도상수",
            f"{k} /시간"
        )

        st.metric(
            "이론적 농도 감소 시간",
            f"{interval}시간"
        )

        st.metric(
            "모델 기준 시간까지 남은 시간",
            f"{remaining_time}시간"
        )

        st.success(
            f"이론적 농도 감소 시간: {interval}시간"
        )

        st.info(
            f"투약 후 경과시간을 반영한 계산상 남은 시간: "
            f"{remaining_time}시간"
        )

        # ==================================
        # 10. 65세 이상 조건 판단
        # ==================================

        if age >= 65:

            st.warning(
                "나이가 65세 이상임으로 "
                "약물투여에 주의가 필요합니다."
            )

        # ==================================
        # 11. 환자 차트 구성
        # ==================================

        st.subheader("④ 환자 차트")

        chart_titles = [
            "환자 이름",
            "나이",
            "몸무게",
            "키",
            "선택 약물",
            "약물 반감기",
            "초기농도/하한농도 비율",
            "제거속도상수",
            "이론적 농도 감소 시간",
            "투약 후 경과시간",
            "계산상 남은 시간",
            "BMI"
        ]

        chart_values = [
            patient_name,
            f"{age}세",
            f"{weight}kg",
            f"{height}cm",
            drug_name,
            f"{half_life}시간",
            concentration_ratio,
            f"{k} /시간",
            f"{interval}시간",
            f"{elapsed_time}시간",
            f"{remaining_time}시간",
            bmi
        ]

        # ==================================
        # 12. for문으로 환자 차트 출력
        # ==================================

        chart_data = []

        for i in range(len(chart_titles)):

            chart_data.append({
                "항목": chart_titles[i],
                "입력 및 계산 정보": chart_values[i]
            })

        df = pd.DataFrame(chart_data)

        st.table(df)

        # ==================================
        # 13. 계산식 출력
        # ==================================

        st.subheader("⑤ 적용된 계산식")

        st.latex(r"k = \frac{0.693}{t_{1/2}}")

        st.latex(
            r"\tau = \frac{\ln(C_0/C_{\min})}{k}"
        )

        st.write(f"제거속도상수 k = {k}")

        st.write(f"계산된 이론적 시간 = {interval}시간")

        # ==================================
        # 14. 안내사항
        # ==================================

        st.divider()

        st.caption(
            "본 프로그램은 1차 제거 약동학을 가정한 "
            "교육용 수학 모델입니다. "
            "계산된 시간은 실제 투여주기 또는 재투여 시점이 아닙니다. "
            "실제 약물 투여는 의료진의 처방과 약물별 "
            "공식 약동학 자료를 따라야 합니다."
        )
