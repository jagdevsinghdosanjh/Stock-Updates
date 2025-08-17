# 📈 Multi-Company Stock Data Viewer

This Streamlit app allows users to view historical stock data for multiple companies using the Polygon.io API. It displays daily price trends, trading volume, and other key metrics in an interactive format.

---

## 🚀 Features

- 🔍 Select from popular companies like Apple, Microsoft, Tesla, Infosys, and more
- 📊 View daily Open, Close, High, Low prices with interactive charts
- 📅 Data range: January 1, 2025 to May 11, 2025 (modifiable)
- 🧠 Caching enabled for faster performance
- 🔐 Uses environment variable for secure API key management

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/multi-company-stock-app.git
cd multi-company-stock-app

2. Install Dependencies
pip install -r requirements.txt

3. Configure API Key
Create a .env file in the root directory:
POLYGON_API_KEY=your_actual_polygon_api_key_here

Make sure to keep this file private. It's already listed in .gitignore.

4. Run the App
streamlit run app.py

5. 🧪 Requirements
Python 3.8+

Streamlit

Requests

Pandas

python-dotenv (for local .env support)

🌐 Deployment
🔒 Streamlit Cloud
Push your code to GitHub

Go to Streamlit Cloud

Create a new app from your repo

Add your API key in Secrets Manager:
    POLYGON_API_KEY = your_actual_polygon_api_key_here

📂 File Structure
![alt text](FileStructure.jpg)

📌 Notes
You can modify START_DATE and END_DATE in app.py to change the data range.

Add more companies to the COMPANIES dictionary as needed.

Consider modularizing the code for scalability (e.g., separate data fetching logic).

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

📄 License
This project is licensed under the MIT License.

🙌 Acknowledgments
Polygon.io for the stock data API

Streamlit for the interactive UI framework