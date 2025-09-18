import requests
from bson.json_util import dumps
from models import Candidate, Job

# Fetch a single candidate
def get_candidate(candidate_id: str):

    try:
        candidate = Candidate.objects(candidate_id=candidate_id).first()
        if not candidate:
            return None
        
        candidate_data = candidate.to_mongo()
        # Call external API
        try:
            api_response = requests.get(f"http://localhost:5000/api/candidate/{candidate_id}")
            if api_response.status_code == 200:
                candidate_data["external_info"] = api_response.json()
        except Exception as api_err:
            candidate_data["external_info_error"] = str(api_err)

        return dumps(candidate_data)

    except Exception as e:
        return {"error": f"Failed to retrieve candidate: {str(e)}"}


# Fetch a single job
def get_job(job_id: str):
    try:
        job = Job.objects(id=job_id).first()
        if not job:
            return None
        
        job_data = job.to_mongo()

        # Call external API
        try:
            api_response = requests.get(f"http://localhost:5000/api/jobs/{job_id}")
            if api_response.status_code == 200:
                job_data["external_info"] = api_response.json()
        except Exception as api_err:
            job_data["external_info_error"] = str(api_err)

        return dumps(job_data)

    except Exception as e:
        return {"error": f"Failed to retrieve job: {str(e)}"}


# List all candidates
def list_candidates():
    try:
       

        # Call external API
        try:
            api_response = requests.get("http://localhost:5000/api/candidates")
            if api_response.status_code == 200:
                return api_response.json()
        except Exception as api_err:
            print("API call error:", api_err)

        return dumps(api_response.json())

    except Exception as e:
        return {"error": f"Failed to retrieve candidates: {str(e)}"}


# List all jobs
def list_jobs():
    try:
    
        try:
            api_response = requests.get("http://localhost:5000/api/jobs")
            if api_response.status_code == 200:
               return (api_response.json())
        except Exception as api_err:
            print("API call error:", api_err)

        return dumps(api_response.json())

    except Exception as e:
        return {"error": f"Failed to retrieve jobs: {str(e)}"}


def check_job_fit(candidate_id: str, job_id: str):
    """
    Performs an ML-powered analysis to check a candidate's fit for a job.
    This function would call your job-fit model.
    """
    # This is a placeholder; you'd integrate your actual ML model here.
    # Example: score = my_ml_model.predict_fit(candidate_data, job_data)
    return f"Candidate {candidate_id} is a good fit for job {job_id} with an 85% score."

def predict_salary(role: str, years_experience: float):
    print('now predect salary')
    """
    Predicts the salary for a given role and years of experience.
    """
    # Placeholder for a salary prediction ML model.
    base_salary = 70000
    predicted_salary = base_salary + (years_experience * 5000)
    return f"${predicted_salary:,.2f}"

def screen_resume(candidate_id: str):
    """
    Performs an automated resume screening for a candidate.
    """
    # Placeholder for a resume screening model.
    return f"Resume for candidate {candidate_id} has been screened and recommended for the next round."

def get_priority(candidate_id: str):
    """
    Retrieves the priority level for a candidate based on internal scoring.
    """
    # Placeholder for a candidate priority function.
    priority = "High" if candidate_id == "CAND001" else "Medium"
    return f"Candidate {candidate_id} has a {priority} priority."
