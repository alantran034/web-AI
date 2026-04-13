import os
import uuid
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO

app = FastAPI()

# Cấu hình để truy cập hình ảnh từ web 
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
model = YOLO('model/yolo11n.pt')

# Đảm bảo các thư mục tồn tại
os.makedirs("static/results", exist_ok=True)
os.makedirs("static/test_images", exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Lấy danh sách file trong thư mục test
    test_files = os.listdir("static/test_images")
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={"test_files": test_files, "detections": None}
    )

@app.post("/predict")
async def predict(request: Request, file: UploadFile = File(None), test_image: str = Form(None)):
    # 1. Xác định ảnh đầu vào: từ upload hoặc từ thư mục test 
    if file and file.filename:
        file_path = f"static/results/{uuid.uuid4()}_{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())
    elif test_image:
        file_path = f"static/test_images/{test_image}"
    else:
        return "No image provided"

    # 2. Chạy AI và vẽ Bounding Box     
    results = model(file_path)
    res_plotted = results[0].plot() # Vẽ khung nhận diện
    
    # 3. Lưu ảnh kết quả
    result_filename = f"res_{uuid.uuid4()}.jpg"
    result_path = f"static/results/{result_filename}"
    import cv2
    cv2.imwrite(result_path, res_plotted)

    # 4. Trích xuất thông tin bảng 
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": model.names[int(box.cls)],
                "conf": f"{float(box.conf)*100:.2f}%"
            })

    test_files = os.listdir("static/test_images")
    return templates.TemplateResponse(
        request=request, 
        name="index.html", 
        context={
            "test_files": test_files,
            "detections": detections,
            "result_image": f"/static/results/{result_filename}"
        }
    )