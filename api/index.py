from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import os

app = FastAPI()

# আপনার API Key এখানে রাখা হলো
API_KEY = "pk_live_8314066e3876952986f7175223152842d3316b37"

# ১. হোম রুট: এটি আপনার index.html ফাইলটি লোড করবে
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        file_path = os.path.join(os.getcwd(), "index.html")
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <body style="background:#0f172a; color:white; display:flex; justify-content:center; align-items:center; height:100vh; font-family:sans-serif;">
                <div style="text-align:center;">
                    <h1>Index.html Not Found!</h1>
                    <p>দয়া করে নিশ্চিত করুন যে আপনার index.html ফাইলটি রুট ডিরেক্টরিতে আছে।</p>
                </div>
            </body>
        </html>
        """

# ২. এপিআই রুট: ফ্রন্টএন্ড থেকে এই লিঙ্কে রিকোয়েস্ট আসবে
@app.get("/api/check")
async def check_number(number: str):
    if not number:
        raise HTTPException(status_code=400, detail="Number is required")
    
    # নতুন এপিআই ইউআরএল এবং কী সেটআপ
    target_url = f"https://api.lookupnow.top/api/v1/query.php?key={API_KEY}&number={number}"
    
    async with httpx.AsyncClient() as client:
        try:
            # এপিআই থেকে ডেটা সংগ্রহ
            response = await client.get(target_url, timeout=15.0)
            
            if response.status_code == 200:
                # সরাসরি এপিআই থেকে পাওয়া JSON ডাটা রিটার্ন করবে
                return response.json()
            else:
                return {
                    "status": "error", 
                    "message": f"API server returned status code {response.status_code}"
                }
                
        except httpx.RequestError as exc:
            return {"status": "error", "message": f"An error occurred while requesting: {exc}"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# ৩. প্রজেক্ট স্ট্যাটাস চেক
@app.get("/status")
async def status():
    return {"status": "online", "project": "Cyber Team Help", "api_provider": "LookupNow"}
