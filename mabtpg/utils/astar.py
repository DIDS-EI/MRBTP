"""A* path planner used by the MiniGrid behavior-library actions.

The MiniGrid action / condition nodes import two helpers from this
module:

    astar(grid, start, goal)
        Plan a 4-connected path on a MiniGrid ``Grid``.  The result is a
        ``list`` of unit direction vectors ``(dx, dy)`` -- one per step
        from ``start`` to ``goal`` -- so that callers can do::

            path = astar(env.grid, start=agent.position, goal=target)
            if path is None:
                ...                       # unreachable
            elif path == []:
                ...                       # already at goal
            else:
                next_dir = path[0]        # (dx, dy), pop after a forward move

        Each element matches one of the four vectors in
        ``minigrid.core.constants.DIR_TO_VEC`` so it can be fed straight
        into ``get_direction_index`` / ``turn_to`` without any further
        conversion.

    is_near(pos_a, pos_b)
        Return ``True`` iff the two grid cells are 4-neighbour adjacent
        (Manhattan distance == 1).
"""

from __future__ import annotations

import heapq
from typing import Dict, List, Optional, Tuple

import numpy as np


Position = Tuple[int, int]
Direction = Tuple[int, int]

# 4-connected moves.  Order is irrelevant for correctness but is kept
# consistent with ``minigrid.core.constants.DIR_TO_VEC``
# (right, down, left, up) for readability.
_DIRECTIONS: Tuple[Direction, ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))


def _to_tuple(pos) -> Position:
    """Coerce ``np.ndarray`` / ``list`` / ``tuple`` to ``(int, int)``."""
    if isinstance(pos, np.ndarray):
        return int(pos[0]), int(pos[1])
    return int(pos[0]), int(pos[1])


def is_near(pos_a, pos_b) -> bool:
    """Return ``True`` iff ``pos_a`` and ``pos_b`` are 4-neighbour adjacent.

    ``None`` inputs return ``False`` so callers can use this defensively
    without an extra null-check.
    """
    if pos_a is None or pos_b is None:
        return False
    ax, ay = _to_tuple(pos_a)
    bx, by = _to_tuple(pos_b)
    return abs(ax - bx) + abs(ay - by) == 1


def _is_walkable(grid, x: int, y: int) -> bool:
    """Whether the path planner may route through cell ``(x, y)``.

    Policy (per project requirement): only **walls** and **closed /
    locked doors** block the planner.  Every other cell -- empty floor,
    open doors, goal markers, lava, picked-up-able items such as keys,
    balls and boxes, etc. -- is treated as passable.  The action layer
    is responsible for handling whatever is on the cell at execution
    time (e.g. picking it up, stepping around it, replanning).
    """
    if x < 0 or y < 0 or x >= grid.width or y >= grid.height:
        return False
    cell = grid.get(x, y)
    if cell is None:
        return True

    # Type-name based check keeps this module independent from the
    # exact import path of MiniGrid's world-object classes.
    type_name = getattr(cell, "type", None) or type(cell).__name__.lower()

    if type_name == "wall":
        return False

    if type_name == "door":
        # A door is passable iff it is currently open.  ``is_locked``
        # implies ``is_open == False`` in MiniGrid, so checking
        # ``is_open`` alone is sufficient, but we also tolerate doors
        # that don't expose the attribute.
        return bool(getattr(cell, "is_open", False))

    # Anything else (key, ball, box, goal, floor, lava, ...): passable.
    return True


def astar(grid, start, goal) -> Optional[List[Direction]]:
    """A* search on a MiniGrid ``Grid``.

    Parameters
    ----------
    grid :
        A MiniGrid ``Grid`` (must expose ``width``, ``height`` and
        ``get(x, y)``).
    start, goal : (int, int)-like
        Source and destination positions.  Numpy arrays / lists / tuples
        are all accepted.

    Returns
    -------
    list[(dx, dy)] | None
        List of unit-vector moves leading from ``start`` to ``goal``.
        ``[]`` is returned when ``start == goal``; ``None`` when the
        goal is unreachable.

    Notes
    -----
    The goal cell itself is treated as walkable even when it is
    occupied (e.g. a key on the floor): the higher-level action node
    decides whether to stop one step short and face the goal, or step
    onto it.  This keeps the planner usable for both ``GoTo``
    (target = an object cell) and ``PutNear`` (target = an empty cell).
    """
    start_t = _to_tuple(start)
    goal_t = _to_tuple(goal)

    if start_t == goal_t:
        return []

    width = grid.width
    height = grid.height
    if not (0 <= goal_t[0] < width and 0 <= goal_t[1] < height):
        return None
    if not (0 <= start_t[0] < width and 0 <= start_t[1] < height):
        return None

    def heuristic(p: Position) -> int:
        return abs(p[0] - goal_t[0]) + abs(p[1] - goal_t[1])

    # Priority queue of (f_score, tie_breaker, position).  The integer
    # tie-breaker keeps tuples comparable when f_scores collide.
    open_heap: list = []
    counter = 0
    heapq.heappush(open_heap, (heuristic(start_t), counter, start_t))

    came_from: Dict[Position, Tuple[Position, Direction]] = {}
    g_score: Dict[Position, int] = {start_t: 0}
    closed: set = set()

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if current in closed:
            continue
        closed.add(current)

        if current == goal_t:
            # Reconstruct the sequence of move vectors.
            directions: List[Direction] = []
            node = current
            while node in came_from:
                prev, direction = came_from[node]
                directions.append(direction)
                node = prev
            directions.reverse()
            return directions

        cx, cy = current
        cur_g = g_score[current]
        for dx, dy in _DIRECTIONS:
            nx, ny = cx + dx, cy + dy
            neighbour: Position = (nx, ny)

            if neighbour == goal_t:
                # Always allow stepping onto the goal cell, even when it
                # is occupied.
                if not (0 <= nx < width and 0 <= ny < height):
                    continue
            elif not _is_walkable(grid, nx, ny):
                continue

            tentative_g = cur_g + 1
            if tentative_g < g_score.get(neighbour, 1 << 30):
                came_from[neighbour] = (current, (dx, dy))
                g_score[neighbour] = tentative_g
                f_score = tentative_g + heuristic(neighbour)
                counter += 1
                heapq.heappush(open_heap, (f_score, counter, neighbour))

    return None


__all__ = ["astar", "is_near"]
