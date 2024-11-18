import os

# Define configurations for opLat and issueLat such that opLat + issueLat = 7
configurations = [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)]

# Path to MinorDefaultFUPool.py
fuPool_path = "gem5/src/cpu/minor/BasicMinorCPU.py"

# Directory for simulation results
output_dir = "simulation_results"
os.makedirs(output_dir, exist_ok=True)

# Path to gem5 binary
gem5_binary = "build/X86/gem5.opt"  # Replace X86 with your architecture if needed

# Path to your simulation configuration script
config_script = "configs/example/se.py"

# Path to your DAXPY binary
daxpy_binary = "daxpy_binary"  # Replace with the actual path

# Function to modify FloatSimd parameters
def modify_fyupool(opLat, issueLat):
    with open(fuPool_path, 'r') as file:
        data = file.readlines()

    for i, line in enumerate(data):
        if "FloatSimd" in line:
            data[i + 1] = f"    opLat: {opLat},\n"
            data[i + 2] = f"    issueLat: {issueLat},\n"
            break

    with open(fuPool_path, 'w') as file:
        file.writelines(data)

# Iterate through all configurations
for idx, (opLat, issueLat) in enumerate(configurations):
    print(f"Running simulation for configuration {idx + 1}: opLat={opLat}, issueLat={issueLat}")

    # Modify FUPool
    modify_fyupool(opLat, issueLat)

    # Rebuild gem5
    os.system(f"scons {gem5_binary}")

    # Run simulation
    output_stats = f"{output_dir}/stats_opLat{opLat}_issueLat{issueLat}.txt"
    os.system(f"{gem5_binary} {config_script} --cmd={daxpy_binary} > {output_stats}")
