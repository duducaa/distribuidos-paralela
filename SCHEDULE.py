import numpy as np

MEM_SIZE = 100

# simple linear memory, filled with random floats
memory = np.random.random(MEM_SIZE)  

# number of processes to simulate
N_PROC = 4   


# Process definition
class Process():
    # MBR
    def __init__(self, id, mem_address, functions) -> None:
        self.id = id
        self.mem_address = mem_address
        self.functions = functions
        self.counter = 0
        self.variables = [memory[mem_address[0]:mem_address[1]], None, None, None]
        self.end = False
        self.status = "ready"
        self.quantum = 0
        self.waiting_t = 0

    def execute(self):
        c = self.counter
        self.variables[c + 1] = self.functions[c](self.variables)
        self.counter += 1

        # If all instructions are done → mark as terminated
        if self.counter == len(self.functions):
            self.status = "terminated"
            self.end = True


# Programs
codes = {
    "zscore": [
        lambda vars: vars[0].mean(),                      
        lambda vars: vars[0].std(),                       
        lambda vars: (vars[0] - vars[1]) / (vars[2] + 1e-8) 
    ],
    "minmax": [
        lambda vars: vars[0].max(),
        lambda vars: vars[0].min(),
        lambda vars: (vars[0] - vars[1]) / (vars[2] - vars[1] + 1e-8) 
    ],
    "clip": [
        lambda vars: np.percentile(vars[0], 25),            
        lambda vars: np.percentile(vars[0], 75),            
        lambda vars: np.clip(vars[0], vars[1], vars[2])
    ]
}

# ensure that the lower limit is less than the upper
def valid_space():
    """
    Selects a valid random memory interval [a, b)
    ensuring a < b.
    """
    a, b = 0, 0
    while a >= b:
        a = np.random.randint(0, MEM_SIZE)
        b = np.random.randint(0, MEM_SIZE)
    return a, b


# Log function
def log(processes, t, current=None):
    print("---------------------")
    print(f"=== t = {t} ===")
    if current is not None:
        print(f">>> Running P{current.id} | quantum={current.quantum} | status={current.status}")
    for p in processes:
        print(f"P{p.id}: STATUS={p.status} COUNTER={p.counter} WAIT_T={p.waiting_t}")
    print("---------------------")


# Creation of process
processes = [
    Process(id, valid_space(), codes[np.random.choice(list(codes.keys()))])
    for id in range(N_PROC)
]


# Scheduler
proc_id = 0
t = 0  

while not all([p.end for p in processes]):
    process = processes[proc_id]

    if not process.end:
        # If process is ready, assign a new quantum and set it to running
        if process.status == "ready":
            process.quantum = np.random.choice([1, 2, 3], p=[0.6, 0.25, 0.15])
            process.status = "running"

        # Execute for the length of the assigned quantum
        for _ in range(process.quantum):
            log(processes, t, process)

            # process is waiting, so decrement waiting timer
            if process.status == "waiting":
                process.waiting_t -= 1
                if process.waiting_t == 0:
                    process.status = "ready"
                t += 1
                continue

            # randomly trigger a stop case
            if np.random.random() <= 0.35 and process.status == "running":
                process.waiting_t = 3
                process.status = "waiting"
                t += 1
                break  # stop current quantum

            # normal execution of one instruction
            if process.status == "running":
                process.execute()
                t += 1

        # If process has finished execution, is terminated
        if process.end:
            process.status = "terminated"

        # If still running after quantum, go to ready
        elif process.status == "running":
            process.status = "ready"

    # always move to the next process
    proc_id = (proc_id + 1) % N_PROC
