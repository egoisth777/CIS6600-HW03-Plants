import LSystem as lsys

l_system = lsys.LSystem()

# Configure the LSystem

l_system.setDefaultAngle(22.5) # set the rotation angle in degrees
l_system.setDefaultStep(1.0) # set the step size


# Testing loading the program
program = """F
F->F+[+F]F[-F]F
"""
l_system.loadProgramFromString(program)

# testing printing the iterations
for i in range(0, 2):
    result = l_system.getIteration(i)
    print(f"L-System String after {i}th iterations:\n{result}")
