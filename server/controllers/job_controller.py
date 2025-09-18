# controllers.py
from flask import jsonify, request
from bson.json_util import dumps # For 

# This function registers all API routes for the jobs collection
def register_job_routes(app, db):
    """
    Registers all API routes for the jobs collection.
    
    Args:
        app: The Flask application instance.
        db: The MongoDB database connection.
    """
    jobs_collection = db.jobs

    # GET: List all jobs
    @app.route('/api/jobs', methods=['GET'])
    def list_jobs():
        print('hi get jobs')
        jobs =list(jobs_collection.find())
        print('jobs',jobs)
        return dumps(jobs)

    # GET: Retrieve a single job by job_id
    @app.route('/api/job/<job_id>', methods=['GET'])
    def get_job(job_id):
        job = jobs_collection.find_one({"job_id": job_id})
        if job:
            return dumps(job)
        return jsonify({"error": "Job not found"}), 404

    # POST: Create a new job
    @app.route('/api/jobs', methods=['POST'])
    def add_job():
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        try:
            # Insert the JSON data directly into the collection
            result = jobs_collection.insert_one(data)
            
            # Return a success message with the ID of the new document
            if result.inserted_id:
                return jsonify({
                    "message": "Job created", 
                    "job_id": data.get("job_id"),
                    "inserted_id": str(result.inserted_id)
                }), 201
            
            return jsonify({"error": "Failed to create job"}), 500
        except Exception as e:
            # Handle potential duplicate key errors (if job_id is unique)
            return jsonify({"error": str(e)}), 400

    # PUT: Update an existing job
    @app.route('/api/job/<job_id>', methods=['PUT'])
    def update_job(job_id):
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        result = jobs_collection.update_one(
            {"job_id": job_id},
            {"$set": data}
        )

        if result.matched_count == 0:
            return jsonify({"error": "Job not found"}), 404
        
        return jsonify({"message": "Job updated"})

    # DELETE: Delete a job
    @app.route('/api/job/<job_id>', methods=['DELETE'])
    def delete_job(job_id):
        result = jobs_collection.delete_one({"job_id": job_id})
        
        if result.deleted_count == 0:
            return jsonify({"error": "Job not found"}), 404
        
        return jsonify({"message": "Job deleted"})