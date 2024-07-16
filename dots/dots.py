import numpy as np
import matplotlib.pyplot as plt


def transform_polygon(polygon, scale, orientation, position):
    # original be centered at origin ?

    # Scale the polygon
    scaled_polygon = polygon * scale

    # Rotate the polygon
    rotation_matrix = np.array([
        [np.cos(orientation), -np.sin(orientation)],
        [np.sin(orientation), np.cos(orientation)]
    ])
    rotated_polygon = np.dot(scaled_polygon, rotation_matrix)

    # Translate the polygon
    translated_polygon = rotated_polygon + position

    return translated_polygon


def gen_base_polygon(n_sides):
    # Generate the vertices of a regular polygon centered at the origin
    angles = np.linspace(0, 2 * np.pi, n_sides, endpoint=False)
    polygon = np.column_stack((np.cos(angles), np.sin(angles)))
    polygon = polygon * 0.25 # scale to 0.25
    return polygon #(n_sides, 2)


def gen_n_polygons(n_sides, n): # return (n, n_sides, 2)
    base_polygon = gen_base_polygon(n_sides)
    polygons = []

    min_scale, max_scale = 0.4, 1

    # shift to positive unit space
    min_pos = np.array([0.25, 0.25])
    max_pos = np.array([0.75, 0.75])

    for _ in range(n):
        scale = np.random.uniform(min_scale, max_scale)
        orientation = np.random.uniform(0, 2 * np.pi)
        position = np.random.uniform(min_pos, max_pos) 
        transformed_polygon = transform_polygon(base_polygon, scale, orientation, position)
        
        polygons.append(transformed_polygon)

    return np.array(polygons)

def plot_polygons(polygon_list, ax): #list of (n_sides, 2)
    # n_sides - not fixed
    # plot in the passed axis
    # fig, ax = plt.subplots()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    for p in polygon_list:
        ax.fill(p[:, 0], p[:, 1], alpha=0.5)
    # plt.show()




def get_edges(polygon):
    # polygon: (n_sides, 2) ndarray
    # get list of (start, end, edge_length) 
    # also perimeter
    edges = []
    perimeter = 0
    num_vertices = len(polygon)
    for i in range(num_vertices):
        start = polygon[i]
        end = polygon[(i + 1) % num_vertices]
        edge_length = np.linalg.norm(end - start)
        perimeter += edge_length
        edges.append((start, end, edge_length))
    return edges, perimeter


def sample_dots(polygon, n_dots):
    # sample n dots from given polygon edges

    # include all vertices
    dots = list(polygon) # list of ndarray (2,)
    n_xtra_dots = n_dots - len(dots)

    edges, perimeter = get_edges(polygon)

    # Distribute additional points along the segments
    for edge in edges:
        start, end, edge_length = edge
        num_points_on_edge = int(np.round(n_xtra_dots * (edge_length / perimeter)))
        for j in range(1, num_points_on_edge + 1):
            t = j / (num_points_on_edge + 1)
            new_point = (1 - t) * np.array(start) + t * np.array(end)
            dots.append(new_point)
    
    # if required count is not reached
    # pick random edge, pick random fraction(between 0,1) and add point
    while len(dots) < n_dots:
        edge = edges[np.random.randint(len(edges))]
        start, end, edge_length = edge
        t = np.random.rand()
        new_point = (1 - t) * np.array(start) + t * np.array(end)
        dots.append(new_point)
    
    # Ensure exactly N points by potentially trimming excess
    while len(dots) > n_dots:
        dots.pop()
    
    return np.array(dots) 


def plot_dots(dots, ax):
    # dots: (n_dots, 2) ndarray
    # plot in the passed axis
    ax.scatter(dots[:, 0], dots[:, 1], color='blue')

    # Label each point with its index
    for i, point in enumerate(dots):
        ax.text(point[0], point[1], str(i), fontsize=12, ha='right')

    # plt.show()

# test for dots
# for p in polygon_list:
#     d = sample_dots(p,12)
#     plot_dots(d, ax)
    


def gen_chains(order, res, n, in_order=False):
    # order = n_sides of polygon
    # get n polygons, sample dots from each with resolution=res

    base_polygon = gen_base_polygon(order)
    chains = []

    min_scale, max_scale = 0.4, 1

    # shift to positive unit space
    min_pos = np.array([0.25, 0.25])
    max_pos = np.array([0.75, 0.75])

    for _ in range(n):
        scale = np.random.uniform(min_scale, max_scale)
        orientation = np.random.uniform(0, 2 * np.pi)
        position = np.random.uniform(min_pos, max_pos) 
        transformed_polygon = transform_polygon(base_polygon, scale, orientation, position)
    
        chain = sample_dots(transformed_polygon, res)
        if in_order:
            chain = order_dots(chain)
        chains.append(chain)

    return np.array(chains) # (n, res, 2)


# given a chain, order the dots in it anti-clockwise
def order_dots(chain):
    # chain: (res, 2) ndarray
    # order in anti-clockwise
    # return (res, 2) ndarray
    # get centroid of the chain
    centroid = np.mean(chain, axis=0)
    angles = np.arctan2(chain[:, 1] - centroid[1], chain[:, 0] - centroid[0])
    sorted_indices = np.argsort(angles)
    return chain[sorted_indices]