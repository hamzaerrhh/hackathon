from flask import Flask, jsonify,request
from flask_cors import CORS
from pymongo import MongoClient
import os
from routes.ml import ml_bp


from dotenv import load_dotenv
import google.generativeai as genai
from helper.tool import (
   check_job_fit, predict_salary,get_candidate,get_job,
    screen_resume, get_priority, list_candidates, list_jobs
)
from controllers.candidate_controller import register_candidate_routes
import controllers.job_controller as job_controller




#!gemini config tool
# Define the list of tools for Gemini
genai.configure(api_key=os.getenv("gemini_ai_key"))



# !gemini config tool
# Define the list of tools for Gemini
tools = genai.protos.Tool(
    function_declarations=[
        genai.protos.FunctionDeclaration(
            name="get_candidate",
            description="Get candidate information by their ID.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "candidate_id": genai.protos.Schema(type=genai.protos.Type.STRING)
                },
                required=["candidate_id"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="get_job",
            description="Get job information by its ID.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "job_id": genai.protos.Schema(type=genai.protos.Type.STRING)
                },
                required=["job_id"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="list_candidates",
            description="Show a list of all available candidates.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={}
            )
        ),
        genai.protos.FunctionDeclaration(
            name="predict_salary",
            description="Predicts the salary for a given data.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "role": genai.protos.Schema(type=genai.protos.Type.STRING),
                    "years_experience": genai.protos.Schema(type=genai.protos.Type.NUMBER)
                },
                required=["role", "years_experience"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="check_job_fit",
            description="Checks a candidate's fit for a job based on their IDs.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "candidate_id": genai.protos.Schema(type=genai.protos.Type.STRING),
                    "job_id": genai.protos.Schema(type=genai.protos.Type.STRING)
                },
                required=["candidate_id", "job_id"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="screen_resume",
            description="Performs an automated resume screening for a candidate by ID.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "candidate_id": genai.protos.Schema(type=genai.protos.Type.STRING)
                },
                required=["candidate_id"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="get_priority",
            description="Retrieves the priority level for a candidate by ID.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={
                    "candidate_id": genai.protos.Schema(type=genai.protos.Type.STRING)
                },
                required=["candidate_id"]
            )
        ),
        genai.protos.FunctionDeclaration(
            name="list_jobs",
            description="Show a list of all available jobs.",
            parameters=genai.protos.Schema(
                type=genai.protos.Type.OBJECT,
                properties={}
            )
        )
    ]
)

load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# MongoDB Atlas connection setup
def get_mongodb_connection():
    try:
        # Get credentials from environment variables
        username = os.environ.get('user_pass')
        password = os.environ.get('pass_key')
        
        # Construct MongoDB Atlas connection URI
        mongodb_uri = f"mongodb+srv://{username}:{password}@cluster0.ggtqgzr.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        database_name = "flask_shop"  # You can change this to your preferred database name
        
        # Connect to MongoDB Atlas
        client = MongoClient(mongodb_uri)
        db = client[database_name]
        
        # Test the connection
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB Atlas!")
        print(f"📊 Database: {database_name}")
        return db
        
    except Exception as e:
        print(f"❌ Error connecting to MongoDB Atlas: {e}")
        return None



# Initialize MongoDB connection
db = get_mongodb_connection()
# mongo = PyMongo(app)


#chat route

@app.route('/api/chat', methods=['POST'])
def handle_chat_request():
    data = request.get_json()
    user_prompt = data.get("prompt")
    if not user_prompt:
        return jsonify({"error": "No prompt provided"}), 400

    model = genai.GenerativeModel('gemini-1.5-flash', tools=[tools])
    chat = model.start_chat()

    try:
        # First turn: Send the user prompt to the model
        response = chat.send_message(user_prompt)

        # Check if the model has a function call
        if response.candidates[0].content.parts[0].function_call:
            function_call = response.candidates[0].content.parts[0].function_call
            function_name = function_call.name
            function_args = {key: value for key, value in function_call.args.items()}

            # Execute the correct Python function based on the name from the model
            tool_functions = {
                "get_candidate": get_candidate,
                "get_job": get_job,
                "check_job_fit": check_job_fit,
                "predict_salary": predict_salary,
                "screen_resume": screen_resume,
                "get_priority": get_priority,
                "list_candidates": list_candidates,
                "list_jobs": list_jobs
            }
            
            if function_name in tool_functions:
                result = tool_functions[function_name](**function_args)
            else:
                return jsonify({"error": "Unknown tool"}), 500

            # Second turn: Send the function's result back to the model
            final_response = chat.send_message(
                genai.protos.Content(
                    role='function',
                    parts=[genai.protos.Part(
                        function_response=genai.protos.FunctionResponse(
                            name=function_name,
                            response=json.loads(result) if isinstance(result, str) else {"result": result}
                        )
                    )]
                )
            )
            return jsonify({"response": final_response.text+ "this is the response from the tool"})

        # If no tool is selected, return the direct model response
        return jsonify({"response": response.text})

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500

# Health check for chat API
@app.route('/api/health', methods=['GET'])
def chat_health():
    """Health check endpoint for the chat API"""
    return jsonify({
        "status": "healthy",
        "service": "chat-api",
        "message": "Chat API is running"
    })

#call route


register_candidate_routes(app, db)
job_controller.register_job_routes(app, db)



#ml route
app.register_blueprint(ml_bp, url_prefix="/api")


# Home route
@app.route('/')
def home():
    if db is not None:  # FIXED: Compare with None instead of using if db:
        # Test connection again to make sure it's still alive
        try:
            db.command('ping')
            return jsonify({
                "message": "Welcome to the Flask backend with MongoDB Atlas!",
                "database": "connected",
                "status": "healthy",
                "connection_type": "MongoDB Atlas",
                "cluster": "Cluster0"
            })
        except Exception as e:
            return jsonify({
                "message": "Welcome to the Flask backend!",
                "database": "disconnected",
                "status": "unhealthy",
                "error": str(e)
            })
    else:
        return jsonify({
            "message": "Welcome to the Flask backend!",
            "database": "disconnected",
            "status": "unhealthy",
            "connection_type": "MongoDB Atlas"
        })

if __name__ == '__main__':
    # Get port from environment variable (for cloud deployment)
    port = int(os.environ.get('PORT', 5000))
    
    # Print connection status on startup
    if db is not None:
        print("🚀 Server starting with MongoDB Atlas connection")
        print("🌐 Cluster: Cluster0")
        print("🔗 Connection URI: mongodb+srv://cluster0.ggtqgzr.mongodb.net/")
    else:
        print("⚠️  Server starting without MongoDB connection")
    
    # Run the app
    print(f"🌐 Server running on port {port}")
    app.run(debug=True, host='0.0.0.0', port=port)