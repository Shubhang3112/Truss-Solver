2-D Truss Solver

All data to be inserted line by line. Not more than one value in a line. Each value in a new line.

1) First input the number of nodes
2) Then input the elastic modulus in Pa and area in m^2 
3) Then input x and y coordinates of all nodes one by one
4) Then input the load on all nodes (first horizontal and then vertical)
5) Then input the constraints on each node (first horizontal and then vertical). Input 1 if reaction is present in that direction else input 0. For example for pinned, input 1 & 1 for vertical roller, input 0 & 1 etc.
6) Then input a n*n matrix A where if A(i,j)=1 then there exists a member between nodes i and j and if A(i,j)=0 then no member exist between nodes i and j.

Example input: 

3
29000000000
0.0005
0 
0
3 
4
6 
0
0
0
0
-2
0
0
1
1
0
0
0
1
1
1
1
1
1
1
1
1
1

