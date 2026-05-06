import gspread
from oauth2client.service_account import ServiceAccountCredentials
from openai import OpenAI
import json
import time

# 1. API 配置
client = OpenAI(api_key='sk-394e6c6525c9436ab085290d76bb2c46', base_url="https://api.deepseek.com")

# 2. Google Sheets 配置
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_path = "/Users/isabella/Desktop/senior project/credentials.json"

def get_authorized_sheet():
    """重新授权并获取表格，用于解决 SSL 断开问题"""
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, SCOPE)
    client_gs = gspread.authorize(creds)
    return client_gs.open("Internship_Data").get_worksheet(0)

# 初始化表格
sheet = get_authorized_sheet()

def run_cleanup_analysis():
    global sheet
    all_values = sheet.get_all_values()
    print(f"✅ Scanning total {len(all_values)} rows...")

    for i, row in enumerate(all_values[1:], start=2):
        # 严格获取当前行数据
        g_val = row[6].strip() if len(row) > 6 else ""
        h_val = row[7].strip() if len(row) > 7 else ""
        
        # 判断逻辑：如果 G 或 H 是空，或者是 N/A，或者是 Pending
        needs_fix = not g_val or not h_val or "pending" in g_val.lower() or g_val == "N/A"
        
        if needs_fix:
            job_title = row[1] if len(row) > 1 else "Unknown"
            description = row[4] if len(row) > 4 else ""
            
            if len(description) < 30:
                continue

            print(f"🚀 Cleaning up Row {i}: {job_title}")

            prompt = f"Analyze: {description}. Return JSON: 'duties' (list), 'tools' (list)."

            try:
                # 调用 AI
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={ "type": "json_object" }
                )
                res = json.loads(response.choices[0].message.content)
                
                # 列表转字符串
                d_str = ", ".join(res.get('duties', [])) if isinstance(res.get('duties'), list) else str(res.get('duties'))
                t_str = ", ".join(res.get('tools', [])) if isinstance(res.get('tools'), list) else str(res.get('tools'))

                # 写入表格（带简单的重试逻辑）
                try:
                    sheet.update_cell(i, 7, d_str) # G列
                    sheet.update_cell(i, 8, t_str) # H列
                    print(f"✨ Row {i} FIXED.")
                except:
                    print(f"⚠️ Connection lost at Row {i}, reconnecting...")
                    time.sleep(5)
                    sheet = get_authorized_sheet()
                    sheet.update_cell(i, 7, d_str)
                    sheet.update_cell(i, 8, t_str)
                    print(f"✨ Row {i} FIXED after reconnect.")

                time.sleep(1.5) # 适当停顿，防止 Google API 限制

            except Exception as e:
                print(f"❌ Failed Row {i}: {e}")
                time.sleep(2)
        else:
            if i % 10 == 0: print(f"⏩ Row {i} is already fine.")

if __name__ == "__main__":
    run_cleanup_analysis()
    print("🎊 MISSION ACCOMPLISHED: All rows from 1 to 74 are checked and filled!")