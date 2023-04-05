import random

import simpy



wait_times = []



class CleanFoodDriveThrough(object):
    
    def __init__(self, env,design):
        self.env = env
        self.driveThrough = None
        self.service_times = None
        self.service_probabilities = None
        if design == "A":
            self.service_times = [2, 3, 4, 5, 6, 7, 8, 9]
            self.service_probabilities = [.24, .2, .15, .14, .12, .08, .05, .02]
            self.driveThrough = simpy.Resource(env, 1)
            
        elif design == "B":
            self.service_times = [1,2,3,4,5]
            self.service_probs = [.2,.35,.3,.1,.05]
            self.driveThrough = simpy.Resource(env, 1)

        elif design == "C":
            self.service_times = [2, 3, 4, 5, 6, 7, 8, 9]
            self.service_probabilities = [.24, .2, .15, .14, .12, .08, .05, .02]
            self.driveThrough = simpy.Resource(env, 2)
        else:
            print("pick A B or C")
            
            


    def serve_customer(self, car):
        
        service_time = random.choices(self.service_times, self.service_probabilities)[0]
        yield self.env.timeout(service_time)
        
        


def customer(env, name, DT):
    
    
    arrival_time = env.now
    begin_service_time = None
    with DT.driveThrough.request() as request:
        yield request
        begin_service_time = env.now
        wait_times.append(begin_service_time-arrival_time)
        yield env.process(DT.serve_customer(name))
        
        

        




def initialize(env,design):
    
    driveThrough = CleanFoodDriveThrough(env, design)

    # Generate cars with exponential interarrival times
    i = 0
    while True:
        yield env.timeout(random.expovariate(1/6))
        i += 1
        env.process(customer(env, 'Customer %d' % i, driveThrough))






def run_simulation(design):
    env = simpy.Environment()
    env.process(initialize(env,design))
    hours = 5
    mins = 60
    env.run(until=hours*mins)
    average = sum(wait_times)/len(wait_times)
    max_time = max(wait_times)
    
    
    
    print("Average wait time for design {design}: {average}".format(design = design,average = average))
    print("Max wait time for design {design}: {max}".format(design = design,max = max_time))

    


if __name__ == "__main__":

    designs = ["A","B","C"]

    for design in designs:
        run_simulation(design)
        wait_times = []