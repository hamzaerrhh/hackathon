# RH Agent - AI Chat Application

A modern AI-powered chat application for HR (Human Resources) assistance, built with React and Flask.

## Features

<img src="https://screendy-cdn.fra1.cdn.digitaloceanspaces.com/platfrom-v2/_files/file_1758053485392_diagram.png" alt width="704" height="713" class="rounded-lg shadow border-[1px] border-gray-200" draggable="false" style="display: block;">

- 🤖 **AI-Powered Chat**: Integrated with Google Gemini AI for intelligent responses
- 💬 **Real-time Messaging**: Smooth chat interface with typing indicators
- 📱 **Responsive Design**: Works on desktop and mobile devices
- 🎨 **Modern UI**: Beautiful glassmorphism design with animations
- 🔄 **Dual Interface**: Full-page chat and modal popup options
- ⚡ **Quick Actions**: Pre-defined buttons for common HR topics

## Tech Stack

### Frontend

- React 18
- Axios for API calls
- Custom CSS with animations
- Responsive design

### Backend

- Flask (Python)
- Google Gemini AI
- MongoDB Atlas
- CORS enabled
- ML library (pandas,pycle....)

## Setup Instructions

### 1. Backend Setup

1. Navigate to the server directory:

   ```bash
   cd server
   ```

2. Install dependencies:

   ```bash
   python setup.py
   ```

   Or manually:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Edit the `.env` file with your API keys:

   ```env
   gemini_ai_key=your_gemini_api_key_here
   user_pass=your_mongodb_username
   pass_key=your_mongodb_password
   ```

4. Start the Flask server:
   ```bash
   python main.py
   ```
   The API will be available at `http://localhost:5000`

### 2. Frontend Setup

1. Navigate to the client directory:

   ```bash
   cd client
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   The app will be available at `http://localhost:5173`

## API Endpoints

- `POST /api/chat` - Send a message to the AI
- `GET /api/health` - Health check for the chat API
- `GET /` - General health check

## Usage

1. Start both the backend and frontend servers
2. Open your browser and navigate to the frontend URL
3. Start chatting with the AI assistant
4. Use quick action buttons for common HR topics

## Project Structure

```
Dataset-genAI/
│
├── client/                         # React Frontend
│   ├── src/
│   │   ├── components/             # Reusable UI components
│   │   ├── pages/                  # Application pages
│   │   └── assets/                 # Static assets (images, styles, etc.)
│   └── package.json                # Frontend dependencies
│
├── server/                         # Flask Backend
│   ├── main.py                     # Application entry point
│   ├── models.py                   # Database models schema
│   │
│   ├── models/                     # Trained AI/ML models
│   │   ├── *.pkl                   # Serialized ML models
│   │   └── *.pt                    # PyTorch models
│   │
│   ├── routes/                     # API route definitions
│   ├── controllers/                # Business logic layer
│   │   ├── candidate_controller.py
│   │   ├── candidate_priority.py
│   │   ├── job_controller.py
│   │   ├── neural.py
│   │   ├── priority_candidate.py
│   │   ├── resume_controller.py
│   │   ├── salary_predict.py
│   │   └── salary_prediction_model.pkl
│   │
│   ├── helper/                     # Utility/helper functions
│   │
│   └── data/                       # Training datasets
│       └── deepLearning/
│           └── resume_screen.csv   # Resume screening dataset
│
└── README.md                       # Project documentation
```

## Features in Detail

### Chat Interface

- Real-time message exchange
- Typing indicators
- Message timestamps
- Auto-scroll to latest messages
- Keyboard shortcuts (Enter to send)

### AI Integration

- Google Gemini AI for intelligent responses
- Error handling with fallback messages
- Contextual HR-focused responses
-
- ### ML models
- Ml prdedict salary (Linear Regrition algho)
- ML predect the condadt job fit (Logistique Rogristion)
- ML predect priority of client (Random Forest Classifier)
- ML Resume Screening Model ( Deep Learning (Neural Network) with TF-IDF)

### UI/UX

- Modern glassmorphism design
- Responsive layout
- Dark theme with gradient accents
- Mobile-friendly interface

## Troubleshooting

### Common Issues

1. **CORS Errors**: Make sure the Flask server is running and CORS is enabled
2. **API Connection**: Check that the backend is running on port 5000
3. **Environment Variables**: Ensure your `.env` file is properly configured
4. **Dependencies**: Make sure all packages are installed correctly

### Getting Help

If you encounter any issues:

1. Check the console for error messages
2. Verify that both servers are running
3. Ensure all environment variables are set correctly
4. Check the network tab for API call failures

## License

This project is open source and available under the MIT License.
