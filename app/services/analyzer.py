from google import genai
import os

class TradeAnalyzer:
    def __init__(self):
        # Uses the new unified 2025 SDK
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    async def generate_report(self, sector: str, raw_news: str):
        prompt = f"""
        Analyze these news results for the {sector} sector in India:
        {raw_news}
        
        Generate a professional Markdown report with:
        # Market Report: {sector.upper()}
        ## SWOT Analysis
        ## FDI & Government Schemes (PLI)
        ## Strategic Conclusion
        """
        response = self.client.models.generate_content(
            model='gemini-2.0-flash', # Latest 2025 model
            contents=prompt
        )
        return response.text