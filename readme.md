🛡️ Appscrip Trade Intel Dashboard
A high-performance Market Intelligence Tool built with a FastAPI backend and Streamlit frontend. This application leverages the Gemini 2.5 Flash-Lite model to generate professional Indian trade reports based on real-time market data.

🚀 Key Features
Real-Time Data: Integrates DuckDuckGo Search to pull the latest 2025 Indian market trends before generating reports.

Resilient AI Engine: Implements an Automatic Fallback Loop. If the primary model is unavailable (404 Error), it instantly cycles through secondary models to ensure zero downtime.

Free-Tier Optimization: Hardcoded for Gemini 2.5 Flash-Lite to provide high-rate limits (30 RPM) without requiring a paid billing account.

Smart Rate-Limiting: Includes a frontend Countdown Timer that triggers if the Free Tier API quota is hit (429 Error), preventing app crashes.

Comparison Mode: A side-by-side analysis hub with Markdown Export functionality for downloading combined reports.

🛠️ Tech Stack
Frontend: Streamlit (Python)

Backend: FastAPI (Uvicorn)

AI: Google Gemini SDK (2.5 Flash-Lite)

Search: DuckDuckGo Search API

Security: Header-based API Key Authentication

📥 Installation & Setup
1. Clone & Environment
Bash

git clone https://github.com/CodeSculpt-RG
cd appscrip-assignment
Create a .env file in the root directory:

Code snippet

GEMINI_API_KEY=your_google_api_key_here
2. Install Dependencies
Bash

pip install fastapi uvicorn streamlit google-genai duckduckgo-search python-dotenv requests
3. Run the Backend
Bash

# From the root directory
python app/main.py
The backend will start at http://localhost:8001

4. Run the Frontend
Bash

streamlit run dashboard.py
📖 Usage Guide
Authentication: Enter the X-API-KEY (default: appscrip_assignment_secret) in the sidebar.

Generate: Go to Analysis Hub, enter a sector (e.g., "Green Hydrogen"), and click Analyze.

Compare: Click the ➕ icon in the History sidebar to add multiple reports to the Comparison View.

Export: In the Comparison tab, use the Download Combined Report button to save your findings.

🛡️ Error Handling Logic
This project includes "Production-Grade" error handling:

404 NOT FOUND: If the Google API region doesn't support a specific model, the backend automatically retries with a broader model family.

429 TOO MANY REQUESTS: The frontend detects the 429 status and initiates a 60-second cooldown UI, disabling the generation button to protect the API key's reputation.

Developed by: G Rahul