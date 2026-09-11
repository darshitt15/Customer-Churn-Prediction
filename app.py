import streamlit as st
import joblib
import pandas as pd
import numpy as np

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>

.main-title {
    font-size: 40px;
    font-weight: 700;
    text-align: center;
}

.subtitle {
    text-align: center;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD MODEL (cached + error-safe)
# -------------------------------
@st.cache_resource
def load_artifacts():
    try:
        model = joblib.load("models/customer_churn_model.pkl")
        columns = joblib.load("models/model_columns.pkl")
        return model, columns
    except FileNotFoundError as e:
        st.error(
            "❌ Model files not found. Make sure "
            "`models/customer_churn_model.pkl` and "
            "`models/model_columns.pkl` exist."
        )
        st.stop()

model, columns = load_artifacts()

# -------------------------
# SIDEBAR NAVIGATION
# -------------------------
st.sidebar.title("📊 Churn Predictor")

st.sidebar.write(
    "Machine Learning powered customer churn analysis."
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📊 Customer Details", "ℹ️ About Project"]
)

st.sidebar.divider()

st.sidebar.caption("Built with Python & Streamlit")
st.sidebar.caption("Random Forest ML Model")

# ===============================
# HOME PAGE
# ===============================
if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">📊 Customer Churn Prediction System</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Machine Learning powered customer retention analysis</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
Welcome to the **Customer Churn Prediction Dashboard**.
This application predicts whether a telecom customer is likely to leave the company using Machine Learning.

### Features
- Customer Details Form
- Machine Learning Prediction
- Prediction Probability
- Business Insights
- Interactive Dashboard
""")

    st.subheader("🎯 What This App Does")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔮 Predict")
        st.write(
            "Estimate whether a customer is likely to stay or churn."
        )

    with col2:
        st.markdown("### 📊 Analyze")
        st.write(
            "View churn probability, risk level and important risk factors."
        )

    with col3:
        st.markdown("### 💡 Act")
        st.write(
            "Get recommended retention actions for at-risk customers."
        )

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Customers", "7043")
    with col2:
        st.metric("Churn Rate", "26.5%")
    with col3:
        st.metric("Best Model", "Random Forest")

    st.divider()

    st.subheader("Project Workflow")
    st.write("""
1. Data Cleaning
2. Exploratory Data Analysis
3. Feature Engineering
4. Machine Learning
5. Model Evaluation
6. Deployment using Streamlit
""")

# ===============================
# CUSTOMER DETAILS PAGE
# ===============================
elif page == "📊 Customer Details":

    st.markdown(
        '<div class="main-title">🎯 Customer Churn Prediction</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Analyze customer behavior and estimate churn risk</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # -------------------------
    # FORM
    # -------------------------
    st.markdown("## 👤 Personal Information")

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
    with col2:
        senior = st.selectbox("Senior Citizen", [0, 1])

    col1, col2 = st.columns(2)
    with col1:
        partner = st.selectbox("Partner", ["Yes", "No"])
    with col2:
        dependents = st.selectbox("Dependents", ["Yes", "No"])

    tenure = st.slider("Tenure (Months)", min_value=0, max_value=72, value=12)

    st.divider()
    st.markdown("## 📡 Services")

    col1, col2 = st.columns(2)
    with col1:
        phone = st.selectbox("Phone Service", ["Yes", "No"])
    with col2:
        internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    col1, col2 = st.columns(2)
    with col1:
        security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    with col2:
        backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])

    col1, col2 = st.columns(2)
    with col1:
        protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    with col2:
        support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])

    tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    st.divider()
    st.markdown("## 💳 Contract & Billing")

    col1, col2 = st.columns(2)
    with col1:
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    with col2:
        payment = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
        )

    col1, col2 = st.columns(2)
    with col1:
        monthly = st.number_input("Monthly Charges", min_value=0.0, value=50.0)
    with col2:
        total = st.number_input("Total Charges", min_value=0.0, value=1000.0)

    paperless = st.selectbox("Paperless Billing", ["Yes", "No"])

    # -------------------------
    # PREDICT BUTTON -> store everything in session_state
    # -------------------------
    if st.button("Save Customer Details"):

        customer = {
            "gender": gender,
            "SeniorCitizen": senior,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone,
            "InternetService": internet,
            "OnlineSecurity": security,
            "OnlineBackup": backup,
            "DeviceProtection": protection,
            "TechSupport": support,
            "StreamingTV": tv,
            "StreamingMovies": movies,
            "Contract": contract,
            "PaperlessBilling": paperless,
            "PaymentMethod": payment,
            "MonthlyCharges": monthly,
            "TotalCharges": total,
        }

        input_df = pd.DataFrame([customer])
        input_df = pd.get_dummies(input_df, drop_first=False)
        input_df = input_df.reindex(columns=columns, fill_value=0)

        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)

        stay_probability = probability[0][0] * 100
        churn_probability = probability[0][1] * 100

        # Everything downstream reads from here, so it survives reruns
        # (e.g. switching sidebar pages and coming back).
        st.session_state["churn_result"] = {
            "customer": customer,
            "prediction": int(prediction[0]),
            "stay_probability": stay_probability,
            "churn_probability": churn_probability,
        }

    # -------------------------
    # SHOW RESULTS (only if a prediction has been made)
    # -------------------------
    if "churn_result" in st.session_state:

        result = st.session_state["churn_result"]
        customer = result["customer"]
        churn_probability = result["churn_probability"]
        stay_probability = result["stay_probability"]

        if result["prediction"] == 1:
            st.error("🔴 CUSTOMER IS LIKELY TO CHURN")
        else:
            st.success("🟢 CUSTOMER IS LIKELY TO STAY")

        # ---- Prediction Result ----
        st.divider()
        st.markdown("## 📊 Prediction Result")

        if churn_probability < 20:
            risk_level = "🟢 LOW RISK"
            risk_message = "The customer has a very low probability of churning."
        elif churn_probability < 35:
            risk_level = "🟡 MODERATE RISK"
            risk_message = "The customer should be monitored for potential churn."
        elif churn_probability < 50:
            risk_level = "🟠 HIGH RISK"
            risk_message = "The customer has a significantly higher risk of churning."
        else:
            risk_level = "🔴 CRITICAL RISK"
            risk_message = "The customer is highly likely to churn."

        st.markdown("### ⚠️ Churn Risk Assessment")
        st.info(risk_level)
        st.write(risk_message)

        st.markdown("### 📈 Prediction Probability")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="🟢 Stay Probability", value=f"{stay_probability:.1f}%")
        with col2:
            st.metric(label="🔴 Churn Probability", value=f"{churn_probability:.1f}%")

        st.markdown("### 📊 Churn Risk Score")
        st.progress(int(churn_probability))
        st.caption(f"Overall Churn Risk: {churn_probability:.1f}%")

        # ---- Customer Summary ----
        st.divider()
        st.markdown("## 👤 Customer Summary")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### Personal Details")
            st.write(f"**Gender:** {customer['gender']}")
            st.write(f"**Senior Citizen:** {customer['SeniorCitizen']}")
            st.write(f"**Partner:** {customer['Partner']}")
            st.write(f"**Dependents:** {customer['Dependents']}")
        with col2:
            st.markdown("### Service Details")
            st.write(f"**Tenure:** {customer['tenure']} months")
            st.write(f"**Internet Service:** {customer['InternetService']}")
            st.write(f"**Contract:** {customer['Contract']}")
            st.write(f"**Tech Support:** {customer['TechSupport']}")
        with col3:
            st.markdown("### Billing Details")
            st.write(f"**Monthly Charges:** ₹{customer['MonthlyCharges']}")
            st.write(f"**Total Charges:** ₹{customer['TotalCharges']}")
            st.write(f"**Paperless Billing:** {customer['PaperlessBilling']}")
            st.write(f"**Payment Method:** {customer['PaymentMethod']}")

        # ---- Risk Factors ----
        st.divider()
        st.markdown("## ⚠️ Risk Factors")

        risk_factors = []

        if customer["tenure"] < 12:
            risk_factors.append("🕒 Short customer tenure - newer customers may have a higher churn risk.")
        if customer["Contract"] == "Month-to-month":
            risk_factors.append("📄 Month-to-month contract - less customer commitment.")
        if customer["InternetService"] == "Fiber optic":
            risk_factors.append("🌐 Fiber optic service - associated with higher churn in this dataset.")
        if customer["TechSupport"] == "No":
            risk_factors.append("🛠️ No tech support - customer may be more likely to leave.")
        if customer["MonthlyCharges"] > 80:
            risk_factors.append("💰 High monthly charges - higher cost may increase churn risk.")
        if customer["PaymentMethod"] == "Electronic check":
            risk_factors.append("💳 Electronic check payment - associated with higher churn risk.")
        if customer["Partner"] == "No":
            risk_factors.append("👤 No partner - may indicate lower household retention.")

        # NOTE: original code used `for ... else:` here, which is a Python
        # for/else (the else always runs unless a `break` happens), so both
        # the warning list AND the "no risk factors" message showed at once.
        # This is a plain if/else instead.
        if risk_factors:
            st.warning("### Factors that may increase churn risk")
            for factor in risk_factors:
                st.write(factor)
        else:
            st.success("### No major churn risk factors detected")
            st.write("This customer profile does not contain any of the selected major churn indicators.")

        # ---- Model Insights ----
        st.divider()
        st.markdown("## 📊 Model Insights")
        st.write("These are the features that had the greatest influence on the model's predictions.")

        if hasattr(model, "feature_importances_"):
            feature_importance = pd.DataFrame({
                "Feature": columns,
                "Importance": model.feature_importances_
            })
            feature_importance = feature_importance.sort_values(by="Importance", ascending=False).head(10)
            st.bar_chart(feature_importance.set_index("Feature"))
        else:
            st.info("Feature importance is not available for this model type.")

        # ---- Retention Recommendation ----
        st.divider()
        st.markdown("## 💡 Recommended Action")

        if churn_probability >= 50:
            st.error("🔴 Immediate retention action recommended.")
            st.write("Consider contacting the customer with a personalized retention offer, "
                     "loyalty benefit, discount, or service improvement.")
        elif churn_probability >= 35:
            st.warning("🟠 Proactive retention recommended.")
            st.write("Monitor this customer closely and consider offering additional support, "
                     "loyalty benefits, or a personalized service offer.")
        elif churn_probability >= 20:
            st.info("🟡 Customer should be monitored.")
            st.write("The customer is not currently at critical risk, but periodic engagement "
                     "and satisfaction checks are recommended.")
        else:
            st.success("🟢 No immediate retention action required.")
            st.write("The customer has a low predicted churn probability. Continue normal "
                     "customer engagement and service.")

    else:
        st.info("👆 Fill in the customer details above and click **Save Customer Details** to see a prediction.")

# ===============================
# ABOUT PAGE
# ===============================
elif page == "ℹ️ About Project":

    st.title("ℹ️ About Project")

    st.write(
        """
        This project uses Machine Learning to predict customer churn.
        The model analyzes customer demographic, service, contract and
        billing information to estimate the probability that a customer
        may leave the company.
        """
    )

    st.divider()

    st.subheader("🛠️ Technologies Used")

    st.write("""
- Python
- Pandas
- NumPy
- Scikit-learn
- Random Forest Classifier
- Streamlit
- Joblib
""")

    st.divider()

    st.subheader("🤖 Model Performance")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Accuracy", "76%")

    with col2:
        st.metric("Churn Recall", "63%")

    with col3:
        st.metric("ROC-AUC", "0.82")

    st.sidebar.divider()
    st.sidebar.markdown("**Developed by Darshit Bangera**")
