# RH Agent - AI Chat Application

A modern AI-powered chat application for HR (Human Resources) assistance, built with React and Flask.

## Features

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
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── pages/         # Page components
│   │   └── index.css      # Global styles
│   └── package.json
├── server/                 # Flask backend
│   ├── main.py            # Main server file
│   ├── requirements.txt   # Python dependencies
│   └── setup.py          # Setup script
└── README.md
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

### UI/UX
- Modern glassmorphism design
- Smooth animations and transitions
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