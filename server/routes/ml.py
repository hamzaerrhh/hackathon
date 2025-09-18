from flask import Blueprint, request, jsonify
from controllers.salary_predet import predict

# Create a blueprint
ml_bp = Blueprint("ml", __name__)
PredectPath="../models/salary_prediction_model.pk1"



@ml_bp.route("/salary/predict", methods=["POST"])
def predict_salary():
    """Predict salary based on candidate/job features."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
        
        print("start predect")

        prediction = predict(PredectPath,data)

        if isinstance(prediction, (int, float)):
            return jsonify({"salary": f"${prediction:,.2f}"})
        return jsonify({"salary": str(prediction)})

    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


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


@ml_bp.route("/resume_screen/predict", methods=["POST"])
def resume_screen():
    """Screen candidate resume (dummy example)."""
    try:
        data = request.get_json()
        if not data or "candidate_id" not in data:
            return jsonify({"error": "candidate_id required"}), 400

        # Dummy response
        result = f"Candidate {data['candidate_id']} resume looks strong."

        return jsonify({"screening_result": result})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@ml_bp.route("/candidate_priority/predict", methods=["POST"])
def candidate_priority():
    """Get candidate priority (dummy example)."""
    try:
        data = request.get_json()
        if not data or "candidate_id" not in data:
            return jsonify({"error": "candidate_id required"}), 400

        # Dummy logic: even IDs = High priority, odd IDs = Medium
        candidate_id = data["candidate_id"]
        priority = "High" if len(candidate_id) % 2 == 0 else "Medium"

        return jsonify({"priority": priority})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500
