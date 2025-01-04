import React from 'react';

function AnalysisResult({ result }) {
  console.log("AnalysisResult received result:", result);

  if (!result) {
    return null;
  }

  return (
    <div className="results-section">
      <h4>Analysis Results:</h4>
      <p><strong>Season:</strong> {result.season}</p>
      <p><strong>Recommended Colors:</strong> {result.recommendations.clothes}</p>
      <p><strong>Makeup Suggestions:</strong> {result.recommendations.makeup}</p>
      <p><strong>Jewelry Tone:</strong> {result.recommendations.jewelry}</p>
    </div>
  );
}

export default AnalysisResult;