# DispatchBrain ETA Predictor 🚚🧠

An interactive machine learning dashboard that predicts estimated delivery arrival time (ETA) based on real-world logistics inputs. Built with **Streamlit**, powered by a **FastAPI backend**, and deployed via **Docker** on Hugging Face Spaces.

---

## 🔗 Live Demo

- 🌐 **Frontend (Streamlit Dashboard):**  
  [DispatchBrain-Fronted on Hugging Face](https://huggingface.co/spaces/salmaml56/DispatchBrain-Fronted)

- ⚙️ **Backend (FastAPI API):**  
  [DispatchBrainETA API Space](https://huggingface.co/spaces/salmaml56/DispacthBrainETA)

---

## 🧠 What It Does

This app predicts the delivery ETA based on:

- Hour of the day  
- Day of the week  
- Weekend indicator  
- Distance and log-distance  
- Weather severity  
- Expected delivery duration

The model is trained on real logistics data and exposed via a FastAPI endpoint. The Streamlit frontend collects user inputs, sends them to the backend, and displays the predicted ETA in minutes.

---

## 🛠 Tech Stack

| Layer       | Tools Used                     |
|-------------|--------------------------------|
| Frontend    | Streamlit                      |
| Backend     | FastAPI                        |
| Deployment  | Docker + Hugging Face Spaces   |
| ML Model    | Scikit-learn / XGBoost (custom)|
| API Comm    | `requests` library             |

---

## 📋 How to Use

1. Open the [Live Demo](https://huggingface.co/spaces/salmaml56/DispatchBrain-Fronted)
2. Fill in delivery details:
   - Hour, Day, Weekend status  
   - Distance, Duration, Weather severity
3. Click **Predict ETA**
4. View the estimated arrival time in minutes

---

## 📂 Project Structure
