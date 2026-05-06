import gspread
from oauth2client.service_account import ServiceAccountCredentials
from openai import OpenAI
import json
import time

client = OpenAI(api_key='sk-394e6c6525c9436ab085290d76bb2c46', base_url="https://api.deepseek.com")

creds_path = '/Users/isabella/Desktop/senior project/credentials.json' 
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
gc = gspread.authorize(creds)

def extract_skills():
    sheet = gc.open("Internship_Data").sheet1
    all_rows = sheet.get_all_values()

    for i, row in enumerate(all_rows[1:], start=2):
        has_h = len(row) > 7 and row[7].strip() != ""
        has_i = len(row) > 8 and row[8].strip() != ""
        
        if has_h and has_i:
            continue

        job_description = row[4] if len(row) > 4 else ""
        if not job_description.strip() or len(job_description) < 20:
            continue

        prompt = f"""
        Extract skills from: "{job_description}"
        Return JSON with keys: "technical", "soft", "tools". 
        If none, use ["N/A"].
        """
        
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )
            data = json.loads(response.choices[0].message.content)
            
            tech = ", ".join(data.get('technical', [])) or "N/A"
            soft = ", ".join(data.get('soft', [])) or "N/A"
            tools = ", ".join(data.get('tools', [])) or "N/A"

            sheet.update_cell(i, 8, tech)
            sheet.update_cell(i, 9, soft)
            sheet.update_cell(i, 10, tools)
            
            print(f"Row {i} success")
            time.sleep(2)
            
        except Exception as e:
            print(f"Row {i} error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    extract_skills()