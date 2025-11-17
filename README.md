# GraphAware-Disinformation-Analysis

GraphAware-Disinformation-Analysis is an end-to-end pipeline for detecting coordinated influence operations (bots, propaganda clusters, manipulated networks) on social media platforms like Twitter/X.
The system converts social interactions into a graph, learns embeddings using Node2Vec, refines structural patterns with a Graph Neural Network (GraphSAGE), and performs supervised classification to identify coordinated accounts.

## Features
- Graph-based modeling of user interactions
- Detection of coordinated patterns and bot-like activity
- Support for large-scale datasets
- PyTorch + PyTorch Geometric based model

## Tech Stack
- Python
- PyTorch
- PyTorch Geometric
- NetworkX
- Scikit-Learn
- Jupyter Notebook

- ## Installation
```bash
pip uninstall torch -y
pip install torch==2.2.0+cpu -f https://download.pytorch.org/whl/cpu
pip install torch-geometric
pip install pyg-lib -f https://data.pyg.org/whl/torch-2.2.0+cpu.html
