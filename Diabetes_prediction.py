import numpy as np
import pickle
import streamlit as st
from PIL import Image
import base64
import pandas as pd
import altair as alt

# Load the saved model
loaded_model = pickle.load(open(r'C:/Users/HP/Desktop/Deployment/trained_model.sav', 'rb'))

# Function for prediction
def diabetes_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    return prediction[0]

# Function to display GIFs
def display_gif(gif_path):
    with open(gif_path, "rb") as file:
        contents = file.read()
        data_url = f"data:image/gif;base64,{base64.b64encode(contents).decode('utf-8')}"
        st.markdown(
            f'<img src="{data_url}" alt="gif" width="700">', 
            unsafe_allow_html=True
        )

# Function to check if inputs meet minimum healthy thresholds
def inputs_valid():
    return (
        Pregnancies >= 1 and
        Glucose >= 70 and
        BloodPressure >= 50 and
        SkinThickness >= 10 and
        Insulin >= 15 and
        BMI >= 18.5 and
        Age >= 30
    )

# Streamlit app main function
def main():
    st.set_page_config(page_title="Diabetes Prediction App", page_icon="🩺", layout="wide")

    # Banner image
    banner = Image.open(r'C:/Users/HP/Desktop/Deployment/banner.jpg')
    st.image(banner, use_column_width=True)

    # Custom CSS styling
    st.markdown("""
        <style>
        .main {
            background-color: #f0f8ff;
        }
        .stButton>button {
            background-color: #ff6f61;
            color: white;
            border-radius: 10px;
            height: 50px;
            font-size: 20px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stButton>button:hover {
            background-color: #ff4b38;
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
        }
        .stTextInput input {
            border-radius: 8px;
            padding: 10px;
            font-size: 18px;
            background-color: #fff4e6;
        }
        .stTextInput input:focus {
            border-color: #ff6f61;
            box-shadow: 0 0 5px rgba(255, 111, 97, 0.5);
        }
        .result-success {
            background-color: #d4edda;
            padding: 20px;
            border-radius: 12px;
            color: #155724;
            font-weight: bold;
            font-size: 20px;
            box-shadow: 0 0 10px rgba(0, 255, 0, 0.2);
        }
        .result-error {
            background-color: #f8d7da;
            padding: 20px;
            border-radius: 12px;
            color: #721c24;
            font-weight: bold;
            font-size: 20px;
            box-shadow: 0 0 10px rgba(255, 0, 0, 0.2);
        }
        h1 {
            font-family: 'Arial', sans-serif;
            font-size: 32px;
            color: #ff6f61;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
        h2 {
            font-family: 'Arial', sans-serif;
            font-size: 28px;
            color: #ff6f61;
        }
        .stInput label {
            font-size: 18px;
            color: #333;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    # Sidebar with logo and info
    with st.sidebar:
        logo = Image.open(r'C:/Users/HP/Desktop/Deployment/logo.png')
        st.image(logo, width=180)
        st.title("📊 Project Info")
        st.write("""
            **Major Project**
            - Diabetes Prediction System  
            - Built with Python, Streamlit & ML  
            - Uses SVM Classifier  
        """)
        st.markdown("---")
        st.write("👨‍💻 Developed by **Anuj Gusain**")

    # Title
    st.title("💉 Diabetes Prediction Web App")

    st.markdown("## 📋 Enter Patient Details")

    global Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, Age
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.number_input('👶 Number of Pregnancies (min 1)', min_value=0, step=1, value=1)
        BloodPressure = st.number_input('🩸 Blood Pressure (mm Hg, min 50)', min_value=0, value=50)

    with col2:
        Glucose = st.number_input('🍬 Glucose Level (mg/dL, min 70)', min_value=0, value=70)
        SkinThickness = st.number_input('📏 Skin Thickness (mm, min 10)', min_value=0, value=10)
        Age = st.number_input('🎂 Age (years, min 30)', min_value=1, max_value=120, step=1, value=30)

    with col3:
        Insulin = st.number_input('💉 Insulin Level (mu U/ml, min 15)', min_value=0, value=15)
        BMI = st.number_input('⚖️ BMI (min 18.5)', min_value=0.0, format="%.2f", value=18.5)

    st.markdown("---")

    # Predict button
    if st.button('🔍 Get Diabetes Test Result'):
        if not inputs_valid():
            st.warning("⚠️ Please enter all values greater than or equal to the minimum healthy thresholds. Refer to the chart below.")
        else:
            input_data = [
                float(Pregnancies), float(Glucose), float(BloodPressure),
                float(SkinThickness), float(Insulin), float(BMI),
                float(Age)
            ]
            result = diabetes_prediction(input_data)

            if result == 0:
                st.markdown('<div class="result-success">✅ The person is <strong>Not Diabetic</strong>.</div>', unsafe_allow_html=True)
                gif_path = r'C:/Users/HP/Desktop/Deployment/nondiabetic.gif'
                display_gif(gif_path)
            else:
                st.markdown('<div class="result-error">⚠️ The person is <strong>Diabetic</strong>.</div>', unsafe_allow_html=True)
                gif_path = r'C:/Users/HP/Desktop/Deployment/diabetic.gif'
                display_gif(gif_path)

            # Diabetes Risk Meter
            glucose_score = min(max((Glucose - 70) / (200 - 70), 0), 1)
            bmi_score = min(max((BMI - 15) / (40 - 15), 0), 1)
            risk_score = (0.6 * glucose_score + 0.4 * bmi_score) * 100
            risk_score = round(risk_score, 1)

            st.markdown("### 📊 Diabetes Risk Meter")
            st.metric(label="Estimated Risk Percentage", value=f"{risk_score} %")

            bar_color = "#ff4b38" if risk_score > 50 else "#28a745"
            st.markdown(f"""
                <div style="background-color:#eee; border-radius:10px; padding:5px; margin-bottom: 30px;">
                    <div style="width:{risk_score}%; background-color:{bar_color}; height:20px; border-radius:10px;"></div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Normal ranges chart
    st.markdown("### 📈 Normal Ranges for Key Features")
    data = {
        'Feature': ['Pregnancies', 'Glucose', 'Blood Pressure', 'Skin Thickness', 'Insulin', 'BMI', 'Age'],
        'Min Normal': [1, 70, 50, 10, 15, 18.5, 30],
        'Max Normal': [10, 140, 90, 40, 200, 35, 80]
    }
    df = pd.DataFrame(data)

    chart = alt.Chart(df).mark_bar(size=12).encode(
        y=alt.Y('Feature', sort='-x'),
        x='Max Normal',
        x2='Min Normal',
        color=alt.condition(
            alt.datum['Max Normal'] > 0,
            alt.value('#ff6f61'),
            alt.value('lightgray')
        )
    ).properties(height=300)

    st.altair_chart(chart, use_container_width=True)

    st.caption("✨ Powered by Anuj Gusain | Major Project 2025")


if __name__ == '__main__':
    main()
