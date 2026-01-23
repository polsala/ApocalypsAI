/**
 * Implements Dijkstra's algorithm to find the shortest path between two nodes in a graph.
 * @param {Object.<string, Object.<string, number>>} graph - Adjacency list representation of the graph.
 *   Keys are node names, values are objects mapping neighbor node names to edge weights.
 * @param {string} startNode - The starting node.
 * @param {string} endNode - The target node.
 * @returns {{path: string[], distance: number}} - The shortest path as an array of node names and its total distance.
 */
export function findShortestPath(graph, startNode, endNode) {
  const distances = {};
  const previousNodes = {};
  const unvisited = new Set(Object.keys(graph));

  // Initialize distances
  for (const node in graph) {
    distances[node] = Infinity;
  }
  distances[startNode] = 0;

  while (unvisited.size > 0) {
    // Find the unvisited node with the smallest distance
    let currentNode = null;
    for (const node of unvisited) {
      if (currentNode === null || distances[node] < distances[currentNode]) {
        currentNode = node;
      }
    }

    if (currentNode === null || distances[currentNode] === Infinity) {
      break; // No path to remaining unvisited nodes
    }

    unvisited.delete(currentNode);

    if (currentNode === endNode) {
      break; // Found the shortest path to the end node
    }

    for (const neighbor in graph[currentNode]) {
      const distance = graph[currentNode][neighbor];
      const newDistance = distances[currentNode] + distance;

      if (newDistance < distances[neighbor]) {
        distances[neighbor] = newDistance;
        previousNodes[neighbor] = currentNode;
      }
    }
  }

  // Reconstruct path
  const path = [];
  let current = endNode;
  while (current && previousNodes[current] !== undefined) {
    path.unshift(current);
    current = previousNodes[current];
  }
  if (current === startNode) {
    path.unshift(startNode);
  } else if (path.length === 0 && startNode === endNode) {
    // Handle case where start and end are the same and no path was found (e.g., single node graph)
    return { path: [startNode], distance: 0 };
  } else if (path.length === 0 && distances[endNode] === Infinity) {
    // No path found
    return { path: [], distance: Infinity };
  }

  return { path, distance: distances[endNode] };
}
