# Modified code based on the given requirements

import simpy
import random

def customer(env, name, employees_a, employees_b, arrival_time, service_time):
    """
    A customer arrives at the store, waits in queue A or B based on their type for service
    and leaves after receiving service.
    """
    print(f'{name} ({type_dict[name]}) arrives at time {env.now:.2f}')
    if type_dict[name] == 'A':
        with employees_a.request() as request:
            yield request
            print(f'{name} starts receiving service at time {env.now:.2f}')
            yield env.timeout(service_time)
            print(f'{name} finishes receiving service at time {env.now:.2f}')
    else:
        with employees_b.request() as request:
            yield request
            print(f'{name} starts receiving service at time {env.now:.2f}')
            yield env.timeout(service_time)
            print(f'{name} finishes receiving service at time {env.now:.2f}')

def generate_customers(env, employees_a, employees_b, max_customers, arrival_time_mean, arrival_time_std, service_time_mean, service_time_std):
    """
    Generate new customers randomly with a time interval of the arrival time.
    """
    global arrival_time_count
    for i in range(max_customers):
        yield env.timeout(random.normalvariate(arrival_time_mean, arrival_time_std))
        arrival_time = env.now
        if random.random() < 0.2:
            name = f'Customer {arrival_time_count+1}'
            type_dict[name] = 'A'
        else:
            name = f'Customer {arrival_time_count+1}'
            type_dict[name] = 'B'
        env.process(customer(env, name, employees_a, employees_b, arrival_time, random.normalvariate(service_time_mean, service_time_std)))
        arrival_time_count += 1

# Set parameters
max_customers = 10
arrival_time_mean = 2
arrival_time_std = 1
service_time_mean = 10
service_time_std = 2

# Create and run simulation with SimPy
env = simpy.Environment()
employees_a = simpy.Resource(env, capacity=1)
employees_b = simpy.Resource(env, capacity=1)
type_dict = {}
arrival_time_count = 0
env.process(generate_customers(env, employees_a, employees_b, max_customers, arrival_time_mean, arrival_time_std, service_time_mean, service_time_std))
env.run()