import streamlit as st
import joblib
import numpy as np
import pandas as pd

st.set_page_config(page_title="App Rating Predictor", layout="centered")

st.markdown("""
    <style>
        .main {
            background-color: #f9f9f9;
        }
        h1 {
            color: #333333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            font-size: 16px;
            padding: 10px 24px;
        }
        .css-1aumxhk {
            background-color: #ffffff;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📱 Google Play App Rating Predictor")
st.markdown("Use this tool to estimate the expected rating of your Android app based on key information.")
st.markdown("---")

model = joblib.load("rating_model.pkl")

all_categories = ['ART', 'AUTOMOTIVE', 'BUSINESS', 'COMMUNICATION', 'EDUCATION',
                  'ENTERTAINMENT', 'HEALTH', 'LIFESTYLE', 'SHOPPING',
                  'TRAVEL', 'SYSTEM']

all_genres = ['Adventure', 'Arcade', 'Art & Design', 'Auto & Vehicles', 'Beauty', 'Board', 'Books & Reference', 'Business', 'Card', 'Casino', 'Casual', 'Comics', 'Communication', 'Dating', 'Education', 'Educational', 'Entertainment', 'Events', 'Finance', 'Food & Drink', 'Health & Fitness', 'House & Home', 'Libraries & Demo', 'Lifestyle', 'Navigation', 'Medical', 'Music', 'Music & Audio', 'News & Magazines', 'Parenting', 'Personalization', 'Photography', 'Productivity', 'Puzzle', 'Racing', 'Role Playing', 'Shopping', 'Simulation', 'Social', 'Sports', 'Strategy', 'Tools', 'Travel & Local', 'Trivia', 'Video Players & Editors', 'Weather', 'Word']

all_content_ratings = ['Everyone', 'Everyone 10+', 'Mature 17+', 'Teen', 'Unrated']

st.subheader("🔧 App Details")

col1, col2 = st.columns(2)
with col1:
    reviews = st.number_input("Number of Reviews", min_value=0)
    price = st.number_input("Price (USD)", min_value=0.0)
    app_type = st.selectbox("Type", ['Free', 'Paid'])
with col2:
    size = st.number_input("App Size (MB)", min_value=0.0)
    installs = st.number_input("Number of Installs", min_value=0)
    content_rating = st.selectbox("Content Rating", all_content_ratings)

genre = st.selectbox("App Genre", all_genres)
category = st.selectbox("App Category", all_categories)
category_encoded = [1 if category == cat else 0 for cat in all_categories]
genre_encoded = [1 if genre == g else 0 for g in all_genres]
content_rating_encoded = [1 if content_rating == cr else 0 for cr in all_content_ratings]
type_encoded = [1] if app_type == 'Paid' else [0]


input_data = np.array([[reviews, price, size, installs] + category_encoded + genre_encoded + content_rating_encoded + type_encoded])


feature_names = ['Reviews', 'Price', 'Size', 'Installs'] + all_categories + all_genres + all_content_ratings + ['Type_Paid']
input_df = pd.DataFrame([[reviews, price, size, installs] + category_encoded + genre_encoded + content_rating_encoded + type_encoded],
                        columns=feature_names)

st.markdown("---")
if st.button("Predict Rating"):
    prediction = model.predict(input_df)
    st.success(f"⭐ Predicted Rating: **{prediction[0]:.2f} / 5.0**")

st.markdown("---")

