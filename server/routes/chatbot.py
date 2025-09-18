from flask import Blueprint, request, jsonify
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controllers.candidate_controller import CandidateController
from controllers.job_controller import JobController
from controllers.resume_controller import ResumeController

# Create blueprints
candidate_bp = Blueprint('candidates', __name__, url_prefix='/api/candidates')
job_bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')
resume_bp = Blueprint('resumes', __name__, url_prefix='/api/resumes')

# Initialize controllers
candidate_controller = CandidateController()
job_controller = JobController()
resume_controller = ResumeController()

# ==================== CANDIDATE ROUTES ====================

@candidate_bp.route('/', methods=['GET'])
def get_all_candidates():
    """Get all candidates"""
    result = candidate_controller.get_all_candidates()
    return jsonify(result), 200 if result['success'] else 400

@candidate_bp.route('/priority/<priority>', methods=['GET'])
def get_candidates_by_priority(priority):
    """Get candidates by priority level"""
    result = candidate_controller.get_candidates_by_priority(priority)
    return jsonify(result), 200 if result['success'] else 400

@candidate_bp.route('/experience/<exp_band>', methods=['GET'])
def get_candidates_by_experience(exp_band):
    """Get candidates by experience band"""
    result = candidate_controller.get_candidates_by_experience(exp_band)
    return jsonify(result), 200 if result['success'] else 400

@candidate_bp.route('/stats', methods=['GET'])
def get_candidate_stats():
    """Get candidate statistics"""
    result = candidate_controller.get_candidate_stats()
    return jsonify(result), 200 if result['success'] else 400

@candidate_bp.route('/search', methods=['POST'])
def search_candidates():
    """Search candidates with filters"""
    filters = request.get_json() or {}
    result = candidate_controller.search_candidates(filters)
    return jsonify(result), 200 if result['success'] else 400

@candidate_bp.route('/<candidate_id>/job-fits', methods=['GET'])
def get_candidate_job_fits(candidate_id):
    """Get job fits for a specific candidate"""
    result = candidate_controller.get_candidate_job_fits(candidate_id)
    return jsonify(result), 200 if result['success'] else 400

@candidate_bp.route('/<candidate_id>/resume-screen', methods=['GET'])
def get_candidate_resume_screen(candidate_id):
    """Get resume screening data for a specific candidate"""
    result = candidate_controller.get_candidate_resume_screen(candidate_id)
    return jsonify(result), 200 if result['success'] else 400

# ==================== JOB ROUTES ====================

@job_bp.route('/', methods=['GET'])
def get_all_jobs():
    """Get all jobs"""
    result = job_controller.get_all_jobs()
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/degree/<degree>', methods=['GET'])
def get_jobs_by_degree(degree):
    """Get jobs by required degree"""
    result = job_controller.get_jobs_by_degree(degree)
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/experience', methods=['GET'])
def get_jobs_by_experience():
    """Get jobs by experience range"""
    min_years = request.args.get('min_years', type=float)
    max_years = request.args.get('max_years', type=float)
    
    if min_years is None:
        return jsonify({'success': False, 'message': 'min_years parameter is required'}), 400
    
    result = job_controller.get_jobs_by_experience(min_years, max_years)
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/skills', methods=['POST'])
def get_jobs_by_skills():
    """Get jobs by required skills"""
    data = request.get_json()
    if not data or 'skills' not in data:
        return jsonify({'success': False, 'message': 'skills array is required'}), 400
    
    result = job_controller.get_jobs_by_skills(data['skills'])
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/families', methods=['GET'])
def get_job_families():
    """Get all job families"""
    result = job_controller.get_job_families()
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/family/<job_family>', methods=['GET'])
def get_jobs_by_family(job_family):
    """Get jobs by job family"""
    result = job_controller.get_jobs_by_family(job_family)
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/seniority/<seniority>', methods=['GET'])
def get_jobs_by_seniority(seniority):
    """Get jobs by seniority level"""
    result = job_controller.get_jobs_by_seniority(seniority)
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/stats', methods=['GET'])
def get_job_stats():
    """Get job statistics"""
    result = job_controller.get_job_stats()
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/search', methods=['POST'])
def search_jobs():
    """Search jobs with filters"""
    filters = request.get_json() or {}
    result = job_controller.search_jobs(filters)
    return jsonify(result), 200 if result['success'] else 400

@job_bp.route('/skill-analysis', methods=['GET'])
def get_skill_analysis():
    """Get skill analysis for jobs"""
    result = job_controller.get_skill_analysis()
    return jsonify(result), 200 if result['success'] else 400

# ==================== RESUME ROUTES ====================

@resume_bp.route('/', methods=['GET'])
def get_all_resumes():
    """Get all resume screening data"""
    result = resume_controller.get_all_resumes()
    return jsonify(result), 200 if result['success'] else 400

@resume_bp.route('/job-family/<job_family>', methods=['GET'])
def get_resumes_by_job_family(job_family):
    """Get resumes by job family"""
    result = resume_controller.get_resumes_by_job_family(job_family)
    return jsonify(result), 200 if result['success'] else 400

@resume_bp.route('/seniority/<seniority>', methods=['GET'])
def get_resumes_by_seniority(seniority):
    """Get resumes by seniority level"""
    result = resume_controller.get_resumes_by_seniority(seniority)
    return jsonify(result), 200 if result['success'] else 400

@resume_bp.route('/advanced', methods=['GET'])
def get_advanced_resumes():
    """Get resumes that advanced to next stage"""
    result = resume_controller.get_advanced_resumes()
    return jsonify(result), 200 if result['success'] else 400

@resume_bp.route('/stats', methods=['GET'])
def get_resume_stats():
    """Get resume statistics"""
    result = resume_controller.get_resume_stats()
    return jsonify(result), 200 if result['success'] else 400

@resume_bp.route('/search', methods=['POST'])
def search_resumes():
    """Search resumes with filters"""
    filters = request.get_json() or {}
    result = resume_controller.search_resumes(filters)
    return jsonify(result), 200 if result['success'] else 400

@resume_bp.route('/skill-extraction', methods=['GET'])
def get_skill_extraction():
    """Get skill extraction analysis"""
    result = resume_controller.get_skill_extraction()
    return jsonify(result), 200 if result['success'] else 400

@resume_bp.route('/job-family-analysis', methods=['GET'])
def get_job_family_analysis():
    """Get job family analysis"""
    result = resume_controller.get_job_family_analysis()
    return jsonify(result), 200 if result['success'] else 400

# ==================== COMBINED ROUTES ====================

@candidate_bp.route('/overview', methods=['GET'])
def get_candidate_overview():
    """Get comprehensive candidate overview"""
    try:
        stats = candidate_controller.get_candidate_stats()
        all_candidates = candidate_controller.get_all_candidates()
        
        return jsonify({
            'success': True,
            'data': {
                'statistics': stats['data'] if stats['success'] else {},
                'recent_candidates': all_candidates['data'][:10] if all_candidates['success'] else [],
                'total_count': all_candidates['count'] if all_candidates['success'] else 0
            },
            'message': 'Candidate overview retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve candidate overview'
        }), 400

@job_bp.route('/overview', methods=['GET'])
def get_job_overview():
    """Get comprehensive job overview"""
    try:
        stats = job_controller.get_job_stats()
        families = job_controller.get_job_families()
        skill_analysis = job_controller.get_skill_analysis()
        
        return jsonify({
            'success': True,
            'data': {
                'statistics': stats['data'] if stats['success'] else {},
                'job_families': families['data'] if families['success'] else [],
                'skill_analysis': skill_analysis['data'] if skill_analysis['success'] else {}
            },
            'message': 'Job overview retrieved successfully'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to retrieve job overview'
        }), 400
