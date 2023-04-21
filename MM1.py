import math
import random
import matplotlib.pyplot as plt

# Queue maximum capacity
Q_LIMIT = 100

# States of the server
BUSY = 1
IDLE = 0

num_events = 2  # Number of possible events
time_next_event = [0.0] * (num_events + 1)  # Time of next event for each event type

queue_length = []  # List to store the number of customers in the queue at each time point
time_points = []  # List to store the time points for the queue length data

def initialize(mean_interarrival, mean_service):

    # Declare global variables
    global server_status, num_in_q, time_last_event, num_custs_delayed, total_of_delays, area_num_in_q, area_server_status, time_next_event, time_arrival

    # Initializing simulation variables
    time = 0.0
    server_status = IDLE
    num_in_q = 0
    time_last_event = 0.0

    num_custs_delayed = 0
    total_of_delays = 0.0
    area_num_in_q = 0.0
    area_server_status = 0.0

    # Schedule the first arrival event and set the time of the next departure event to infinity
    time_next_event[1] = time + random.expovariate(1.0 / mean_interarrival)
    time_next_event[2] = 1.0e+30

    # List for storing arrival times
    time_arrival = []

    # Lists for recording data
    global num_in_q_list, server_utilization_list, delay_list, time_list
    num_in_q_list = []
    server_utilization_list = []
    delay_list = []
    time_list = []

def timing():

    # Declare global variables
    global time, next_event_type, time_next_event

    # Variables for the loop
    min_time_next_event = 1.0e+29
    next_event_type = 0

    # Loop over all events to find the next event type and its corresponding time
    for i in range(1, num_events + 1):
        if time_next_event[i] < min_time_next_event:
            min_time_next_event = time_next_event[i]
            next_event_type = i

    # If the event list is empty print:
    if not next_event_type:
        print(f"Event list empty at time {time}")
        exit(1)

    # Update the simulation time to the next event time
    time = min_time_next_event

def arrive():

    # Declare global variables
    global server_status, num_in_q, total_of_delays, num_custs_delayed, time_arrival, time_next_event, mean_service

    # Schedule the next arrival event
    time_next_event[1] = time + random.expovariate(1.0 / mean_interarrival)

    # If the server is busy, add the customer to the queue
    if server_status == BUSY:
        num_in_q += 1

        # If the queue is full print:
        if num_in_q > Q_LIMIT:
            print(f"Overflow of the array time_arrival at time {time}")
            exit(2)

        # Record the arrival time of the customer
        time_arrival.append(time)

    # If the server is idle, start service for the customer
    else:
        delay = 0.0
        total_of_delays += delay

        num_custs_delayed += 1
        server_status = BUSY

        # Schedule the departure event for the customer
        time_next_event[2] = time + random.expovariate(1.0 / mean_service)

    # Record data for plotting
    num_in_q_list.append(num_in_q)
    server_utilization_list.append(area_server_status / time)
    delay_list.append(total_of_delays / num_custs_delayed)
    time_list.append(time)

def depart():

    # Declare global variables
    global server_status, num_in_q, total_of_delays, num_custs_delayed, time_arrival, time_next_event, mean_service

    # If the queue is empty, set the server to idle and remove the departure event
    if num_in_q == 0:
        server_status = IDLE
        time_next_event[2] = 1.0e+30

    # If the queue is not empty, serve the next customer in the queue
    else:
        num_in_q -= 1

        # Calculate the delay for the customer and update the delay statistics
        delay = time - time_arrival.pop(0)
        total_of_delays += delay

        num_custs_delayed += 1

        # Schedule the departure event for the next customer in the queue
        time_next_event[2] = time + random.expovariate(1.0 / mean_service)

    # Record data for plotting
    num_in_q_list.append(num_in_q)
    server_utilization_list.append(area_server_status / time)
    delay_list.append(total_of_delays / num_custs_delayed)
    time_list.append(time)

def update_time_avg_stats():

    # Declare global variables
    global time_since_last_event, time_last_event, area_num_in_q, area_server_status, queue_length, time_points

    # Calculate the time since the last event and update the last event time
    time_since_last_event = time - time_last_event
    time_last_event = time

    # Update the area under the queue length and server status curves
    area_num_in_q += num_in_q * time_since_last_event
    area_server_status += server_status * time_since_last_event

    # Record the current queue length and simulation time
    queue_length.append(num_in_q)
    time_points.append(time)

def expon(mean):

    # Generates a random number from an exponential distribution with mean 'mean'
    u = random.random()
    return -mean * math.log(u)

# Read input parameters
mean_interarrival = float(input("Mean interarrival time(λ): "))
mean_service = float(input("Mean service time(μ): "))
num_delays_required = int(input("Number of customers: "))

# Initialize the simulation
time_arrival = []  # List of arrival times

# Set up the simulation
initialize(mean_interarrival=mean_interarrival, mean_service=mean_service)

# Run the simulation while more delays are still needed
while num_custs_delayed < num_delays_required:

    # Determine the next event and update the simulation time
    timing()
    update_time_avg_stats()

    # If the next event is an arrival
    if next_event_type == 1:

        # Simulate the arrival of a customer
        arrive()

    # Simulate the departure of a customer
    elif next_event_type == 2:
        depart()


def report():

    # Declare global variables
    global num_custs_delayed, total_of_delays, area_num_in_q, area_server_status

    # Print out the results of the simulation
    print(f"Average delay in queue: {total_of_delays / num_custs_delayed:.3f} minutes")
    print(f"Average number in queue: {area_num_in_q / time:.3f}")
    print(f"Server utilization: {area_server_status / time:.3f}")
    print(f"Time simulation ended: {time:.3f}")

    # Plot the number of customers in the queue over time
    plt.plot(time_points, num_in_q_list)
    plt.xlabel("Time")
    plt.ylabel("Number of customers in queue")
    plt.title("Number of customers in queue over time")
    plt.grid()
    plt.show()

# Report the simulation results
report()
