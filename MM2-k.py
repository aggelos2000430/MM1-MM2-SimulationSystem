import random
import matplotlib.pyplot as plt

# Queue maximum capacity
Q_LIMIT = 100

# States of the server
BUSY = 1
IDLE = 0

# Number of possible events
num_events = 2
time_next_event = [0.0] * (num_events + 1)  # Time of next event for each event type

queue_length = []  # List to store the number of customers in the queue at each time point
time_points = []  # List to store the time points for the queue length data

def initialize(mean_interarrival, mean_service, num_servers):

    # Declare global variables
    global server_status, num_in_q, time_last_event, num_custs_delayed, total_of_delays, area_num_in_q, area_server_status, time_next_event, time_arrival, servers

    # Initializing simulation variables
    time = 0.0
    server_status = [IDLE] * num_servers
    num_in_q = 0
    time_last_event = 0.0

    num_custs_delayed = 0
    total_of_delays = 0.0
    area_num_in_q = 0.0
    area_server_status = 0.0

    servers = num_servers

    # Schedule the first arrival event and set the time of the next departure event to infinity
    time_next_event[1] = time + random.expovariate(1.0 / mean_interarrival)
    time_next_event[2] = 1.0e+30

    # List for storing arrival times
    time_arrival = []

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

def arrive(mean_service):

    # Declare global variables
    global server_status, num_in_q, total_of_delays, num_custs_delayed, time_arrival, time_next_event, servers

    # Schedule the next arrival event
    time_next_event[1] = time + random.expovariate(1.0 / mean_interarrival)

    # Find an idle server, if any
    idle_server = find_idle_server()

    # If there are no idle servers
    if idle_server == -1:

        # Increment the number of customers in the queue
        num_in_q += 1

        # Check if the queue has exceeded the maximum length
        if num_in_q > Q_LIMIT:
            print(f"Overflow of the array time_arrival at time {time}")

            # Exit the simulation with an error code
            exit(2)

        # Add the arrival time of the customer to the time_arrival list
        time_arrival.append(time)

    # If there is an idle server
    else:

        # Initialize the delay to zero
        delay = 0.0

        # Update the total delay time
        total_of_delays += delay

        # Increment the number of customers delayed
        num_custs_delayed += 1

        # Set the server status to busy
        server_status[idle_server] = BUSY

        # Schedule the departure of the customer
        time_next_event[2] = time + random.expovariate(1.0 / mean_service)

def depart():

    # Declare global variables
    global server_status, num_in_q, total_of_delays, num_custs_delayed, time_arrival, time_next_event, mean_service, servers

    # Find a busy server, if any
    busy_server = find_busy_server()

    # If there are no busy servers
    if busy_server == -1:

        # Set the departure time to infinity
        time_next_event[2] = 1.0e+30

    # If there is a busy server
    else:

        # If there are no customers waiting in the queue
        if num_in_q == 0:

            # Set the server status to idle
            server_status[busy_server] = IDLE

            # Set the departure time to infinity
            time_next_event[2] = 1.0e+30

        # If there are customers waiting in the queue
        else:

            # Decrement the number of customers in the queue
            num_in_q -= 1

            # Calculate the delay and update the total delay time
            delay = time - time_arrival.pop(0)
            total_of_delays += delay

            # Increment the number of customers delayed
            num_custs_delayed += 1

            # Schedule the departure of the next customer
            time_next_event[2] = time + random.expovariate(1.0 / mean_service)

            # Set the server status to busy
            server_status[busy_server] = BUSY

def update_time_avg_stats():

    # Declare global variables
    global time_since_last_event, time_last_event, area_num_in_q, area_server_status, queue_length, time_points

    # Calculate the time since the last event and update the time of the last event
    time_since_last_event = time - time_last_event
    time_last_event = time

    # Update the area under the number in queue and server status curves
    area_num_in_q += num_in_q * time_since_last_event
    area_server_status += sum([status == BUSY for status in server_status]) * time_since_last_event

    # Add the current number in queue and time to the respective lists
    queue_length.append(num_in_q)
    time_points.append(time)

def find_idle_server():

    # Declare global variables
    global server_status, servers

    # Loop through each server
    for i in range(servers):

        # If the server is idle, return its index
        if server_status[i] == IDLE:
            return i

    # If no idle servers are found, return -1
    return -1

def find_busy_server():

    # Declare global variables
    global server_status, servers

    # Loop through each server
    for i in range(servers):

        # If the server is busy, return its index
        if server_status[i] == BUSY:
            return i

    # If no busy servers are found, return -1
    return -1

def report():

    # Declare global variables
    global num_custs_delayed, total_of_delays, area_num_in_q, area_server_status

    print(f"Average delay in queue: {total_of_delays / num_custs_delayed:.3f} minutes")
    print(f"Average number in queue: {area_num_in_q / time:.3f}")
    print(f"Server utilization: {area_server_status / (servers * time):.3f}")

# Plot the number of customers in the queue over time
def plot_queue_length(time_points, queue_length):
    plt.plot(time_points, queue_length)
    plt.xlabel('Simulation Time')
    plt.ylabel('Queue Length')
    plt.title('Queue Length vs. Simulation Time')

    # Show the plot
    plt.show()

def main():

    # Declare global variables
    global mean_interarrival, mean_service, num_servers, num_customers

    mean_interarrival = float(input('Mean interarrival time(λ):'))
    mean_service = float(input('Mean service time(μ):'))
    num_servers = 2
    num_customers = int(input('Number of customers:'))

    # Initialize the simulation
    initialize(mean_interarrival, mean_service, num_servers)

    # Run the simulation until all customers have been served
    while num_custs_delayed < num_customers:
        timing()

        update_time_avg_stats()

        # If the next event is an arrival, handle it
        if next_event_type == 1:
            arrive(mean_service)

        # If the next event is a departure, handle it
        elif next_event_type == 2:
            depart()

    # Report the simulation results
    report()

    # Plot the number of customers in the queue over time
    plot_queue_length(time_points, queue_length)

if __name__ == "__main__":
    main()
