import gurobipy as gp
from gurobipy import GRB

# Color Weights

W = [[1,1,1,1,1,1,1,1,1],
     [1,1,1,1,2,1,1,1,1],
     [1,2,2,2,2,2,3,3,1],
     [1,1,4,4,2,3,3,1,1],
     [5,1,1,4,2,3,1,1,6],
     [5,5,1,1,2,1,1,6,6],
     [7,5,5,1,1,1,8,9,6],
     [7,7,5,5,1,8,8,9,6],
     [7,5,5,5,5,5,9,9,9]]

n = len(W[0])

def solveMatrix(W, n):
    print(W)
    print(n)
    
    # Create Model
    model = gp.Model("Queens")

    # Create Edge Variable
    edge = model.addVars(n, n, vtype=GRB.BINARY, name="edge")

    # Create Color Variable
    color = model.addVars(n, lb=1, ub=100, vtype=GRB.INTEGER, name="color")

    # Constants
    eps = 0.0001
    M = 1000

    # One Queen Per Row Constraint
    for j in range(n):
        model.addConstr(sum(edge[i, j] for i in range(n)) == 1, name=f"col_sum_{j}")

    # One Queen Per Col Constraint
    for i in range(n):
        model.addConstr(sum(edge[i, j] for j in range(n)) == 1, name=f"row_sum_{i}")

    # No Adjacent Coloring Constraint
    for i in range(1, n-1):
        for j in range(1, n-1):
            model.addConstr(edge[i-1, j-1] + edge[i, j] <= 1)
            model.addConstr(edge[i-1, j] + edge[i, j] <= 1)
            model.addConstr(edge[i-1, j+1] + edge[i, j] <= 1)
            model.addConstr(edge[i, j+1] + edge[i, j] <= 1)
            model.addConstr(edge[i+1, j+1] + edge[i, j] <= 1)
            model.addConstr(edge[i+1, j] + edge[i, j] <= 1)
            model.addConstr(edge[i+1, j-1] + edge[i, j] <= 1)
            model.addConstr(edge[i, j-1] + edge[i,j] <= 1)
    for j in range(1, n-1):
        # First Row
        model.addConstr(edge[0, j-1] + edge[0,j] <= 1)
        model.addConstr(edge[0+1, j-1] + edge[0,j] <= 1)
        model.addConstr(edge[0+1, j] + edge[0,j] <= 1)
        model.addConstr(edge[0+1, j+1] + edge[0,j] <= 1)
        model.addConstr(edge[0, j+1] + edge[0,j] <= 1)

        # Last Row
        model.addConstr(edge[(n-1), j-1] + edge[(n-1),j] <= 1)
        model.addConstr(edge[(n-1)-1, j-1] + edge[(n-1),j] <= 1)
        model.addConstr(edge[(n-1)-1, j] + edge[(n-1),j] <= 1)
        model.addConstr(edge[(n-1)-1, j+1] + edge[(n-1),j] <= 1)
        model.addConstr(edge[(n-1), j+1] + edge[(n-1),j] <= 1)




    # Color Definition Constraint
    for i in range(n):
        model.addConstr(color[i] == sum(edge[i, j] * W[i][j] for j in range(n)), name=f"color_def_{i}")

    # Distinct Colors Constraint
    for r_1 in range(n - 1):
        for r_2 in range(r_1 + 1, n):
            # Binary variable for each pair (r_1, r_2)
            b = model.addVar(vtype=GRB.BINARY, name=f"b_{r_1}_{r_2}")

            # Big-M constraints to determine if color[r_1] > color[r_2]
            model.addConstr(color[r_1] >= color[r_2] + eps - M * (1 - b), name=f"bigM_constr1_{r_1}_{r_2}")
            model.addConstr(color[r_1] <= color[r_2] + M * b, name=f"bigM_constr2_{r_1}_{r_2}")

            # Conditional constraints for OR condition
            model.addConstr((b == 1) >> (color[r_1] + color[r_2] >= 2 * color[r_2] + 0.1), name=f"or_constr1_{r_1}_{r_2}")
            model.addConstr((b == 0) >> (color[r_1] + color[r_2] >= 2 * color[r_1] + 0.1), name=f"or_constr2_{r_1}_{r_2}")

    # Optional constraint removed temporarily if testing feasibility issues
    # model.addConstr(sum(color[i] for i in range(n)) == (n*(n+1))/2, name="sum_of_colors")

    # Optimize the model
    model.optimize()

    # Check the optimization status and print results
    result = []
    if model.status == GRB.OPTIMAL:
        for i in range(n):
            for j in range(n):
                if edge[i, j].X != 0:
                    #print(f"edge[{i},{j}] = {edge[i, j].X}")  # Output the edge values
                    result.append([i+1, j+1])
        #for i in range(n):
            #print(f"color[{i}] = {color[i].X}")  # Output the color values
    #else:
        #print("No feasible solution found.")
    
    return result


print(solveMatrix([[1,1]], 1))