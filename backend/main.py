import os
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from ultralytics import YOLO
import torch
import cv2
import numpy as np
from io import BytesIO
import uuid

app = FastAPI()

# Static and template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Device and model
device = 'mps' if torch.backends.mps.is_available() else 'cpu'
model = YOLO('best.pt')

# Class labels and colors
class_names = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
          (255, 0, 255), (0, 255, 255), (128, 0, 128), (0, 128, 128),
          (128, 128, 0), (0, 0, 0)]

def read_imagefile(file) -> np.ndarray:
    image_bytes = BytesIO(file).read()
    np_arr = np.frombuffer(image_bytes, np.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

def annotate_predictions(image: np.ndarray, results):
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        confidence = float(box.conf[0])
        label_index = int(box.cls[0])
        label_name = class_names[label_index]
        color = colors[label_index % len(colors)]
        label_text = f"{label_name} ({confidence:.2f})"

        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
        cv2.putText(image, label_text, (x1, y1 - 10),
                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    return image

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_images(files: List[UploadFile] = File(...)):
    results_data = []

    for file in files:
        contents = await file.read()
        image = read_imagefile(contents)
        results = model(image, conf=0.25)[0]
        image = annotate_predictions(image, results)

        # Save annotated image
        filename = f"{uuid.uuid4().hex}.jpg"
        output_path = f"static/uploads/{filename}"
        cv2.imwrite(output_path, image)

        # Extract prediction info
        predictions = []
        for box in results.boxes:
            confidence = float(box.conf[0])
            label_index = int(box.cls[0])
            label_name = class_names[label_index]
            predictions.append({
                "label": label_name,
                "confidence": round(confidence, 3)
            })

        results_data.append({
            "image_url": f"/static/uploads/{filename}",
            "predictions": predictions
        })

    return JSONResponse(content={"results": results_data})
