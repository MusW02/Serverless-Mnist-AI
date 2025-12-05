import { useState, useRef } from 'react';
import { ReactSketchCanvas } from 'react-sketch-canvas';
import axios from 'axios';
import './App.css';

// ⚠️ Ensure this is your live Lambda URL
const API_URL = "https://jg65ekrwln3agbhuagz2l3uobu0lnsfh.lambda-url.eu-north-1.on.aws/";
//const API_URL = "http://localhost:8000/";

function App() {
  const canvasRef = useRef(null);
  const [prediction, setPrediction] = useState(null);
  const [probabilities, setProbabilities] = useState(Array(10).fill(0));
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    try {
      setLoading(true);
      const imageBase64 = await canvasRef.current.exportImage("png");
      const base64String = imageBase64.split(',')[1];

      const response = await axios.post(`${API_URL}predict`, {
        image: base64String
      });

      setPrediction(response.data.digit);
      
      if (response.data.probabilities && Array.isArray(response.data.probabilities)) {
        setProbabilities(response.data.probabilities);
      }
    } catch (err) {
      console.error("Prediction error:", err);
      alert("Error connecting to backend.");
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    canvasRef.current.clearCanvas();
    setPrediction(null);
    setProbabilities(Array(10).fill(0));
  };

  return (
    <div className="app-container">
      {/* Updated Heading */}
      <header className="app-bar">
        <h1>Serverless Application Deployment: Handwritten Digit Recognition</h1>
      </header>

      <main className="main-content">
        
        {/* Left Side: Drawing Area */}
        <div className="canvas-section">
          <h2>Draw any digit (0-9) here</h2>
          
          <div className="canvas-container">
            <ReactSketchCanvas
              ref={canvasRef}
              strokeWidth={40}       
              strokeColor="black"
              canvasColor="white"
              width="100%"
              height="100%"
              className="sketch-canvas"
            />
          </div>

          <div className="controls">
            <button className="btn-clear" onClick={handleClear}>
              ✕ CLEAR
            </button>
            <button className="btn-predict" onClick={handlePredict} disabled={loading}>
              {loading ? "..." : "PREDICT"}
            </button>
          </div>
        </div>

        {/* Right Side: Probability Bar Chart */}
        <div className="chart-section">
          {probabilities.map((prob, index) => (
            <div key={index} className="chart-row">
              {/* Highlight winner */}
              <span className={`digit-label ${index === prediction ? 'winner-text' : ''}`}>
                {index}
              </span>
              
              <div className="bar-track">
                {/* Gradient Bar */}
                <div 
                  className={`bar-fill ${index === prediction ? 'winner-bar' : ''}`}
                  style={{ width: `${prob * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>

      </main>
    </div>
  );
}

export default App;
