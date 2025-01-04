import './ImageUploader.css';
import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import AnalysisResult from './AnalysisResult';

function ImageUploader() {
  const [file, setFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);

  useEffect(() => {
    if (isCameraActive) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
          videoRef.current.srcObject = stream;
        })
        .catch((err) => {
          setError("Error accessing the camera: " + err.message);
        });
    }
    return () => {
      if (videoRef.current?.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, [isCameraActive]);

  const handleFileChange = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile);
      setImagePreview(URL.createObjectURL(uploadedFile));
      setError(null);
    }
  };

  const captureImage = () => {
    const canvas = canvasRef.current;
    const video = videoRef.current;
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);
    
    canvas.toBlob((blob) => {
      setFile(blob);
      setImagePreview(URL.createObjectURL(blob));
    }, 'image/jpeg');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const formData = new FormData();
    if (file instanceof Blob) {
      formData.append('file', file);
    } else if (typeof file === 'string') {
      formData.append('image', file);
    }

    try {
      const response = await axios.post('http://localhost:5001/api/analyze', formData, {  // Update the port number here if needed
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      console.log("Response data:", response.data);
      setResult(response.data);
    } catch (error) {
      console.error("Error:", error);
      console.error("Error response:", error.response);
      setError(error.response?.data?.error || "Error analyzing image");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h3>Color Analysis Tool</h3>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit}>
        <div className="upload-section">
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <button type="button" onClick={() => setIsCameraActive(!isCameraActive)}>
            {isCameraActive ? 'Stop Camera' : 'Start Camera'}
          </button>
        </div>

        {isCameraActive && (
          <div className="camera-section">
            <video ref={videoRef} autoPlay playsInline />
            <canvas ref={canvasRef} style={{ display: 'none' }} />
            <button type="button" onClick={captureImage}>Capture</button>
          </div>
        )}

        {imagePreview && (
          <div className="preview-section">
            <h4>Preview:</h4>
            <img src={imagePreview} alt="Preview" />
          </div>
        )}

        <button type="submit" disabled={!file || loading}>
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </form>

      <AnalysisResult result={result} />
    </div>
  );
}

export default ImageUploader;