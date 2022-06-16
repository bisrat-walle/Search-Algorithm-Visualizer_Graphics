from common.splash_screen import *
from graphsearch.graph_search_visualizer import *
            
if __name__ == "__main__":
    choosen = SplashUserInput().getInput()
    print(f"Choosen Alg Type: {choosen}")
    if choosen == "Graph Search":
        GraphAlgorithmVisualizer()
    else:
        print("We are currently developing it (stay tuned)")
        