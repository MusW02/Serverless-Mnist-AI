import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
import base64
from PIL import Image, ImageOps
from io import BytesIO

# 1. Initialize FastAPI
app = FastAPI()

# 2. Add CORS (Allows your future frontend to talk to this backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows ANY frontend to connect (Change this for production!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Load Model (Global scope so it loads only once)
session = ort.InferenceSession("mnist-8.onnx")

# 4. Define Input Data Structure
class ImageInput(BaseModel):
    image: str  # Base64 string

@app.get("/")
def root():
    return {"message": "MNIST Serverless API is running!"}

@app.post("/predict")
def predict(input_data: ImageInput):
    try:
        # Decode Base64
        image_data = base64.b64decode(input_data.image)
        
        # Preprocess Image (Same logic as before)
        img = Image.open(BytesIO(image_data)).convert('L')
        img = ImageOps.invert(img)
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
        
        # Convert to Numpy
        img_array = np.array(img, dtype=np.float32).reshape(1, 1, 28, 28) / 255.0
        
        # Inference
        inputs = {session.get_inputs()[0].name: img_array}
        outputs = session.run(None, inputs)
        prediction = int(np.argmax(outputs[0]))
        
        return {"digit": prediction}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 5. The Bridge for AWS Lambda
handler = Mangum(app)