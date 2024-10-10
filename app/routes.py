import os
import json
from app import webserver
from flask import request, jsonify


"""Example of a POST endpoint"""
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        print(f"got data in post {data}")

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405


"""Return the results of the job with the given job_id"""
@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    path = os.path.abspath("results")

    if int(job_id) < 1 or int(job_id) > webserver.job_counter:
        webserver.logger.info(f"Got request for job_id {job_id}")
        return jsonify({"error": "Invalid {job_id}"})
    
    if not os.path.exists(f"{path}/{job_id}.json"):
        webserver.logger.info(f"Got request for job_id {job_id}")
        return jsonify({"status": "running"})
    
    with open(f"{path}/{job_id}.json", 'r') as f:
        webserver.logger.info(f"Got request for job_id {job_id}")
        return jsonify({"status": "done", "data": json.loads(f.read())})

"""Gracefully shutdown the webserver"""
@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    # Shutdown the webserver
    webserver.tasks_runner.stop()
    webserver.logger.info(f"Got request for graceful_shutdown")
    return jsonify({"status": "ok"})

"""Return the status of the jobs"""
@webserver.route('/api/jobs', methods=['GET'])
def jobs():
    res = {"status": "done"}
    list_status_jobs = []
    for i in range(1, webserver.job_counter):
        path = os.path.abspath("results")
        if not os.path.exists(f"{path}/{i}.json"):
            list_status_jobs.append({"job_id_{i}": "running"})
        else:
            list_status_jobs.append({"job_id_{i}": "done"})

    res["data"] = list_status_jobs
    webserver.logger.info(f"Got request for jobs")
    return jsonify(res)

"""Return the number of jobs"""
@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    webserver.logger.info(f"Got request for num_jobs")
    return webserver.tasks_runner.pool._adjust_thread_count()

"""Return mean value of all states"""
@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_states_mean_request(data["question"], job_id))
    webserver.job_counter += 1

    webserver.logger.info(f"Got request states_mean{job_id}")
    return jsonify({"job_id": job_id})

"""Return the mean value for a state"""
@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    data = request.json
    print(f"Got request {data}")

    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_state_mean_request(data["question"], job_id, data["state"]))
    webserver.job_counter += 1
    webserver.logger.info(f"Got request for state_mean")
    return jsonify({"job_id": job_id})

"""Return the best 5 states"""
@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    data = request.json
    
    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_best5_request(data["question"], job_id))
    webserver.job_counter += 1
    webserver.logger.info(f"Got request for best5, {job_id}")
    return jsonify({"job_id": job_id})

"""Return the worst 5 states"""
@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_worst5_request(data["question"], job_id))
    webserver.job_counter += 1
    webserver.logger.info(f"Got request for worst5, {job_id}")
    return jsonify({"job_id": job_id})

"""Return the global mean"""
@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_global_mean_request(data["question"], job_id))
    webserver.job_counter += 1
    webserver.logger.info(f"Got request for global_mean, {job_id}")
    return jsonify({"job_id": job_id})

"""Return the difference from the mean"""
@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    data = request.json
    
    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_diff_from_mean_request(data["question"], job_id))
    webserver.job_counter += 1
    webserver.logger.info(f"Got request for diff_from_mean, {job_id}")
    return jsonify({"job_id": job_id})

"""Return the difference from the mean for a state"""
@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    data = request.json
    
    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_state_diff_from_mean_request(data["question"], job_id, data["state"]))
    webserver.job_counter += 1

    return jsonify({"job_id": job_id})

"""Return the mean value for each category"""
@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_mean_by_category_request(data["question"], job_id))
    webserver.job_counter += 1
    webserver.logger.info(f"Got request for mean_by_category, {job_id}")
    return jsonify({"job_id": job_id})

"""Return the mean valie for each category in a state"""
@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    data = request.json

    job_id = webserver.job_counter
    webserver.tasks_runner.submit_task(webserver.tasks_runner.result_state_mean_by_category_request(data["question"], job_id, data["state"]))
    webserver.job_counter += 1
    webserver.logger.info(f"Got request for state_mean_by_category, {job_id}")
    return jsonify({"status": "NotImplemented"})

"""You can check localhost in your browser to see what this displays"""
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

"""Return the defined routes"""
def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
