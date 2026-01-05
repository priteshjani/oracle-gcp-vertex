import streamlit as st
import requests
import pandas as pd

# Streamlit App for Retail Demo

st.set_page_config(page_title="Retail Supermarket Demo", layout="wide")

st.title("🛒 Supermarket AI Search")
st.markdown("### Powered by Google Vertex AI & Oracle Autonomous Database")

API_URL = "http://localhost:8000/search"

# Sidebar
st.sidebar.header("Settings")
st.sidebar.info("This demo connects to a mock backend simulating Oracle DB and Vertex AI.")

# Main Search
query = st.text_input("What are you looking for?", placeholder="e.g., Show me shoes for boys size 7 in blue")

if st.button("Search"):
    if query:
        with st.spinner("Analyzing query with Gemini... searching Oracle Database..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                if response.status_code == 200:
                    items = response.json()

                    if items:
                        st.success(f"Found {len(items)} items matching your request.")

                        # Display items in a grid
                        cols = st.columns(3)
                        for idx, item in enumerate(items):
                            with cols[idx % 3]:
                                st.image(item["image_url"], use_column_width=True)
                                st.subheader(item["name"])
                                st.write(f"**Category:** {item['category']}")
                                st.write(f"**Size:** {item['size']}")
                                st.write(f"**Color:** {item['color']}")
                                st.write(f"**Price:** ${item['price']}")
                    else:
                        st.warning("No items found. Try a different query.")
                else:
                    st.error(f"Error connecting to backend: {response.status_code}")
            except Exception as e:
                # For demo purposes if backend isn't running, show mock result
                st.error(f"Connection failed: {e}")
                st.info("Displaying mock fallback data for demonstration:")

                mock_items = [
                    {"name": "Blue Running Shoes", "category": "Boys", "size": 7, "color": "Blue", "price": 45.99, "image_url": "https://placehold.co/300x300?text=Blue+Shoes"},
                    {"name": "Blue Sneakers", "category": "Boys", "size": 7, "color": "Blue", "price": 49.99, "image_url": "https://placehold.co/300x300?text=Blue+Sneakers"}
                ]
                cols = st.columns(2)
                for idx, item in enumerate(mock_items):
                     with cols[idx % 2]:
                        st.image(item["image_url"], use_column_width=True)
                        st.subheader(item["name"])
                        st.write(f"**Price:** ${item['price']}")

    else:
        st.warning("Please enter a query.")

st.markdown("---")
st.caption("Demo Architecture: React Frontend -> FastAPI Backend -> Vertex AI (Gemini) -> Oracle Autonomous DB (Shared VPC)")
