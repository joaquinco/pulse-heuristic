def draw_solution(graph, solution, cmap=['orange', 'blue', 'green', 'black'], location_key='pos'):
    import osmnx as ox
    """
    Draw solution obtained by the pulse solver
    """
    # TODO: add references to figure

    def get_xy(graph, n1, n2):
        return list(zip(graph.nodes[n1][location_key], graph.nodes[n2][location_key]))
    
    fig, ax = ox.plot_graph(graph, fig_height=15, show=False, close=False)
    for odpair, data in solution.shortest_paths.items():
        path = data['path']
        for n1, n2 in zip(path[:-1], path[1:]):
            ax.plot(*get_xy(graph, n1, n2), 'r--', linewidth=2)
        
        for edge in solution.modifications[odpair].keys():
            n1, n2, infra = edge
            if infra > 0:
                ax.plot(*get_xy(graph, n1, n2), c=cmap[infra], linewidth=4)
    
        source, target = odpair
        ax.scatter(*graph.nodes[source][location_key], s=100, c='red', zorder=4)
        ax.scatter(*graph.nodes[target][location_key], s=100, c='red', zorder=4)
            
    return fig, ax
