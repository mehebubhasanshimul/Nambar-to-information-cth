from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/api/check-number")
async def check_number(number: str):
    target_url = f"https://sbsakib.eu.cc/apis/truecaller?key=Test&number1={number}"
    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)
        # এপিআই থেকে সরাসরি ডেটা রিটার্ন করবে যা ফ্রন্টএন্ডে রিসিভ করবেন
        return response.json()
