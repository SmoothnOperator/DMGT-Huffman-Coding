"""
Huffman Tree Graph Visualizer using NetworkX & Matplotlib
Module: src/visualizer.py
Role: Khyathi (Visualization, Report & Presentation)
Discrete Mathematics & Graph Theory - Experiential Learning Project
"""

import os
from typing import Optional
import networkx as nx
import matplotlib.pyplot as plt
from src.huffman import HuffmanNode


class HuffmanVisualizer:
    """
    Renders rooted binary trees with edge labels ('0' and '1') and node weights.
    """

    @classmethod
    def build_networkx_graph(
        cls,
        root: HuffmanNode,
        graph: Optional[nx.DiGraph] = None,
        pos: Optional[dict] = None,
        x: float = 0.0,
        y: float = 0.0,
        layer: float = 1.0,
        parent_id: Optional[int] = None,
        edge_label: str = ""
    ) -> Tuple[nx.DiGraph, dict, dict, dict]:
        """
        Recursively converts a binary tree into a directed NetworkX graph with hierarchical layout.
        """
        if graph is None:
            graph = nx.DiGraph()
            pos = {}

        node_id = root.node_id
        pos[node_id] = (x, y)

        if root.is_leaf():
            display_char = repr(root.char) if root.char in ('\n', ' ', '\t') else root.char
            label = f"{display_char}\n(w={root.freq})"
            node_type = "leaf"
        else:
            label = f"w={root.freq}"
            node_type = "internal"

        graph.add_node(node_id, label=label, type=node_type)

        if parent_id is not None:
            graph.add_edge(parent_id, node_id, label=edge_label)

        # Recursively layout children
        dx = 1.0 / (2 ** layer)
        if root.left:
            cls.build_networkx_graph(
                root.left, graph, pos,
                x=x - dx, y=y - 1.0, layer=layer + 1.0,
                parent_id=node_id, edge_label="0"
            )
        if root.right:
            cls.build_networkx_graph(
                root.right, graph, pos,
                x=x + dx, y=y - 1.0, layer=layer + 1.0,
                parent_id=node_id, edge_label="1"
            )

        labels = nx.get_node_attributes(graph, 'label')
        edge_labels = nx.get_edge_attributes(graph, 'label')
        return graph, pos, labels, edge_labels

    @classmethod
    def plot_tree(
        cls,
        root: HuffmanNode,
        title: str = "Huffman Optimal Prefix Code Tree",
        save_path: Optional[str] = None
    ):
        """Plots the tree with color-coded leaf and internal nodes."""
        graph, pos, labels, edge_labels = cls.build_networkx_graph(root)

        plt.figure(figsize=(14, 8))
        plt.title(title, fontsize=14, fontweight="bold", pad=20)

        # Classify nodes for visual styling
        internal_nodes = [n for n, attr in graph.nodes(data=True) if attr['type'] == 'internal']
        leaf_nodes = [n for n, attr in graph.nodes(data=True) if attr['type'] == 'leaf']

        # Draw internal nodes (blue circular)
        nx.draw_networkx_nodes(
            graph, pos, nodelist=internal_nodes,
            node_color="#6baed6", node_size=1600, node_shape="o"
        )
        # Draw leaf nodes (green squares)
        nx.draw_networkx_nodes(
            graph, pos, nodelist=leaf_nodes,
            node_color="#74c476", node_size=1800, node_shape="s"
        )

        # Draw edges and labels
        nx.draw_networkx_edges(graph, pos, arrows=False, edge_color="#636363", width=1.5)
        nx.draw_networkx_labels(graph, pos, labels=labels, font_size=9, font_family="sans-serif")
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10, font_color="#cb181d")

        plt.axis("off")
        plt.tight_layout()

        if save_path:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            plt.savefig(save_path, dpi=300, bbox_inches="tight")
            print(f"[OK] Saved tree visualization to: {save_path}")
        plt.close()
