"""
Sorted — AI Search & Pathfinding Algorithms
===========================================
Implements the AI curriculum search algorithms:
- Depth-First Search (DFS with Stack)
- Breadth-First Search (BFS with Queue)
- Greedy Best-First Search (Priority Queue with h(n))
- A* Search (Priority Queue with f(n) = g(n) + h(n))
- Weighted A* Search (Priority Queue with f(n) = g(n) + w * h(n))
- AI Search Comparison (Comparative evaluation on identical graph/grid)
"""

import heapq
from typing import List, Dict, Any, Tuple, Optional
from .base import Algorithm
from .steps import ExecutionTrace


DEFAULT_GRID_GW = 14
DEFAULT_GRID_GH = 8


def get_default_grid() -> Tuple[int, int, int, int, List[int]]:
    gw, gh = DEFAULT_GRID_GW, DEFAULT_GRID_GH
    start = 0
    goal = gw * gh - 1
    # Simple default walls layout
    walls = [0] * (gw * gh)
    for y in range(1, gh - 1):
        walls[y * gw + 4] = 1
        walls[(gh - 1 - y) * gw + 9] = 1
    return gw, gh, start, goal, walls


def manhattan_distance(idx1: int, idx2: int, gw: int) -> float:
    x1, y1 = idx1 % gw, idx1 // gw
    x2, y2 = idx2 % gw, idx2 // gw
    return abs(x1 - x2) + abs(y1 - y2)


class DepthFirstSearch(Algorithm):
    """Depth-First Search (DFS) using Stack."""

    @property
    def name(self) -> str:
        return "Depth-First Search (DFS)"

    @property
    def category(self) -> str:
        return "AI Search"

    @property
    def description(self) -> str:
        return "Explores graph or grid nodes by plunging as deep as possible along each branch before backtracking using a Stack."

    @property
    def time_complexity_best(self) -> str:
        return "O(1)"

    @property
    def time_complexity_average(self) -> str:
        return "O(V + E)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(V + E)"

    @property
    def space_complexity(self) -> str:
        return "O(V)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def dfs(grid, start, goal):",
            "    stack = [start]",
            "    visited = set()",
            "    parent = {}",
            "    while stack:",
            "        node = stack.pop()",
            "        if node == goal: return reconstruct_path(parent, goal)",
            "        if node in visited: continue",
            "        visited.add(node)",
            "        for nb in neighbors(node):",
            "            if nb not in visited:",
            "                parent[nb] = node; stack.append(nb)"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        gw, gh, start, goal, walls = get_default_grid()
        trace = ExecutionTrace(self.name, walls)
        trace.begin()

        stack = [start]
        visited = set()
        parent = {}
        max_stack_size = 1

        trace.add_step(
            operation="INIT",
            array_state=walls,
            explanation=f"Starting DFS from Start cell {start} to Goal cell {goal}. Stack initialized with [{start}].",
            code_line=2,
            code_highlight="stack = [start]",
            variables={"start": start, "goal": goal, "stack": list(stack), "visited_count": 0}
        )

        found = False
        while stack:
            node = stack.pop()
            if node in visited:
                continue

            visited.add(node)
            trace.increment_comparisons()

            trace.add_step(
                operation="DFS_POP",
                array_state=walls,
                active_indices=[node],
                explanation=f"Popped node ({node % gw}, {node // gw}) from stack. Stack size = {len(stack)}.",
                code_line=6,
                code_highlight="node = stack.pop()",
                variables={"current": node, "stack": list(stack), "visited_count": len(visited), "max_frontier": max_stack_size}
            )

            if node == goal:
                found = True
                break

            # Neighbors: right, down, left, up
            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = (node % gw) + dx, (node // gw) + dy
                nb = ny * gw + nx
                if 0 <= nx < gw and 0 <= ny < gh and not walls[nb] and nb not in visited:
                    parent[nb] = node
                    stack.append(nb)
                    if len(stack) > max_stack_size:
                        max_stack_size = len(stack)

            trace.add_step(
                operation="DFS_PUSH",
                array_state=walls,
                active_indices=[node],
                explanation=f"Inspected neighbors of ({node % gw}, {node // gw}). Updated stack size = {len(stack)}.",
                code_line=12,
                code_highlight="stack.append(nb)",
                variables={"current": node, "stack": list(stack), "visited_count": len(visited)}
            )

        path = []
        if found:
            curr = goal
            while curr in parent or curr == start:
                path.append(curr)
                if curr == start:
                    break
                curr = parent[curr]
            path.reverse()

        trace.add_step(
            operation="COMPLETE",
            array_state=walls,
            active_indices=path,
            explanation=f"DFS search finished. Goal {'reached! Path length = ' + str(len(path) - 1) if found else 'unreachable.'}",
            code_line=7,
            variables={"found": found, "path_length": len(path) - 1 if found else 0, "nodes_explored": len(visited), "max_stack_size": max_stack_size}
        )
        trace.end({"path": path, "visited": list(visited), "nodes_explored": len(visited)})
        trace.finalize()
        return trace


class BreadthFirstSearch(Algorithm):
    """Breadth-First Search (BFS) using Queue."""

    @property
    def name(self) -> str:
        return "Breadth-First Search (BFS)"

    @property
    def category(self) -> str:
        return "AI Search"

    @property
    def description(self) -> str:
        return "Explores graph or grid level-by-level using a Queue to guarantee the shortest path on unweighted graphs."

    @property
    def time_complexity_best(self) -> str:
        return "O(1)"

    @property
    def time_complexity_average(self) -> str:
        return "O(V + E)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(V + E)"

    @property
    def space_complexity(self) -> str:
        return "O(V)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def bfs(grid, start, goal):",
            "    queue = [start]",
            "    visited = {start}",
            "    parent = {}",
            "    while queue:",
            "        node = queue.pop(0)",
            "        if node == goal: return reconstruct_path(parent, goal)",
            "        for nb in neighbors(node):",
            "            if nb not in visited:",
            "                visited.add(nb); parent[nb] = node; queue.append(nb)"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        gw, gh, start, goal, walls = get_default_grid()
        trace = ExecutionTrace(self.name, walls)
        trace.begin()

        queue = [start]
        visited = {start}
        parent = {}
        max_queue_size = 1

        trace.add_step(
            operation="INIT",
            array_state=walls,
            explanation=f"Starting BFS from Start cell {start} to Goal cell {goal}. Queue initialized with [{start}].",
            code_line=2,
            code_highlight="queue = [start]",
            variables={"start": start, "goal": goal, "queue": list(queue), "visited_count": len(visited)}
        )

        found = False
        while queue:
            node = queue.pop(0)
            trace.increment_comparisons()

            trace.add_step(
                operation="BFS_DEQUEUE",
                array_state=walls,
                active_indices=[node],
                explanation=f"Dequeued cell ({node % gw}, {node // gw}). Remaining queue size = {len(queue)}.",
                code_line=6,
                code_highlight="node = queue.pop(0)",
                variables={"current": node, "queue": list(queue), "visited_count": len(visited)}
            )

            if node == goal:
                found = True
                break

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = (node % gw) + dx, (node // gw) + dy
                nb = ny * gw + nx
                if 0 <= nx < gw and 0 <= ny < gh and not walls[nb] and nb not in visited:
                    visited.add(nb)
                    parent[nb] = node
                    queue.append(nb)
                    if len(queue) > max_queue_size:
                        max_queue_size = len(queue)

            trace.add_step(
                operation="BFS_ENQUEUE",
                array_state=walls,
                active_indices=[node],
                explanation=f"Enqueued unvisited neighbors of ({node % gw}, {node // gw}). Updated queue size = {len(queue)}.",
                code_line=10,
                code_highlight="visited.add(nb); parent[nb] = node; queue.append(nb)",
                variables={"current": node, "queue": list(queue), "visited_count": len(visited)}
            )

        path = []
        if found:
            curr = goal
            while curr in parent or curr == start:
                path.append(curr)
                if curr == start:
                    break
                curr = parent[curr]
            path.reverse()

        trace.add_step(
            operation="COMPLETE",
            array_state=walls,
            active_indices=path,
            explanation=f"BFS complete. Shortest path found with length {len(path) - 1 if found else 0}.",
            code_line=7,
            variables={"found": found, "path_length": len(path) - 1 if found else 0, "nodes_explored": len(visited), "max_queue_size": max_queue_size}
        )
        trace.end({"path": path, "visited": list(visited), "nodes_explored": len(visited)})
        trace.finalize()
        return trace


class GreedyBestFirstSearch(Algorithm):
    """Greedy Best-First Search using Heuristic h(n)."""

    @property
    def name(self) -> str:
        return "Greedy Best-First Search"

    @property
    def category(self) -> str:
        return "AI Search"

    @property
    def description(self) -> str:
        return "Expands node that appears closest to goal using heuristic h(n). Fast but not guaranteed to find shortest path."

    @property
    def time_complexity_best(self) -> str:
        return "O(1)"

    @property
    def time_complexity_average(self) -> str:
        return "O(b^m)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(b^m)"

    @property
    def space_complexity(self) -> str:
        return "O(b^m)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def greedy_best_first(grid, start, goal):",
            "    # Greedy Best-First Search chooses the node that appears closest to goal.",
            "    open_pq = [(h(start), start)]",
            "    visited = {start}",
            "    parent = {}",
            "    while open_pq:",
            "        h_val, node = heapq.heappop(open_pq)",
            "        if node == goal: return reconstruct_path(parent, goal)",
            "        for nb in neighbors(node):",
            "            if nb not in visited:",
            "                visited.add(nb); parent[nb] = node; heapq.heappush(open_pq, (h(nb), nb))"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        gw, gh, start, goal, walls = get_default_grid()
        trace = ExecutionTrace(self.name, walls)
        trace.begin()

        def h(idx: int) -> float:
            return manhattan_distance(idx, goal, gw)

        open_pq = [(h(start), start)]
        visited = {start}
        parent = {}

        trace.add_step(
            operation="INIT",
            array_state=walls,
            explanation=f"Starting Greedy Best-First Search. Heuristic h(start) = {h(start):.1f}. Note: Greedy Best-First Search chooses the node that appears closest to the goal. It does not consider the cost already spent.",
            code_line=3,
            code_highlight="open_pq = [(h(start), start)]",
            variables={"start": start, "goal": goal, "h_start": h(start)}
        )

        found = False
        while open_pq:
            h_val, node = heapq.heappop(open_pq)
            trace.increment_comparisons()

            trace.add_step(
                operation="GREEDY_EXPAND",
                array_state=walls,
                active_indices=[node],
                explanation=f"Expanded node ({node % gw}, {node // gw}) with lowest estimated heuristic h(n) = {h_val:.1f}.",
                code_line=7,
                code_highlight="h_val, node = heapq.heappop(open_pq)",
                variables={"current": node, "h_val": h_val, "open_size": len(open_pq), "visited_count": len(visited)}
            )

            if node == goal:
                found = True
                break

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = (node % gw) + dx, (node // gw) + dy
                nb = ny * gw + nx
                if 0 <= nx < gw and 0 <= ny < gh and not walls[nb] and nb not in visited:
                    visited.add(nb)
                    parent[nb] = node
                    heapq.heappush(open_pq, (h(nb), nb))

            trace.add_step(
                operation="GREEDY_ENQUEUE",
                array_state=walls,
                active_indices=[node],
                explanation=f"Evaluated neighbors of ({node % gw}, {node // gw}) and enqueued into priority queue by h(n).",
                code_line=10,
                code_highlight="heapq.heappush(open_pq, (h(nb), nb))",
                variables={"current": node, "open_size": len(open_pq), "visited_count": len(visited)}
            )

        path = []
        if found:
            curr = goal
            while curr in parent or curr == start:
                path.append(curr)
                if curr == start:
                    break
                curr = parent[curr]
            path.reverse()

        trace.add_step(
            operation="COMPLETE",
            array_state=walls,
            active_indices=path,
            explanation=f"Greedy Best-First Search complete. Path length = {len(path) - 1 if found else 0}.",
            code_line=8,
            variables={"found": found, "path_length": len(path) - 1 if found else 0, "nodes_explored": len(visited)}
        )
        trace.end({"path": path, "visited": list(visited), "nodes_explored": len(visited)})
        trace.finalize()
        return trace


class AStarSearch(Algorithm):
    """Standard A* Search using f(n) = g(n) + h(n)."""

    @property
    def name(self) -> str:
        return "A* Search"

    @property
    def category(self) -> str:
        return "AI Search"

    @property
    def description(self) -> str:
        return "Informed search algorithm expanding nodes with minimum total estimated cost f(n) = g(n) + h(n)."

    @property
    def time_complexity_best(self) -> str:
        return "O(1)"

    @property
    def time_complexity_average(self) -> str:
        return "O(b^d)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(b^d)"

    @property
    def space_complexity(self) -> str:
        return "O(b^d)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def a_star(grid, start, goal):",
            "    # f(n) = g(n) + h(n)",
            "    open_pq = [(h(start), 0, start)]  # (f, g, node)",
            "    g_score = {start: 0}",
            "    parent = {}",
            "    closed_set = set()",
            "    while open_pq:",
            "        f_val, g_val, node = heapq.heappop(open_pq)",
            "        if node == goal: return reconstruct_path(parent, goal)",
            "        closed_set.add(node)",
            "        for nb in neighbors(node):",
            "            tentative_g = g_val + 1",
            "            if tentative_g < g_score.get(nb, inf):",
            "                g_score[nb] = tentative_g; parent[nb] = node",
            "                heapq.heappush(open_pq, (tentative_g + h(nb), tentative_g, nb))"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        gw, gh, start, goal, walls = get_default_grid()
        trace = ExecutionTrace(self.name, walls)
        trace.begin()

        def h(idx: int) -> float:
            return manhattan_distance(idx, goal, gw)

        open_pq = [(h(start), 0, start)]
        g_score = {start: 0}
        parent = {}
        closed_set = set()

        trace.add_step(
            operation="INIT",
            array_state=walls,
            explanation=f"Starting A* Search. Start node g=0, h={h(start):.1f}, f={h(start):.1f}.",
            code_line=3,
            code_highlight="open_pq = [(h(start), 0, start)]",
            variables={"start": start, "goal": goal, "g": 0, "h": h(start), "f": h(start)}
        )

        found = False
        while open_pq:
            f_val, g_val, node = heapq.heappop(open_pq)
            if node in closed_set:
                continue

            closed_set.add(node)
            trace.increment_comparisons()

            trace.add_step(
                operation="ASTAR_EXPAND",
                array_state=walls,
                active_indices=[node],
                explanation=f"Expanded cell ({node % gw}, {node // gw}) with lowest f(n) = g({g_val}) + h({f_val - g_val:.1f}) = {f_val:.1f}.",
                code_line=8,
                code_highlight="f_val, g_val, node = heapq.heappop(open_pq)",
                variables={"current": node, "g": g_val, "h": round(f_val - g_val, 1), "f": round(f_val, 1), "open_size": len(open_pq), "closed_size": len(closed_set)}
            )

            if node == goal:
                found = True
                break

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = (node % gw) + dx, (node // gw) + dy
                nb = ny * gw + nx
                if 0 <= nx < gw and 0 <= ny < gh and not walls[nb] and nb not in closed_set:
                    tentative_g = g_val + 1
                    if tentative_g < g_score.get(nb, float('inf')):
                        g_score[nb] = tentative_g
                        parent[nb] = node
                        f_nb = tentative_g + h(nb)
                        heapq.heappush(open_pq, (f_nb, tentative_g, nb))

            trace.add_step(
                operation="ASTAR_UPDATE",
                array_state=walls,
                active_indices=[node],
                explanation=f"Evaluated neighbors of ({node % gw}, {node // gw}). Open set size: {len(open_pq)}.",
                code_line=15,
                code_highlight="heapq.heappush(open_pq, (tentative_g + h(nb), tentative_g, nb))",
                variables={"current": node, "open_size": len(open_pq), "closed_size": len(closed_set)}
            )

        path = []
        if found:
            curr = goal
            while curr in parent or curr == start:
                path.append(curr)
                if curr == start:
                    break
                curr = parent[curr]
            path.reverse()

        trace.add_step(
            operation="COMPLETE",
            array_state=walls,
            active_indices=path,
            explanation=f"A* Search complete. Optimal path found with cost = {len(path) - 1 if found else 0}.",
            code_line=9,
            variables={"found": found, "path_cost": len(path) - 1 if found else 0, "nodes_explored": len(closed_set)}
        )
        trace.end({"path": path, "visited": list(closed_set), "nodes_explored": len(closed_set)})
        trace.finalize()
        return trace


class WeightedAStarSearch(Algorithm):
    """Weighted A* Search using f(n) = g(n) + w * h(n)."""

    @property
    def name(self) -> str:
        return "Weighted A*"

    @property
    def category(self) -> str:
        return "AI Search"

    @property
    def description(self) -> str:
        return "Variant of A* using weighted heuristic f(n) = g(n) + w * h(n) to balance search speed vs path optimality."

    @property
    def time_complexity_best(self) -> str:
        return "O(1)"

    @property
    def time_complexity_average(self) -> str:
        return "O(b^d)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(b^d)"

    @property
    def space_complexity(self) -> str:
        return "O(b^d)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def weighted_a_star(grid, start, goal, weight=1.5):",
            "    # f(n) = g(n) + w * h(n)",
            "    open_pq = [(weight * h(start), 0, start)]",
            "    g_score = {start: 0}",
            "    parent = {}",
            "    closed_set = set()",
            "    while open_pq:",
            "        f_val, g_val, node = heapq.heappop(open_pq)",
            "        if node == goal: return reconstruct_path(parent, goal)",
            "        closed_set.add(node)",
            "        for nb in neighbors(node):",
            "            tentative_g = g_val + 1",
            "            if tentative_g < g_score.get(nb, inf):",
            "                g_score[nb] = tentative_g; parent[nb] = node",
            "                heapq.heappush(open_pq, (tentative_g + weight * h(nb), tentative_g, nb))"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        w = kwargs.get("weight", 1.5)
        try:
            w = float(w)
        except (ValueError, TypeError):
            w = 1.5

        gw, gh, start, goal, walls = get_default_grid()
        trace = ExecutionTrace(self.name, walls)
        trace.begin()

        def h(idx: int) -> float:
            return manhattan_distance(idx, goal, gw)

        open_pq = [(w * h(start), 0, start)]
        g_score = {start: 0}
        parent = {}
        closed_set = set()

        trace.add_step(
            operation="INIT",
            array_state=walls,
            explanation=f"Starting Weighted A* Search with weight w = {w:.2f}. Initial f(n) = g(0) + {w:.2f}*h({h(start):.1f}) = {w*h(start):.1f}.",
            code_line=3,
            code_highlight=f"open_pq = [({w:.2f} * h(start), 0, start)]",
            variables={"weight": w, "start": start, "goal": goal, "g": 0, "h": h(start), "weighted_h": round(w * h(start), 2), "f": round(w * h(start), 2)}
        )

        found = False
        while open_pq:
            f_val, g_val, node = heapq.heappop(open_pq)
            if node in closed_set:
                continue

            closed_set.add(node)
            trace.increment_comparisons()

            h_raw = h(node)
            trace.add_step(
                operation="WEIGHTED_ASTAR_EXPAND",
                array_state=walls,
                active_indices=[node],
                explanation=f"Weighted A* (w={w:.1f}) expanded cell ({node % gw}, {node // gw}): g={g_val}, h={h_raw:.1f}, w*h={w*h_raw:.1f}, f={f_val:.1f}.",
                code_line=8,
                code_highlight="f_val, g_val, node = heapq.heappop(open_pq)",
                variables={"weight": w, "current": node, "g": g_val, "h": round(h_raw, 1), "weighted_h": round(w * h_raw, 1), "f": round(f_val, 1), "closed_size": len(closed_set)}
            )

            if node == goal:
                found = True
                break

            for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                nx, ny = (node % gw) + dx, (node // gw) + dy
                nb = ny * gw + nx
                if 0 <= nx < gw and 0 <= ny < gh and not walls[nb] and nb not in closed_set:
                    tentative_g = g_val + 1
                    if tentative_g < g_score.get(nb, float('inf')):
                        g_score[nb] = tentative_g
                        parent[nb] = node
                        f_nb = tentative_g + w * h(nb)
                        heapq.heappush(open_pq, (f_nb, tentative_g, nb))

            trace.add_step(
                operation="WEIGHTED_ASTAR_UPDATE",
                array_state=walls,
                active_indices=[node],
                explanation=f"Evaluated neighbors with weight w={w:.1f}. Open set size: {len(open_pq)}.",
                code_line=15,
                code_highlight="heapq.heappush(open_pq, (tentative_g + weight * h(nb), tentative_g, nb))",
                variables={"weight": w, "current": node, "open_size": len(open_pq), "closed_size": len(closed_set)}
            )

        path = []
        if found:
            curr = goal
            while curr in parent or curr == start:
                path.append(curr)
                if curr == start:
                    break
                curr = parent[curr]
            path.reverse()

        trace.add_step(
            operation="COMPLETE",
            array_state=walls,
            active_indices=path,
            explanation=f"Weighted A* (w={w:.1f}) search complete. Path length = {len(path) - 1 if found else 0}, Nodes explored = {len(closed_set)}.",
            code_line=9,
            variables={"weight": w, "found": found, "path_length": len(path) - 1 if found else 0, "nodes_explored": len(closed_set)}
        )
        trace.end({"path": path, "visited": list(closed_set), "nodes_explored": len(closed_set), "weight": w})
        trace.finalize()
        return trace


class AISearchComparison(Algorithm):
    """AI Search Comparative Workbench."""

    @property
    def name(self) -> str:
        return "AI Search Comparison"

    @property
    def category(self) -> str:
        return "AI Search"

    @property
    def description(self) -> str:
        return "Evaluates DFS, BFS, Greedy Best-First, A*, and Weighted A* on an identical grid/graph to compare nodes explored, path cost, and frontier size."

    @property
    def time_complexity_best(self) -> str:
        return "O(V + E)"

    @property
    def time_complexity_average(self) -> str:
        return "O(V + E)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(V + E)"

    @property
    def space_complexity(self) -> str:
        return "O(V)"

    @property
    def source_code(self) -> List[str]:
        return [
            "# AI Search Benchmark Arena",
            "for algo in [DFS, BFS, Greedy, A*, WeightedA*]:",
            "    trace = algo.execute(grid, start, goal)",
            "    record_metrics(nodes_explored, path_length, execution_steps)"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        dfs = DepthFirstSearch().execute(data, **kwargs)
        bfs = BreadthFirstSearch().execute(data, **kwargs)
        greedy = GreedyBestFirstSearch().execute(data, **kwargs)
        astar = AStarSearch().execute(data, **kwargs)
        w_astar = WeightedAStarSearch().execute(data, weight=1.5, **kwargs)

        summary_results = [
            {"algorithm": "DFS", "nodes_explored": dfs.result.get("nodes_explored"), "path_length": len(dfs.result.get("path", [])) - 1, "steps": dfs.total_steps},
            {"algorithm": "BFS", "nodes_explored": bfs.result.get("nodes_explored"), "path_length": len(bfs.result.get("path", [])) - 1, "steps": bfs.total_steps},
            {"algorithm": "Greedy Best-First", "nodes_explored": greedy.result.get("nodes_explored"), "path_length": len(greedy.result.get("path", [])) - 1, "steps": greedy.total_steps},
            {"algorithm": "A*", "nodes_explored": astar.result.get("nodes_explored"), "path_length": len(astar.result.get("path", [])) - 1, "steps": astar.total_steps},
            {"algorithm": "Weighted A* (w=1.5)", "nodes_explored": w_astar.result.get("nodes_explored"), "path_length": len(w_astar.result.get("path", [])) - 1, "steps": w_astar.total_steps},
        ]

        trace = ExecutionTrace(self.name, get_default_grid()[4])
        trace.begin()
        trace.add_step(
            operation="COMPLETE",
            array_state=get_default_grid()[4],
            explanation="AI Search comparative analysis on identical grid complete.",
            variables={"comparison_table": summary_results}
        )
        trace.end(summary_results)
        trace.finalize()
        return trace
