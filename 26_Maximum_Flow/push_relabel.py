import random


def push_relabel(V, E, neighbourhood, cap, s="s", t="t"):
    height = init_height(V, s, t)
    flow, excess, overflowing = init_preflow(V, E, neighbourhood, cap, s, t)

    while len(overflowing) > 0:
        u = overflowing.pop()

        new_overflowing = push_from_vertex(u, neighbourhood, cap, height, excess, flow, t)
        overflowing += new_overflowing
        if excess[u] > 0:
            overflowing.append(u)
            relabel(u, height, neighbourhood)
    return -excess[s], flow


def init_height(V, s, t):
    # height function h: V-> |N
    height = {v: 0 for v in V}
    height[s] = len(V)
    height[t] = 0
    return height


def push_from_vertex(u, neighbourhood, cap, height, excess, flow, t):
    u_neighbourhood = neighbourhood[u]
    new_overflowing = []
    for v in u_neighbourhood:
        if height[u] == height[v]+1:
            push(cap, excess, flow, u, v, neighbourhood)
            if excess[v] > 0 and v != t:
                new_overflowing.append(v)
    return new_overflowing


def push(cap, excess, flow, u, v, neighbourhood):
    push_amount = min(excess[u], cap[(u, v)])
    flow[(u, v)] = flow.get((u, v), 0) + push_amount
    flow[(v, u)] = flow.get((v, u), 0) - push_amount

    excess[u] -= push_amount
    excess[v] += push_amount

    cap[(u, v)] = cap[(u, v)] - push_amount
    if cap[(u, v)] == 0:
        neighbourhood[u].remove(v)
    cap[(v, u)] = cap.get((v, u), 0) + push_amount
    if cap[(v, u)] > 0 and (u not in neighbourhood[v]):
        neighbourhood[v].append(u)


def relabel(u, height, neighbourhood):
    u_neighbourhood = [b for b in neighbourhood[u]]
    if len(u_neighbourhood) == 0:
        print("relabel useless node. buggy")
        return
    height[u] = 1 + min([height[v] for v in u_neighbourhood])


def init_preflow(V, E, neighbourhood, cap, s, t):
    excess = {v: 0 for v in V}
    flow = {e: 0 for e in E}

    overflowing = []
    for v in neighbourhood[s]:
        flow[(s, v)] = cap[(s, v)]
        excess[v] = cap[(s, v)]
        if v != t:
            overflowing.append(v)
        excess[s] -= cap[(s, v)]
        cap[(v, s)] = cap[(s, v)]
        if s not in neighbourhood[v]:
            neighbourhood[v].append(s)
        cap[(s, v)] = 0
    neighbourhood[s] = []

    return flow, excess, overflowing


def get_neighbourhood(E, V):
    neighbourhood = {v: [] for v in V}
    for u, v in E:
        neighbourhood[u].append(v)
    return neighbourhood

import time
# def test():
push_label_time = 0
networkx_time = 0
for _ in range(100):
    N = 11
    V = [str(x) for x in range(N+1)]
    E = [(str(random.randint(0, N)), str(random.randint(0, N))) for i in range(N * 10)]
    E = list(set(E))
    E = [x for x in E if x[0] != x[1]]
    neighbourhood = get_neighbourhood(E, V)
    cap_orig = {e: random.randint(1, 10) for e in E}
    cap = cap_orig.copy()
    a = time.time()
    my_flow_val, my_flow_dict = push_relabel(V, E, neighbourhood, cap, s="1", t=str(N))
    b = time.time()
    push_label_time += (b - a)

    from networkx.algorithms.flow import maximum_flow
    from networkx import DiGraph
    G=DiGraph()
    for u,v in E:
        G.add_edge(u, v, capacity=cap_orig[(u, v)])
    c=time.time()
    flow_val, flow_dict = maximum_flow(G, _s="1", _t=str(N))
    d=time.time()
    networkx_time += (d-c)
    if flow_val != my_flow_val:
        print(flow_val)
        cap = cap_orig.copy()
        a = time.time()
        my_flow_val, my_flow_dict = push_relabel(V, E, neighbourhood, cap,
                                                 s="1", t=str(N))
        raise ValueError("networkx and push label dont have the same result")

print(f"push relabel time: {push_label_time}")
print(f"networkx_time :{networkx_time}")
# push relabel is faster until N=11, for higher N the difference in runtime
# complexity in the number of edges shows. CLRS says push relabel is O(V^2E)
# networkx claims to have a O(V^2*sqrt(E)) implementation