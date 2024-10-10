import concurrent.futures
import os
import json
import app.data_ingestor as dt

class ThreadPool:
    def __init__(self):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        # use threadpooexecutor
        workers = os.getenv('TP_NUM_OF_THREADS', os.cpu_count())
        self.pool = concurrent.futures.ThreadPoolExecutor(workers)
        

    # task = fucntia care calculeaz ccerinta pentru fiecare api
    def submit_task(self, task):
        # Submit a task to the ThreadPool
        # This function should return immediately
        # and not wait for the task to complete
        future = self.pool.submit(task)

    def stop (self):
        # This function should stop all the threads in the pool
        self.pool.shutdown(wait=True)

    def result_states_mean_request(self, question, job_id):               
        data = dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").rows
        states = {}
        for row in data:
            if row["Question"] == question:
                if row["LocationDesc"] not in states:
                    states[row["LocationDesc"]] = []
                states[row["LocationDesc"]].append(row["Data_Value"])
            else:
                continue

        for state in states:
            states[state] = sum(states[state]) / len(states[state])
        
        states = dict(sorted(states.items(), key=lambda item: item[1]))
        path = os.path.abspath("results")
        with open(f"{path}/{job_id}.json", 'a') as f:
            f.write(json.dumps(states))

    def result_state_mean_request(self, question, job_id, state):
        data = dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").rows
        states = {}
        for row in data:
            if row["Question"] == question and row["LocationDesc"] == state:
                if row["LocationDesc"] not in states:
                    states[row["LocationDesc"]] = []
                states[row["LocationDesc"]].append(row["Data_Value"])
            else:
                continue

        for state in states:
            states[state] = sum(states[state]) / len(states[state])
        
        states = dict(sorted(states.items(), key=lambda item: item[1]))
        path = os.path.abspath("results")
        with open(f"{path}/{job_id}.json", 'a') as f:
            f.write(json.dumps(states))

    def result_best5_request(self, question, job_id):
        data = dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").rows
        states = {}
        for row in data:
            if row["Question"] == question:
                if row["LocationDesc"] not in states:
                    states[row["LocationDesc"]] = []
                states[row["LocationDesc"]].append(row["Data_Value"])
            else:
                continue

        for state in states:
            states[state] = sum(states[state]) / len(states[state])

        if question in dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").questions_best_is_min:
            states = dict(sorted(states.items(), key=lambda item: item[1]))
        elif question in dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").questions_best_is_max:
            states = dict(sorted(states.items(), key=lambda item: item[1], reverse=True))

        path = os.path.abspath("results")

        n = 5
        first_n_elem = dict(list(states.items())[:n])
        with open(f"{path}/{job_id}.json", 'a') as f:
            f.write(json.dumps(first_n_elem))

    def result_worst5_request(self, question, job_id):
        data = dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").rows
        states = {}
        for row in data:
            if row["Question"] == question:
                if row["LocationDesc"] not in states:
                    states[row["LocationDesc"]] = []
                states[row["LocationDesc"]].append(row["Data_Value"])
            else:
                continue

        for state in states:
            states[state] = sum(states[state]) / len(states[state])

        if question in dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").questions_best_is_min:
            states = dict(sorted(states.items(), key=lambda item: item[1], reverse=True))
        elif question in dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").questions_best_is_max:
            states = dict(sorted(states.items(), key=lambda item: item[1]))

        path = os.path.abspath("results")

        n = 5
        first_n_elem = dict(list(states.items())[:n])
        with open(f"{path}/{job_id}.json", 'a') as f:
            f.write(json.dumps(first_n_elem))

    def result_global_mean_request(self, question, job_id):
        data = dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").rows
        states = {}
        for row in data:
            if row["Question"] == question:
                if row["LocationDesc"] not in states:
                    states[row["LocationDesc"]] = []
                states[row["LocationDesc"]].append(float(row["Data_Value"]))
            else:
                continue

        res = 0.0
        count = 0
        for i in states:
            for j in range(len(states[i])):
                res += states[i][j]
                count += 1

        path = os.path.abspath("results")
        with open(f"{path}/{job_id}.json", 'a') as f:
            f.write(json.dumps({"global_mean": res/count}))
        
    def result_diff_from_mean_request(self, question, job_id):
        states = {}
        data = dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").rows
        
        for row in data:
            if row["Question"] == question:
                if row["LocationDesc"] not in states:
                    states[row["LocationDesc"]] = []
                states[row["LocationDesc"]].append(row["Data_Value"])
            else:
                continue

        res = 0.0
        count = 0
        for i in states:
            for j in range(len(states[i])):
                res += states[i][j]
                count += 1

        global_mean = res/count

        for state in states:
            states[state] = sum(states[state]) / len(states[state])

        new_states = {}
        for state in states:
            new_states[state] = global_mean - states[state]
         
           

        final_states = dict(sorted(new_states.items(), key=lambda item: item[1]))

        path = os.path.abspath("results")
        with open(f"{path}/{job_id}.json", 'a') as f:
            f.write(json.dumps(final_states))
        
    def result_state_diff_from_mean_request(self, question, job_id, stat):
        states = {}
        data = dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").rows

        for row in data:
            if row["Question"] == question:
                if row["LocationDesc"] not in states:
                    states[row["LocationDesc"]] = []
                states[row["LocationDesc"]].append(row["Data_Value"])
            else:
                continue

        res = 0.0
        count = 0
        for i in states:
            for j in range(len(states[i])):
                res += states[i][j]
                count += 1

        global_mean = res/count

        state_mean = sum(states[stat]) / len(states[stat])
        path = os.path.abspath("results")
        with open(f"{path}/{job_id}.json", 'a') as f:
            f.write(json.dumps({stat: global_mean - state_mean}))

    def result_mean_by_category_request(self, question, job_id):
        data = dt.DataIngestor("./nutrition_activity_obesity_usa_subset.csv").rows
        pass

    def result_state_mean_by_category_request(self, question, job_id, state):
        pass
