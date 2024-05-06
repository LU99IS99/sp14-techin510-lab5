import os
import streamlit as st
from datetime import date
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Google generative AI with an API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Function to generate travel plans based on user input using Google AI
def ai_gen_travel_plan(destination, start_date, end_date, activities, budget):
    requirement = f"Generate a travel plan for {destination} from {start_date} to {end_date}. Activities: {', '.join(activities)}. Budget: ${budget}."
    response = model.generate_content([requirement])
    return response.text

# Main function for Streamlit app
def main():
    st.title("AI-Powered Travel Planner 🌍")

    # Travel destination input
    destination = st.text_input("Enter your travel destination", "New York")

    # Travel dates input
    start_date = st.date_input("Start date", date.today())
    end_date = st.date_input("End date", date.today())

    # Select activities of interest
    activities_list = ['Sightseeing', 'Hiking', 'Beach', 'Museums', 'Shopping', 'Nightlife']
    activities = st.multiselect("What activities are you interested in?", activities_list)

    # Budget input
    budget = st.slider("What is your budget for this trip?", 100, 10000, 1000)

    # Button to generate travel plan
    if st.button("Generate Travel Plan"):
        with st.spinner("Generating your AI-powered travel plan..."):
            travel_plan = ai_gen_travel_plan(destination, start_date, end_date, activities, budget)
            st.success("Here is your AI-generated travel plan:")
            st.write(travel_plan)

if __name__ == "__main__":
    main()
