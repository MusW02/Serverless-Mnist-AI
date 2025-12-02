import { useState, useRef } from 'react';
import { ReactSketchCanvas } from 'react-sketch-canvas';
import axios from 'axios';
import './App.css';

const API_URL = "https://jg65ekrwln3agbhuagz2l3uobu0lnsfh.lambda-url.eu-north-1.on.aws/"; // Ensure it ends with /

function App() {
  const canvasRef = useRef(null);
  const [prediction, setPrediction] = useState(null);

  const handleSubmit = async () => {
    // 1. Get image from canvas
    const image = await canvasRef.current.exportImage("png");
    const base64 = image.split(',')[1]; // Remove "data:image/png..." header

    // 2. Send to FastAPI
    try {
      const res = await axios.post(`${API_URL}predict`, { image: base64 });
      setPrediction(res.data.digit);
    } catch (error) {
      console.error(error);
      alert("Backend error!");
    }
  };

  return (
    <div className="app-container">
      <h1>Draw a Digit</h1>
      <div className="canvas-wrapper">
        <ReactSketchCanvas 
          ref={canvasRef} 
          strokeWidth={15} 
          strokeColor="#00ffcc" 
          width="280px" 
          height="280px" 
        />
      </div>
      <div className="controls">
        <button className="btn clear" onClick={() => canvasRef.current.clearCanvas()}>Clear</button>
        <button className="btn predict" onClick={handleSubmit}>Predict</button>
      </div>
      {prediction !== null && <div className="result">Result: {prediction}</div>}
    </div>
  );
}

export default App;
