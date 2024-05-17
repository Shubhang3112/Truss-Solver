import numpy as py

def truss_solver(n,node_loads,node_coordinates,node_constraints,adjacency_matrix,trigno_matrix,member_no,reactions):
    coefficient_matrix=[]
    constant_matrix=[]
    for i in range(2*n):
        temp=[]
        constant_matrix.append(0)
        for j in range(2*n):
            temp.append(0)
        coefficient_matrix.append(temp)
    idx = 2*n - reactions
    for i in range(n):
        constant_matrix[2*i]+=-1*node_loads[i][0]
        constant_matrix[2*i+1]+=-1*node_loads[i][1]
        if(node_constraints[i][0]!=0):
            coefficient_matrix[2*i][idx]=1
            idx+=1
        if(node_constraints[i][1]!=0):
            coefficient_matrix[2*i+1][idx]=1
            idx+=1
        for j in range(n):
            if(i==j): continue
            if member_no[i][j]==-1: continue
            coefficient_matrix[2*i][member_no[i][j]]=trigno_matrix[i][j][0]/trigno_matrix[i][j][2]
            coefficient_matrix[2*i+1][member_no[i][j]]=trigno_matrix[i][j][1]/trigno_matrix[i][j][2]
    ans = py.linalg.solve(coefficient_matrix,constant_matrix)
    return ans

def deflection(idx,ans,lengths,n,E,A,node_coordinates,node_constraints,adjacency_matrix,trigno_matrix,member_no,reactions):
    node_loads=[]
    for i in range(n):
        if i==idx: node_loads.append([-1,0])
        else: node_loads.append([0,0])
    a=truss_solver(n,node_loads,node_coordinates,node_constraints,adjacency_matrix,trigno_matrix,member_no,reactions)
    sum=0
    for i in range(2*n-reactions):
        sum+=ans[i]*a[i]*lengths[i]
    hori=sum/(A*E)
    node_loads=[]
    for i in range(n):
        if i==idx: node_loads.append([0,-1])
        else: node_loads.append([0,0])
    a=truss_solver(n,node_loads,node_coordinates,node_constraints,adjacency_matrix,trigno_matrix,member_no,reactions)
    sum=0
    for i in range(2*n-reactions):
        sum+=ans[i]*a[i]*lengths[i]
    veri=sum/(A*E)
    return hori,veri


n=int(input())
E=float(input())
A=float(input())
node_coordinates=[]
for i in range(n):
    temp=[]
    temp.append(int(input()))
    temp.append(int(input()))
    node_coordinates.append(temp)
node_loads=[]
for i in range(n):
    temp=[]
    temp.append(int(input()))
    temp.append(int(input()))
    node_loads.append(temp)
node_constraints=[]
for i in range(n):
    temp=[]
    temp.append(int(input()))
    temp.append(int(input()))
    node_constraints.append(temp)
adjacency_matrix=[]
for i in range(n):
    temp=[]
    for j in range(n):
        temp.append(int(input()))
    adjacency_matrix.append(temp)
trigno_matrix=[]
for i in range(n):
    temp=[]
    for j in range(n):
        a=[]
        a.append(node_coordinates[j][0]-node_coordinates[i][0])
        a.append(node_coordinates[j][1]-node_coordinates[i][1])
        a.append((a[0]**2+a[1]**2)**0.5)
        temp.append(a)
    trigno_matrix.append(temp)
member_no=[]
lengths=[]
ct=0
for i in range(n):
    temp=[]
    for j in range(n):
        if i>j: temp.append(member_no[j][i])
        elif i==j: temp.append(-1)
        elif adjacency_matrix[i][j]==0: temp.append(-1)
        else:
            temp.append(ct)
            lengths.append(trigno_matrix[i][j][2])
            ct+=1
    member_no.append(temp)
reactions=0
for i in range(n):
    reactions+=node_constraints[i][0]+node_constraints[i][1]
# reaction_matrix = [[0,0,0],[0,0,0],[0,0,0]]
# idx=0
# cx=0;cy=0;m=0
# for i in range(n):
#     if(node_loads[i][0]!=0): 
#         cx+=-1*node_loads[i][0]
#         m+=-1*(node_coordinates[i][1]-node_coordinates[0][1])*node_loads[i][0]
#     if(node_loads[i][1]!=0): 
#         cy+=-1*node_loads[i][1]
#         m+=(node_coordinates[i][0]-node_coordinates[0][0])*node_loads[i][1]
#     if(node_constraints[i][0]!=0):
#         reaction_matrix[0][idx]=1
#         reaction_matrix[2][idx]=(node_coordinates[i][1]-node_coordinates[0][1])
#         idx+=1
#     if(node_constraints[i][1]!=0):
#         reaction_matrix[1][idx]=1
#         reaction_matrix[2][idx]=-1*(node_coordinates[i][0]-node_coordinates[0][0])
#         idx+=1
# b=[cx,cy,m]
# r1,r2,r3 = py.linalg.solve(reaction_matrix,b)
# for i in range(n):
#     for j in range(n):
#         print(trigno_matrix[i][j])

ans=truss_solver(n,node_loads,node_coordinates,node_constraints,adjacency_matrix,trigno_matrix,member_no,reactions)
print("The member force matrix is:")
for i in range(n):
    for j in range(n):
        if(member_no[i][j]==-1):print(0,end=" ")
        else: print(ans[member_no[i][j]],end=" ")
    print()
print()
print("The reactions are")
idx = 2*n-reactions 
for i in range(n):
    if(node_constraints[i][0]):
        print(f"Horizontal Reaction at node {i+1} is {ans[idx]}")
        idx+=1
    if(node_constraints[i][1]):
        print(f"Vertical Reaction at node {i+1} is {ans[idx]}")
        idx+=1
print()   
print("The deflections are")

for i in range(n):
    hori,veri=deflection(i,ans,lengths,n,E,A,node_coordinates,node_constraints,adjacency_matrix,trigno_matrix,member_no,reactions)
    print(f"The horizontal and vertical deflections at node {i+1} are {hori} and {veri} respectively.")