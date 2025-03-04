import streamlit as st
import pandas as pd
import sqlite3
import numpy as np
import joblib
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# Database connection
conn = sqlite3.connect("fitness_tracker.db")
cursor = conn.cursor()

# User authentication
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
""")
conn.commit()

# Function to create a new user
def signup_user(username, password):
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

# Function to check user login
def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    return cursor.fetchone()

# Page selection
def main():
    st.title("🏋️ **Personal Fitness Tracker**")
    
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"
    
    if st.session_state["page"] == "Home":
        st.markdown("<h3 style='color:white; font-weight:bold;'>Welcome! Please choose an option:</h3>", unsafe_allow_html=True)
        if st.button("Login"):
            st.session_state["page"] = "Login"
            st.rerun()
        if st.button("Sign Up"):
            st.session_state["page"] = "Sign Up"
            st.rerun()

    elif st.session_state["page"] == "Sign Up":
        st.markdown("<h3 style='color:white; font-weight:bold;'>Create an Account</h3>", unsafe_allow_html=True)
        new_user = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            if signup_user(new_user, new_password):
                st.success("Account created successfully! Redirecting to Login...")
                st.session_state["page"] = "Login"
                st.rerun()
            else:
                st.error("Username already exists. Try another one.")

    elif st.session_state["page"] == "Login":
        st.markdown("<h3 style='color:white; font-weight:bold;'>Login to Your Account</h3>", unsafe_allow_html=True)
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if login_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("Login successful! Redirecting to Fitness Tracking...")
                st.session_state["page"] = "Track Fitness"
                st.rerun()
            else:
                st.error("Invalid username or password.")

    elif st.session_state["page"] == "Track Fitness":
        if "logged_in" in st.session_state:
            st.markdown("<h3 style='color:white; font-weight:bold;'>Fitness Progress Dashboard</h3>", unsafe_allow_html=True)

            @st.cache_data
            def load_data():
                df = pd.read_csv("cleaned_fitness_data.csv")
                return df

            df = load_data()
            df.to_sql("merged_data", conn, if_exists="replace", index=False)

            @st.cache_resource
            def train_model():
                X = df[['Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']]
                y = df['Calories']
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
                model = LinearRegression()
                model.fit(X_train, y_train)
                joblib.dump(model, "calorie_predictor.pkl")
                return model

            model = train_model()

            st.sidebar.markdown("<h3 style='color:black; font-weight:bold;'>🔥 Predict Calories Burned</h3>", unsafe_allow_html=True)
            age = st.sidebar.number_input("Age", min_value=10, max_value=100, value=25)
            weight = st.sidebar.number_input("Weight (kg)", value=70)
            height = st.sidebar.number_input("Height (cm)", value=175)
            duration = st.sidebar.number_input("Exercise Duration (min)", value=30)
            heart_rate = st.sidebar.number_input("Heart Rate (bpm)", value=80)
            body_temp = st.sidebar.number_input("Body Temperature (°C)", value=36.5)

            if st.sidebar.button("Predict"):
                input_data = np.array([[age, height, weight, duration, heart_rate, body_temp]])
                prediction = model.predict(input_data)[0]
                st.sidebar.success(f"🔥 Estimated Calories Burned: {prediction:.2f} kcal")

            # Adding detailed fitness tips after login
            st.markdown("<h3 style='color:blue; font-weight:bold;'>💡 Detailed Fitness Tips</h3>", unsafe_allow_html=True)
            
            # 1. The Importance of Staying Active
            st.subheader("1️⃣ The Importance of Staying Active")  
            st.write("""
            - Regular exercise improves cardiovascular health, boosts metabolism, and reduces stress.
            - Aim for at least **30 minutes of moderate activity** (walking, jogging, or cycling) daily.
            """)  

            # 2. Hydration Matters
            st.subheader("2️⃣ Hydration Matters 💧")  
            st.write("""
            - Water is essential for digestion, energy levels, and muscle recovery.
            - Drink **at least 8 glasses (2 liters)** of water daily, more if you exercise intensely.
            """)  

            # 3. Sleep & Recovery
            st.subheader("3️⃣ Sleep & Recovery 😴")  
            st.write("""
            - Quality sleep (7-9 hours per night) improves muscle recovery and mental focus.
            - Avoid screens before bed, and follow a consistent sleep schedule for better rest.
            """)  

            # 4. Nutrition for Optimal Performance
            st.subheader("4️⃣ Nutrition for Optimal Performance 🥗")  
            st.write("""
            - Balance your diet with **40% carbs, 30% protein, and 30% healthy fats** for energy and muscle growth.
            - Include **lean proteins (chicken, fish, beans), whole grains, and fresh vegetables** in every meal.
            """)  

            # 5. Pre & Post-Workout Nutrition
            st.subheader("5️⃣ Pre & Post-Workout Nutrition")  
            st.write("""
            - **Before Workout**: Eat a light meal with complex carbs & protein (e.g., banana with peanut butter).
            - **After Workout**: Refuel with protein (chicken, eggs, whey) to aid muscle recovery.
            """)  

            # 6. Stretching & Injury Prevention
            st.subheader("6️⃣ Stretching & Injury Prevention 🤸‍♂️")  
            st.write("""
            - Always warm up before workouts to prevent injuries.
            - Include dynamic stretching before workouts and static stretching afterward to improve flexibility.
            """)  

            # 7. Fitness Myths Busted
            st.subheader("7️⃣ Fitness Myths Busted 🔍")  
            st.write("""
            ❌ **"Lifting weights makes you bulky"** – Strength training boosts metabolism and burns fat.  
            ❌ **"More sweat means more fat loss"** – Sweat is water loss, not fat loss.  
            ❌ **"Carbs are bad for you"** – Healthy carbs like oats, quinoa, and sweet potatoes provide energy.  
            """)  

            # 8. Stress & Mental Well-Being
            st.subheader("8️⃣ Stress & Mental Well-Being 🧘‍♂️")  
            st.write("""
            - Physical activity releases **endorphins ("feel-good" hormones)** that reduce stress and anxiety.
            - Try meditation, yoga, or deep breathing exercises to improve mental well-being.
            """)  
            
            st.markdown("<h3 style='color:black; font-weight:bold;'>📊 Fitness Charts</h3>", unsafe_allow_html=True)

            # Categorize age into groups
            df['Age_Group'] = pd.cut(df['Age'], bins=[0, 18, 35, 60, 100], labels=['Young', 'Adult', 'Middle-Aged', 'Elder'])

            filter_option = st.selectbox("Filter Data By:", ["All", "Male", "Female"])
            if filter_option == "Male":
                df = df[df['Gender'] == 'male']
            elif filter_option == "Female":
                df = df[df['Gender'] == 'female']

            fig1 = px.scatter(df, x="Weight", y="Calories", color="Gender", title="📈 Weight vs Calories Burned", labels={"Weight": "Weight (kg)", "Calories": "Calories Burned"})
            fig2 = px.scatter(df, x="Duration", y="Calories", color="Gender", title="🔥 Duration vs Calories Burned", labels={"Duration": "Exercise Duration (min)", "Calories": "Calories Burned"})
            fig3 = px.scatter(df, x="Heart_Rate", y="Body_Temp", color="Gender", title="💓 Heart Rate vs Body Temperature", labels={"Heart_Rate": "Heart Rate (bpm)", "Body_Temp": "Body Temperature (°C)"})
            fig4 = px.histogram(df, x="Gender", y="Calories", color="Age_Group", title="👫 Gender vs Calories Burned by Age Group", labels={"Gender": "Gender", "Calories": "Calories Burned"})
            fig1.update_layout(template="plotly_dark", font=dict(color="white"))
            fig2.update_layout(template="plotly_dark", font=dict(color="white"))
            fig3.update_layout(template="plotly_dark", font=dict(color="white"))
            fig4.update_layout(template="plotly_dark", font=dict(color="white"))
            st.plotly_chart(fig1)
            st.plotly_chart(fig2)
            st.plotly_chart(fig3)
            st.plotly_chart(fig4)

            st.markdown("<h3 style='color:black; font-weight:bold;'>💡Fitness Tips</h3>", unsafe_allow_html=True)
            st.markdown("""
                - **Stay Consistent:** Consistency is key to achieving your fitness goals. Stick to your workout routine and track your progress regularly.
                - **Balanced Diet:** Ensure you have a balanced diet that includes a variety of nutrients to fuel your body.
                - **Stay Hydrated:** Drink plenty of water throughout the day to stay hydrated, especially during workouts.
                - **Rest and Recovery:** Give your body enough time to rest and recover to avoid injuries and improve performance.
                - **Set Realistic Goals:** Set achievable fitness goals and celebrate your progress along the way.
            """)
            
           
        else:
            st.warning("Please log in to access this feature.")

if __name__ == "__main__":
    main()