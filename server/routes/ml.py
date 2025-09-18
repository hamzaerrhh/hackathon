from flask import Blueprint, request, jsonify
from controllers.salary_predet import predict
import pickle
import pandas as pd
from controllers.salary_predet import predict
from controllers.priorityçcondidat  import  predict_priority
from controllers.neural import predict_advance

# Create a blueprint

ml_bp = Blueprint("ml", __name__)
PredectPath="C:/Users/DELL/Desktop/hackathon/Dataset-genAI/server/models/salary_prediction_model.pkl"

# Path to the random forest model
RANDOM_FOREST_PATH = "C:/Users/DELL/Desktop/hackathon/Dataset-genAI/server/models/random_forest.pkl"


@ml_bp.route("/salary/predict", methods=["POST"])
def predict_salary():
    """Predict salary based on candidate/job features."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        print("Received data:", data)
        
        # Validate required fields
        required_fields = ['role', 'years_experience', 'degree', 'company_size', 'location', 'level']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Convert years_experience to float
        try:
            data['years_experience'] = float(data['years_experience'])
        except ValueError:
            return jsonify({"error": "years_experience must be a number"}), 400
        
        print("Starting prediction with data:", data)
        
        # Make prediction
        prediction = predict(PredectPath, data)
        
        # Format the prediction result
        if isinstance(prediction, (int, float)):
            return jsonify({"salary": f"${prediction:,.2f}"})
        return jsonify({"salary": str(prediction)})

    except Exception as exc:
        return jsonify({"error": f"Prediction error: {str(exc)}"}), 500


@ml_bp.route("/job_fit/predict", methods=["POST"])
def predict_job_fit():
    """Check if a candidate fits a job (dummy example)."""
    try:
        data = request.get_json()
        if not data or "candidate_id" not in data or "job_id" not in data:
            return jsonify({"error": "candidate_id and job_id required"}), 400

        # Dummy logic: fit score = length of candidate_id + job_id
        fit_score = len(data["candidate_id"]) + len(data["job_id"])

        return jsonify({"fit_score": fit_score})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500





@ml_bp.route("/candidate_priority/predict", methods=["POST"])
def candidate_priority():
    """Predict candidate priority using the random forest model."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        # Make prediction
        result = predict_priority(RANDOM_FOREST_PATH, data)
        
        # If there was an error, return it
        if "error" in result:
            return jsonify({"error": result["error"]}), 500
        
        return jsonify(result)
        
    except Exception as exc:
        return jsonify({"error": f"Priority prediction failed: {str(exc)}"}), 500


@ml_bp.route("/resume_screen/predict", methods=["POST"])
def resume_screen():
    """
    Screen a candidate's resume against a job description and return an
    "advance" probability score.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Validate that all required fields are in the request
        required_fields = ['resume_text', 'jd_text', 'job_family', 'seniority']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Call the main prediction function
        probability = predict_advance(
            resume_text=data['resume_text'],
            jd_text=data['jd_text'],
            job_family=data['job_family'],
            seniority=data['seniority']
        )

        return jsonify({"advance_probability": probability})

    except Exception as exc:
        print(f"ERROR in /resume_screen/predict: {str(exc)}") # Log the error for debugging
        return jsonify({"error": "An internal server error occurred during prediction."}), 400