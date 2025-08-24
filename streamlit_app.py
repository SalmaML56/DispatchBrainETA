# --------------------------------------------------
# API Call and Prediction Display
# --------------------------------------------------
API_URL = "https://salmaml56-dispacthbraineta.hf.space/predict_eta"

if st.button("Predict ETA"):
    try:
        # Send POST request to FastAPI backend
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        # Display prediction result
        st.success(f"Estimated Arrival Time: {result['predicted_eta']} minutes")

    except requests.exceptions.RequestException as req_err:
        st.error("Prediction failed due to a connection issue.")
        st.code(str(req_err), language="text")

    except Exception as e:
        st.error("An unexpected error occurred during prediction.")
        st.code(str(e), language="text")
