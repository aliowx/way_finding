import logging
import heapq
import numpy as np
import math
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app import crud, schemas
from app.core.config import settings


logger = logging.getLogger(__name__)

async def create_super_admin(db: AsyncSession) -> None:
    user = await crud.user.get_by_email(db=db, email=settings.FIRST_SUPERUSER)
    if not user:
        user = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        await crud.user.create(db=db, obj_in=user)


async def get_graph_data(db: AsyncSession) -> tuple[dict, dict]:
    vertices = await crud.vertex.get_multi(db) 
    edges = await crud.edge.get_multi(db)

    graph: dict[int, dict[int, float]] = {vertex.id: {} for vertex in vertices}
    coordinates: dict[int, tuple[int, float]] = {
        vertex.id: (vertex.x, vertex.y) for vertex in vertices
    }

    for edge in edges:
        graph[edge.source_vertex_id][edge.destination_vertex_id] = edge.distance
    return graph, coordinates


def dijkstra(graph: dict[int, dict[int, float]], start_vertex: int):
    queue: list[tuple[int, int]] = [(0, start_vertex)]
    distances: dict[int, float] = {vertex: float("inf") for vertex in graph}
    distances[start_vertex] = 0
    previous_vertices: dict[int, int | None] = {vertex: None for vertex in graph}

    while queue:
        current_distance, current_vertex = heapq.heappop(queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heapq.heappush(queue, (distance, neighbor))
    return distances, previous_vertices


def reconstruct_path(
    destination_vertex: int, previous_vertices: dict[int, int | None]
) -> list[int]:
    path: list[int] = []
    current_vertex = destination_vertex

    while current_vertex is not None:
        path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]

    return path[::-1]


def angle_between_three_points(
    point_a: tuple[float, float],
    point_b: tuple[float, float],
    point_c: tuple[float, float],
) -> tuple[float, str]:

    vector_ab = np.array([point_b[0] - point_a[0], point_b[1] - point_a[1]])
    vector_bc = np.array([point_c[0] - point_b[0], point_c[1] - point_b[1]])

    dot_product = np.dot(vector_ab, vector_bc)
    magnitude_ab = np.linalg.norm(vector_ab)
    magnitude_bc = np.linalg.norm(vector_bc)

    if magnitude_ab == 0 or magnitude_bc == 0:
        return 0.0, "undefined"

    cosine_angle = dot_product / (magnitude_ab * magnitude_bc)
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    cross_product = np.cross(vector_ab, vector_bc)

    tolerance = 1e-2

    if abs(angle - 180) < tolerance or abs(angle) < tolerance:
        return angle, "straight"
    elif cross_product > 0:
        return angle, "left"
    else:
        return angle, "right"


def generate_direction(
    path: list[int],
    coordinates: dict[int, tuple[int, float]],
    graph: dict[int, dict[int, float]],
) -> list[str]:
    directions: list[str] = []

    for i in range(1, len(path) - 1):
        p1 = coordinates[path[i - 1]]
        p2 = coordinates[path[i]]
        p3 = coordinates[path[i + 1]]

        angle, direction = angle_between_three_points(p1, p2, p3)
        distance = graph[path[i - 1]][path[i]]

        directions.append(
            f"From vertex {path[i-1]} walk {distance}m to vertex {path[i]}, turn {direction} by {angle:.2f} degrees."
        )
    return directions

async def init_db(db: AsyncSession) -> None:
    await create_super_admin(db)


async def shortest_path(db: AsyncSession) -> None:
    graph, coordinates = await get_graph_data(db)
    start_vertex, destination_vertex = (1, 8)
    distances, previous_vertices = dijkstra(graph=graph, start_vertex=start_vertex)
    find_path = reconstruct_path(
        destination_vertex=destination_vertex,
        previous_vertices=previous_vertices,
    )
    directions = generate_direction(find_path, coordinates=coordinates, graph=graph)
    print(directions)

if __name__== "__main__":
    asyncio.run(shortest_path(db=AsyncSession))