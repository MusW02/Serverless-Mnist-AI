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
    <div className="card">
      <h1>Draw a Digit</h1>
      <ReactSketchCanvas 
        ref={canvasRef} 
        strokeWidth={15} 
        strokeColor="black" 
        width="280px" 
        height="280px" 
        style={{border: "2px solid #333"}}
      />
      <div style={{marginTop: "20px"}}>
        <button onClick={() => canvasRef.current.clearCanvas()}>Clear</button>
        <button onClick={handleSubmit}>Predict</button>
      </div>
      {prediction !== null && <h2>Result: {prediction}</h2>}
    </div>
  );
}

export default App;