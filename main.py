from common.splash_screen import *
from graphsearch.graph_search_visualizer import *
            
if __name__ == "__main__":
    choosen = SplashUserInput().getInput()
    if not choosen:
        print("Window closed unexpectedly")
        exit()
    print(f"Choosen Algorithm Type: {choosen}")
    if choosen == "Graph Search":
        GraphAlgorithmVisualizer()
    else:
        print("We are currently developing it (stay tuned)")
        