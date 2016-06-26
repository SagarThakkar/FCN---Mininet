import pdb
"""
The Bellman-Ford algorithm
g API:
    iter(g) gives all nodes
    iter(g[u]) gives neighbours of u
    g[u][v] gives weight of edge (u, v)
"""

# Step 1: For each node prepare the destination and predecessor
def initialize(g, host):
    d = {} # Stands for destination
    p = {} # Stands for predecessor
    for node in g:
        d[node] = float('Inf') # We start admiting that the rest of nodes are very very far
        p[node] = None
    d[host] = 0 # For the host we know how to reach
    return d, p

def relax(node, neighbour, g, d, p):
    # If the distance between the node and the neighbour is lower than the one I have now
    if d[neighbour] > d[node] + g[node][neighbour]:
        # Record this lower distance
        d[neighbour]  = d[node] + g[node][neighbour]
        p[neighbour] = node

def bellman_ford(g, host):
    d, p = initialize(g, host)
    for i in range(len(g)-1): #Run this until is converges
        for u in g:
            for v in g[u]: #For each neighbour of u
                relax(u, v, g, d, p) #Lets relax it

    # Step 3: check for negative-weight cycles
    for u in g:
        for v in g[u]:
            assert d[v] <= d[u] + g[u][v]

    return d, p


host[] = {H1,H2,R1,R2,R3,R4}
   
if __name__ == '__main__': bellman_ford(topo,hosts)

