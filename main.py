from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# ตั้งค่า CORS ให้รองรับทุก origin หรือกำหนดเฉพาะที่ต้องการ
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # หรือใส่แค่ origin ที่ต้องการ เช่น "http://127.0.0.1:5500"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# สร้าง function ที่จะส่งข้อมูลไปยัง client อย่างต่อเนื่อง
def event_stream():
    print("event_stream")
    while True:
        time.sleep(1)  # รอ 1 วินาที
        print(time.strftime('%Y-%m-%d %H:%M:%S'))
        # ส่งข้อมูลเวลาเป็น message ทุกๆ 1 วินาที
        yield f"data: The time is {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n"

# กำหนด route สำหรับส่งข้อมูล SSE
@app.get("/events")
async def get_events():
    return StreamingResponse(event_stream(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8010)
