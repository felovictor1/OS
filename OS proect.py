# Define a function to implement FCFS scheduling
def fcfs_scheduling(processes):
    """
    Simulates the FCFS CPU scheduling algorithm.

    Parameters:
        processes (list of dict): A list of processes with 'pid', 'arrival_time', and 'burst_time'.

    Returns:
        list of dict: A list of processes with additional fields: 'completion_time', 'turnaround_time', 'waiting_time'.
    """
    # Sort processes by their arrival time
    processes.sort(key=lambda x: x['arrival_time'])

    # Initialize variables
    current_time = 0

    for process in processes:
        # Calculate Completion Time
        if current_time < process['arrival_time']:
            current_time = process['arrival_time']
        current_time += process['burst_time']
        process['completion_time'] = current_time

        # Calculate Turnaround Time
        process['turnaround_time'] = process['completion_time'] - process['arrival_time']

        # Calculate Waiting Time
        process['waiting_time'] = process['turnaround_time'] - process['burst_time']

    return processes


        
def sjf_non_preemptive(processes):
    """
    Simulates the Non-Preemptive Shortest Job First CPU scheduling algorithm.

    Parameters:
        processes (list of dict): List of processes with 'pid', 'arrival_time', and 'burst_time'.

    Returns:
        list of dict: Processes with 'completion_time', 'turnaround_time', 'waiting_time'.
    """
    processes.sort(key=lambda x: (x['arrival_time'], x['burst_time']))
    current_time = 0

    scheduled = []
    while processes:
        available = [p for p in processes if p['arrival_time'] <= current_time]
        if available:
            shortest = min(available, key=lambda x: x['burst_time'])
            processes.remove(shortest)
            current_time = max(current_time, shortest['arrival_time']) + shortest['burst_time']
            shortest['completion_time'] = current_time
            shortest['turnaround_time'] = shortest['completion_time'] - shortest['arrival_time']
            shortest['waiting_time'] = shortest['turnaround_time'] - shortest['burst_time']
            scheduled.append(shortest)
        else:
            current_time += 1

    return scheduled
def sjf_preemptive(processes):
    time = 0
    completed = 0
    n = len(processes)
    ready_queue = []

    # Initialize all processes
    for process in processes:
        process['remaining_time'] = process['burst_time']
        process['response_time'] = None  # Response time

    while completed < n:
        # Add processes to the ready queue based on arrival time
        ready_queue = [
            p for p in processes if p['arrival_time'] <= time and p['remaining_time'] > 0
        ]
        if not ready_queue:
            time += 1
            continue

        # Select the process with the shortest remaining time
        ready_queue.sort(key=lambda p: p['remaining_time'])
        current_process = ready_queue[0]

        # If the process is being executed for the first time, record response time
        if current_process['response_time'] is None:
            current_process['response_time'] = time - current_process['arrival_time']

        # Execute the process for 1 unit of time
        current_process['remaining_time'] -= 1
        time += 1

        # If the process is completed
        if current_process['remaining_time'] == 0:
            current_process['completion_time'] = time
            current_process['turnaround_time'] = time - current_process['arrival_time']
            current_process['waiting_time'] = current_process['turnaround_time'] - current_process['burst_time']
            completed += 1

    # Calculate averages
    total_waiting_time = sum(p['waiting_time'] for p in processes)
    total_turnaround_time = sum(p['turnaround_time'] for p in processes)
    total_response_time = sum(p['response_time'] for p in processes)

    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    avg_response_time = total_response_time / n

    return processes, avg_waiting_time, avg_turnaround_time, avg_response_time


def round_robin(processes, time_quantum):
    # Create a queue to manage processes
    queue = []
    time = 0

    # Initialize remaining_time and response_time for all processes
    for process in processes:
        process['remaining_time'] = process['burst_time']
        process['response_time'] = None  # Initialize response time

    completed_processes = []

    while processes or queue:
        # Add processes to the queue that have arrived by the current time
        while processes and processes[0]['arrival_time'] <= time:
            queue.append(processes.pop(0))
        
        if queue:
            process = queue.pop(0)
            
            # Set response time if this is the first time the process is running
            if process['response_time'] is None:
                process['response_time'] = time - process['arrival_time']
            
            # Run the process for the time quantum or until it finishes
            exec_time = min(time_quantum, process['remaining_time'])
            process['remaining_time'] -= exec_time
            time += exec_time
            
            # If the process is completed
            if process['remaining_time'] == 0:
                process['completion_time'] = time
                process['turnaround_time'] = process['completion_time'] - process['arrival_time']
                process['waiting_time'] = process['turnaround_time'] - process['burst_time']
                completed_processes.append(process)
            else:
                # Re-add the process to the queue if it has remaining time
                queue.append(process)
        else:
            # If no process is available, increment time
            time += 1

    return completed_processes

def priority_scheduling(processes, preemptive=False):
    current_time = 0
    completed_processes = []
    
    # Ensure all processes have the necessary keys
    for process in processes:
        if 'completion_time' not in process:
            process['completion_time'] = None

    while len(completed_processes) < len(processes):
        # Filter available processes
        available = [
            p for p in processes
            if p['arrival_time'] <= current_time and p['completion_time'] is None
        ]

        if not available:
            current_time += 1
            continue

        # Sort by priority, then arrival time
        available.sort(key=lambda p: (p['priority'], p['arrival_time']))

        if preemptive:
            # Preemptive: Execute for 1 time unit
            selected_process = available[0]
            if 'remaining_time' not in selected_process:
                selected_process['remaining_time'] = selected_process['burst_time']
            
            selected_process['remaining_time'] -= 1
            current_time += 1

            if selected_process['remaining_time'] == 0:
                selected_process['completion_time'] = current_time
                selected_process['turnaround_time'] = current_time - selected_process['arrival_time']
                selected_process['waiting_time'] = selected_process['turnaround_time'] - selected_process['burst_time']
                completed_processes.append(selected_process)
        else:
            # Non-preemptive: Execute until completion
            selected_process = available[0]
            current_time += selected_process['burst_time']
            selected_process['completion_time'] = current_time
            selected_process['turnaround_time'] = current_time - selected_process['arrival_time']
            selected_process['waiting_time'] = selected_process['turnaround_time'] - selected_process['burst_time']
            completed_processes.append(selected_process)

    return completed_processes

def calculate_averages(processes):
    """
    Calculate and print the average waiting time, turnaround time, and response time.
    
    Parameters:
        processes (list of dict): List of processes with calculated times.
    """
    n = len(processes)
    total_waiting_time = sum(p['waiting_time'] for p in processes)
    total_turnaround_time = sum(p['turnaround_time'] for p in processes)
    total_response_time = sum(p.get('response_time', p['waiting_time']) for p in processes)

    avg_waiting_time = total_waiting_time / n
    avg_turnaround_time = total_turnaround_time / n
    avg_response_time = total_response_time / n

    print(f"Average Waiting Time: {avg_waiting_time:.2f}")
    print(f"Average Turnaround Time: {avg_turnaround_time:.2f}")
    print(f"Average Response Time: {avg_response_time:.2f}")

    return avg_waiting_time, avg_turnaround_time, avg_response_time
if __name__ == "__main__":
    # Define a sample set of processes
    processes_fcfs = [
        {'pid': 'P1', 'arrival_time': 5, 'burst_time': 8},
        {'pid': 'P2', 'arrival_time': 1, 'burst_time': 4},
        {'pid': 'P3', 'arrival_time': 2, 'burst_time': 9},
        {'pid': 'P4', 'arrival_time': 3, 'burst_time': 5},
    ]
    processes_sjf = [
        {'pid': 'P1', 'arrival_time': 0, 'burst_time': 5},
        {'pid': 'P2', 'arrival_time': 1, 'burst_time': 4},
        {'pid': 'P3', 'arrival_time': 2, 'burst_time': 9},
        {'pid': 'P4', 'arrival_time': 3, 'burst_time': 5},
    ]
    processes_rr = [
        {'pid': 'P1', 'arrival_time': 0, 'burst_time': 8},
        {'pid': 'P2', 'arrival_time': 1, 'burst_time': 4},
        {'pid': 'P3', 'arrival_time': 2, 'burst_time': 9},
        {'pid': 'P4', 'arrival_time': 3, 'burst_time': 5},
    ]
    processes_priority = [
        {'pid': 'P1', 'arrival_time': 0, 'burst_time': 8, 'priority': 2},
        {'pid': 'P2', 'arrival_time': 1, 'burst_time': 4, 'priority': 1},
        {'pid': 'P3', 'arrival_time': 2, 'burst_time': 9, 'priority': 3},
        {'pid': 'P4', 'arrival_time': 3, 'burst_time': 5, 'priority': 2},
]


    # Test FCFS
    print("\n--- First Come First Serve (FCFS) ---")
    fcfs_result = fcfs_scheduling(processes_fcfs)
    print("PID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting")
    for p in fcfs_result:
        print(f"{p['pid']}\t{p['arrival_time']}\t{p['burst_time']}\t{p['completion_time']}\t\t{p['turnaround_time']}\t\t{p['waiting_time']}")
    calculate_averages(fcfs_result)

    # Test Non-Preemptive SJF
    print("\n--- Non-Preemptive Shortest Job First (SJF) ---")
    sjf_non_preemptive_result = sjf_non_preemptive(processes_sjf)
    print("PID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting")
    for p in sjf_non_preemptive_result:
        print(f"{p['pid']}\t{p['arrival_time']}\t{p['burst_time']}\t{p['completion_time']}\t\t{p['turnaround_time']}\t\t{p['waiting_time']}")
    calculate_averages(sjf_non_preemptive_result)

    # Test Round Robin
    print("\n--- Round Robin (RR) ---")
    rr_result = round_robin(processes_rr, time_quantum=3)
    print("PID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting")
    for p in rr_result:
        print(f"{p['pid']}\t{p['arrival_time']}\t{p['burst_time']}\t{p['completion_time']}\t\t{p['turnaround_time']}\t\t{p['waiting_time']}")
    calculate_averages(rr_result)

    # Test Priority Scheduling (Non-Preemptive)
    print("\n--- Priority Scheduling (Non-Preemptive) ---")
    priority_result = priority_scheduling(processes_priority, preemptive=False)
    print("PID\tArrival\tBurst\tPriority\tCompletion\tTurnaround\tWaiting")
    for p in priority_result:
        print(f"{p['pid']}\t{p['arrival_time']}\t{p['burst_time']}\t{p['priority']}\t\t{p['completion_time']}\t\t{p['turnaround_time']}\t\t{p['waiting_time']}")
    calculate_averages(priority_result)

    



    sjf_preemptive_processes = [
       {'pid': 'P1', 'arrival_time': 10, 'burst_time': 10},
       {'pid': 'P2', 'arrival_time': 0, 'burst_time': 12},
       {'pid': 'P3', 'arrival_time': 3, 'burst_time': 8},
       {'pid': 'P4', 'arrival_time': 5, 'burst_time': 4},
       {'pid': 'P5', 'arrival_time': 12, 'burst_time': 6},
]


result, avg_waiting_time, avg_turnaround_time, avg_response_time = sjf_preemptive( sjf_preemptive_processes)

# Display results
print("\n--- Preemptive Shortest Job First (SJF) ---")
print("PID\tArrival\tBurst\tCompletion\tTurnaround\tWaiting\tResponse")
for p in result:
    print(f"{p['pid']}\t{p['arrival_time']}\t{p['burst_time']}\t{p['completion_time']}\t\t{p['turnaround_time']}\t\t{p['waiting_time']}\t\t{p['response_time']}")

# Display averages
print("\nAverage Waiting Time:", avg_waiting_time)
print("Average Turnaround Time:", avg_turnaround_time)
print("Average Response Time:", avg_response_time)

