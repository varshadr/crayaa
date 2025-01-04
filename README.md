# Color Analysis Application

This project is a color analysis application that consists of a Flask backend and a React frontend. The application allows users to analyze colors and get insights based on their input.

## Project Structure

```
color-analysis-app
├── backend
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── public
│   │   ├── index.html
│   └── src
│       ├── App.js
│       ├── index.js
│       └── components
│           └── ColorAnalyzer.js
├── package.json
├── README.md
└── .gitignore
```

## Setup Instructions

### Backend

1. Navigate to the `backend` directory:
   ```
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Flask app:
   ```
   python app.py
   ```

### Frontend

1. Navigate to the `frontend` directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Build the React app:
   ```
   npm run build
   ```

4. Serve the build folder using a static server or deploy it to a hosting service like Vercel or Netlify.

## Deployment Instructions

### Combine Both

1. Ensure the backend is running and accessible.
2. Configure the frontend to make API calls to the backend's endpoint for color analysis.

## License

This project is licensed under the MIT License.