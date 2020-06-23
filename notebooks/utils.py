import numpy as np
import matplotlib.pyplot as plt

def plot_graph(vertices, edges=None, fig=None, ax=None):
    """
    Draw a graph from (N,2) array of vertices with optional edges
    
    Parameters
    ----------
    vertices: ndarray
        (N,2) ndarray of (x,y) positions of N vertices
    
    edges: ndarray (default: None)
        (N,) ndarray of ints for the order of the vertices
        
    fig : plt.figure (default: None)
        Figure to draw the axes/graph onto
    
    ax : plt.axes (default: None)
        Axis to draw the graph onto
    """
    if fig is None:
        fig = plt.figure(figsize=(3,3), dpi=200)
    if ax is None:
        ax = fig.subplots()
        
    if edges is not None:
        vertices_ordered = np.take(vertices, edges, axis=0)
        ax.plot(
            vertices_ordered[:,0],
            vertices_ordered[:,1],
            '-', color='black',
        )
        
    ax.plot(
        vertices[:,0], vertices[:,1], 'o',
        color='#1f78b4', ms=8,
    )
    for idx, vertex in enumerate(vertices):
        ax.annotate(
            r'${}$'.format(idx), xy=(0,0), xytext=vertex[:2],
            ha='center', va='center',
            fontsize=6, color='white',
        )
    
    return fig, ax