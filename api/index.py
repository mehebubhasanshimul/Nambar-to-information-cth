from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import httpx
import os

app = FastAPI()

# ১. হোম রুট: এটি আপনার index.html ফাইলটি লোড করবে
@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        # রুট ডিরেক্টরিতে থাকা index.html ফাইলটি পড়ার চেষ্টা করবে
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
    
    # টার্গেট এপিআই ইউআরএল
    target_url = f"https://sbsakib.eu.cc/apis/truecaller?key=Test&number1={number}"
    
    async with httpx.AsyncClient() as client:
        try:
            # এপিআই থেকে ডেটা সংগ্রহ
            response = await client.get(target_url, timeout=10.0)
            
            # যদি এপিআই থেকে সফল রেসপন্স আসে
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "error", "message": "API server returned an error"}
                
        except Exception as e:
            # কোনো কানেকশন এরর হলে
            return {"status": "error", "message": str(e)}

# ৩. হেলথ চেক রুট (অপশনাল)
@app.get("/status")
async def status():
    return {"status": "online", "project": "Cyber Team Help"}
