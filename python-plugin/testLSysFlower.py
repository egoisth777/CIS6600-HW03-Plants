import LSystem as lsys


l_system = lsys.LSystem()

# Configure the LSystem

l_system.setDefaultAngle(30) # set the rotation angle in degrees
l_system.setDefaultStep(1.0) # set the step size


# Testing loading the program
program = """X
X->F[+X][-X]FX
F->*FF*
"""
l_system.loadProgramFromString(program)


branches = lsys.VectorPyBranch()
flowers = lsys.VectorPyBranch()

# testing printing the iterations
for i in range(0, 2):
    result = l_system.getIteration(i)
    l_system.processPy(i, branches, flowers)
    print(f"L-System String after {i}th iterations:\n{result}")
