import numpy as np
import onnxruntime as ort
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from pydantic import BaseModel
import base64
from PIL import Image, ImageOps
from io import BytesIO

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
session = ort.InferenceSession("mnist-8.onnx")

class ImageInput(BaseModel):
    image: str

@app.get("/")
def root():
    return {"message": "MNIST Serverless API is running!"}

@app.post("/predict")
def predict(input_data: ImageInput):
    try:
        # 1. Decode Image
        image_data = base64.b64decode(input_data.image)
        img = Image.open(BytesIO(image_data)).convert('L')
        
        # 2. SMART INVERSION (Crucial for the new Light UI)
        # Calculate the average pixel brightness (0=Black, 255=White)
        img_np = np.array(img)
        avg_brightness = np.mean(img_np)
        
        # If the image is mostly light (> 127), invert it to match the model's training data (White digit on Black background)
        if avg_brightness > 127:
            img = ImageOps.invert(img)

        # 3. Resize to 28x28 (Standard MNIST size)
        img = img.resize((28, 28), Image.Resampling.LANCZOS)
        
        # 4. Normalize (0 to 1)
        img_array = np.array(img, dtype=np.float32).reshape(1, 1, 28, 28) / 255.0
        
        # 5. Run Inference
        inputs = {session.get_inputs()[0].name: img_array}
        outputs = session.run(None, inputs)
        
        # 6. Calculate Probabilities (Softmax)
        raw_output = outputs[0][0]
        exp_scores = np.exp(raw_output - np.max(raw_output)) # Subtract max for stability
        probs = exp_scores / np.sum(exp_scores)
        
        prediction = int(np.argmax(probs))
        
        return {
            "digit": prediction,
            "probabilities": probs.tolist() # Required for the Bar Chart
        }

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

handler = Mangum(app)



# --------------------------------
#gpt content

# import numpy as np
# import onnxruntime as ort
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from mangum import Mangum
# from pydantic import BaseModel
# import base64
# from PIL import Image, ImageOps
# from io import BytesIO

# app = FastAPI()

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Load ONNX Model
# session = ort.InferenceSession("mnist-8.onnx")

# class ImageInput(BaseModel):
#     image: str

# @app.get("/")
# def root():
#     return {"message": "MNIST API Running"}

# @app.post("/predict")
# def predict(input_data: ImageInput):
#     try:
#         # Decode
#         img_bytes = base64.b64decode(input_data.image)
#         img = Image.open(BytesIO(img_bytes)).convert("L")

#         # Auto-invert if drawn on white background
#         img_np = np.array(img)
#         if np.mean(img_np) > 127:
#             img = ImageOps.invert(img)

#         # Resize to 28×28
#         img = img.resize((28, 28), Image.Resampling.LANCZOS)

#         # Normalize
#         img_array = np.array(img, dtype=np.float32).reshape(1, 1, 28, 28) / 255.0

#         # Inference
#         input_name = session.get_inputs()[0].name
#         raw_output = session.run(None, {input_name: img_array})[0][0]

#         # Softmax
#         exp_scores = np.exp(raw_output - raw_output.max())
#         probs = exp_scores / exp_scores.sum()

#         return {
#             "digit": int(np.argmax(probs)),
#             "probabilities": probs.tolist()
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# handler = Mangum(app)
