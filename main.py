import os
import requests
import streamlit as st
from dotenv import load_dotenv
from twilio.rest import Client

# 🔐 Load .env
load_dotenv()

# 🔑 Twilio credentials
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
from_whatsapp_number = os.getenv("TWILIO_PHONE_NUMBER")

# 🔑 Google CSE credentials
google_api_key = os.getenv("GOOGLE_API_KEY")
google_cx = os.getenv("GOOGLE_CX")

# 💬 Twilio Client
client = Client(account_sid, auth_token)

# 📌 Sidebar instructions
st.set_page_config(page_title="MatchGuru-Bot 💞", page_icon="💌", layout="centered")
st.sidebar.markdown("### 🤖 WhatsApp Setup Instructions")
st.sidebar.markdown("""
1. 📲 Apna WhatsApp number se yeh code bhejein:  
   **`join twice-under`**  
   is number par:  
   **+1 (415) 523-8886**

2. 📇 Yeh number apni contacts mein save karein as:  
   **Twilio WhatsApp Bot**

3. ✅ Ab MatchGuru-Bot se WhatsApp par rishtay hasil kar sakte hain!
""")

# 🌐 Search LinkedIn
def search_linkedin_profile(name):
    query = f"{name} site:linkedin.com/in"
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": google_api_key,
        "cx": google_cx,
        "q": query
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "items" in data:
            top = data["items"][0]
            return f"""🔎 *LinkedIn Search Result:*\n📌 *{top.get('title')}*\n🔗 {top.get('link')}\n📝 {top.get('snippet')}"""
        else:
            return "🔍 LinkedIn par koi result nahi mila."
    except Exception as e:
        return f"❌ Search failed: {str(e)}"

# 📤 Send WhatsApp
def send_whatsapp_message(to, msg):
    try:
        message = client.messages.create(
            body=msg,
            from_=from_whatsapp_number,
            to=f"whatsapp:{to}"
        )
        return f"✅ Message sent to {to} (SID: {message.sid})"
    except Exception as e:
        return f"❌ WhatsApp sending failed: {str(e)}"

# 🧠 Streamlit App
def main():
    st.title("🤖 MatchGuru-Bot 💞")
    st.markdown("Aap ke liye behtareen rishtay dhoondhne wala bot, ab LinkedIn info ke sath!")

    with st.form("match_form"):
        gender = st.selectbox("Ap kis ka rishta dhoond rahay hain?", ["Larka", "Larki"])
        name = st.text_input("Naam kya hai?")
        age = st.text_input("Umar (approx)?")
        profession = st.text_input("Profession?")
        city = st.text_input("City ya Country?")
        whatsapp_number = st.text_input("Apna WhatsApp number (+923xx...)")
        submitted = st.form_submit_button("🔍 Rishta Search Karo")

        if submitted:
            with st.spinner("LinkedIn par search aur WhatsApp par message bhej rahe hain..."):
                profile_text = f"""📄 *MatchGuru Rishta Report:*

👤 Name: {name.title()}
🎂 Age: ~{age}
💼 Profession: {profession.title()}
🌍 Location: {city.title() if city else 'Not specified'}

📇 Profile Summary:
{name.title()} is a professional {profession.lower()} based in {city or 'an unspecified location'}.
"""
                linkedin_info = search_linkedin_profile(name)
                final_msg = profile_text + "\n" + linkedin_info
                st.code(final_msg)
                result = send_whatsapp_message(whatsapp_number, final_msg)
                st.success(result)

if __name__ == "__main__":
    main()
