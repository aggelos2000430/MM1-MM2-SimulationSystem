import simpy
import random
import matplotlib.pyplot as plt

# Define the source process that generates customers and adds them to the queue
def source(env, mean_interarrival_time, mean_service_time, number_of_customers, server):

    for i in range(number_of_customers):

        # Create a new customer process
        customer = customer_process(env, f"Customer {i}", server, mean_service_time)
        env.process(customer)

        # Generate a random interarrival time and wait for it
        interarrival_time = random.expovariate(1.0 / mean_interarrival_time)
        yield env.timeout(interarrival_time)

# Define the customer process that represents a single customer in the queue
def customer_process(env, name, server, mean_service_time):

    # Record the arrival time, queue length, and arrival time
    arrival_time = env.now
    queue_lengths.append(len(server.queue))
    arrival_times.append(arrival_time)

    # Request access to the server and wait until access is granted
    with server.request() as req:
        yield req

        # Calculate and record the delay
        delay = env.now - arrival_time
        delays.append(delay)

        # Generate a random service time and wait for it
        service_time = random.expovariate(1.0 / mean_service_time)
        yield env.timeout(service_time)

        # Record the completion time
        completion_times.append(env.now)

# Take user input for the simulation parameters
mean_interarrival_time = float(input("Enter the mean interarrival time: "))
mean_service_time = float(input("Enter the mean service time: "))
number_of_customers = int(input("Enter the number of customers: "))
number_of_servers = int(input("Enter the number of servers: "))

# Create the simulation environment, server resource, and empty lists for data recording
env = simpy.Environment()
server = simpy.Resource(env, capacity=number_of_servers)

delays = []
queue_lengths = []
arrival_times = []
completion_times = []

# Start the source process and run the simulation
env.process(source(env, mean_interarrival_time, mean_service_time, number_of_customers, server))
env.run()

# Calculate and print out simulation statistics
average_delay = sum(delays) / len(delays)
average_number_in_queue = sum(queue_lengths) / len(queue_lengths)
server_utilization = sum(completion_times) / (number_of_servers * env.now)
simulation_time = env.now

print(f"Average delay in queue: {average_delay:.2f}")
print(f"Average number in queue: {average_number_in_queue:.2f}")
print(f"Server utilization: {server_utilization:.2f}")
print(f"Time simulation ended: {simulation_time:.2f}")

# Generate a plot of the queue length over time
plt.plot(arrival_times, queue_lengths)
plt.xlabel("Simulation Time")
plt.ylabel("Queue Length")
plt.title("Queue Length vs Simulation Time")
plt.show()
