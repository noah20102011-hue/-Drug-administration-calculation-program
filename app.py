
import streamlit as st
import pandas as pd

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
    "환자 정보와 약물 정보를 입력하여 "
    "처방된 투여주기까지 남은 시간을 계산합니다."
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
# 2. 환자 정보 및 약물 정보 입력
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
        "투여할 약물을 선택하세요.",
        drug_list
    )

    if selected_drug == "기타 약물":
        other_drug = st.text_input("약물 이름 직접 입력")
    else:
        other_drug = ""

    # 처방된 투여주기 입력
    prescribed_interval = st.number_input(
        "처방된 투여주기 (시간)",
        min_value=0.1,
        value=12.0,
        help="의료진이 확인한 처방상 투여주기를 입력하세요."
    )

    # 투약 후 경과시간
    elapsed_time = st.number_input(
        "마지막 투약 후 흐른 시간 (시간)",
        min_value=0.0,
        value=0.0
    )

    submitted = st.form_submit_button("계산하기")


# ==========================================
# 3. 계산 함수
# ==========================================

def calculate_interval(
    weight,
    height,
    age,
    prescribed_interval
):

    # BMI 계산
    bmi = weight / ((height / 100) ** 2)

    # 투여주기는 처방된 값을 사용
    # 체중과 키로 임의 변경하지 않음
    result = [
        round(bmi, 2),
        prescribed_interval
    ]

    return result


# ==========================================
# 4. 남은 시간 계산 함수
# ==========================================

def calculate_remaining_time(
    prescribed_interval,
    elapsed_time
):

    remaining_time = (
        prescribed_interval - elapsed_time
    )

    return max(remaining_time, 0)


# ==========================================
# 5. 계산하기 버튼 실행
# ==========================================

if submitted:

    if not patient_name.strip():
        st.error("환자 이름을 입력해주세요.")

    elif selected_drug == "기타 약물" and not other_drug.strip():
        st.error("약물 이름을 입력해주세요.")

    elif elapsed_time >= prescribed_interval:
        st.error(
            "입력한 경과시간이 처방된 투여주기 이상입니다. "
            "다음 투약 시점은 의료진 또는 처방을 확인하세요."
        )

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
            prescribed_interval,
            elapsed_time
        ]

        # ==================================
        # 7. 투여주기 계산 함수 실행
        # ==================================

        calculation_result = calculate_interval(
            weight,
            height,
            age,
            prescribed_interval
        )

        bmi = calculation_result[0]
        interval = calculation_result[1]

        # ==================================
        # 8. 남은 시간 계산
        # ==================================

        remaining_time = calculate_remaining_time(
            interval,
            elapsed_time
        )

        # ==================================
        # 9. 결과 출력
        # ==================================

        st.divider()

        st.subheader("③ 계산 결과")

        st.success(
            f"약물을 {remaining_time}시간 후 재투여 예정입니다."
            f" (약물주기: {interval}시간)"
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
        # 11. 환자 차트 리스트 정의
        # ==================================

        st.subheader("④ 환자 차트")

        chart_titles = [
            "환자 이름",
            "나이",
            "몸무게",
            "키",
            "선택 약물",
            "처방된 투여주기",
            "투약 후 경과시간",
            "남은 시간",
            "BMI"
        ]

        chart_values = [
            patient_name,
            f"{age}세",
            f"{weight}kg",
            f"{height}cm",
            drug_name,
            f"{interval}시간",
            f"{elapsed_time}시간",
            f"{remaining_time}시간",
            bmi
        ]

        # ==================================
        # 12. for문을 이용한 환자 차트 출력
        # ==================================

        chart_data = []

        for i in range(len(chart_titles)):

            chart_data.append({
                "항목": chart_titles[i],
                "입력 정보": chart_values[i]
            })

        df = pd.DataFrame(chart_data)

        st.table(df)

        st.divider()

        st.caption(
            "본 프로그램은 처방된 투여주기를 기준으로 "
            "시간을 계산하는 학습용 프로그램입니다. "
            "실제 투약 시점은 의료진의 처방을 따르세요."
        )
