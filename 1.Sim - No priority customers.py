import simpy
import random

def customer(env, name, employees, arrival_time, service_time):
    """
    A customer arrives at the store, waits in queue for service
    and leaves after receiving service.
    """
    print(f'{name} arrives at time {env.now:.2f}')
    with employees.request() as request:
        yield request
        print(f'{name} starts receiving service at time {env.now:.2f}')
        yield env.timeout(service_time)
        print(f'{name} finishes receiving service at time {env.now:.2f}')

def generate_customers(env, employees, max_customers, arrival_time_mean, arrival_time_std, service_time_mean, service_time_std):
    """
    Generate new customers randomly with a time interval of the arrival time.
    """
    for i in range(max_customers):
        yield env.timeout(random.normalvariate(arrival_time_mean, arrival_time_std))
        env.process(customer(env, f'Customer {i+1}', employees, env.now, random.normalvariate(service_time_mean, service_time_std)))
        
# Set parameters
max_customers = 10
arrival_time_mean = 2
arrival_time_std = 1
service_time_mean = 10
service_time_std = 2

# Create and run simulation with SimPy
env = simpy.Environment()
employees = simpy.Resource(env, capacity=2)
env.process(generate_customers(env, employees, max_customers, arrival_time_mean, arrival_time_std, service_time_mean, service_time_std))
env.run()
