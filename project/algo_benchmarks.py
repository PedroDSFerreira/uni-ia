from agent import Agent
from time import time
import csv
import sys

SAMPLE_SIZE = 5

def main():
    if len(sys.argv) != 2:
        print('Usage: python algo_benchmarks.py <output_file>')
        sys.exit(1)


    path = "results/"
    csv_file = sys.argv[1]
    with open(path+csv_file, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Level", "Avg Moves", "Avg Open Nodes", "Agv Time"])

    with open("levels.txt", "r") as f:
            for lvl, map_str in enumerate(f.readlines(), start=1):

                grid = map_str.split(' ')[1]
                

                times = []
                len_open_nodes = []
                len_moves = []

                for sample in range(SAMPLE_SIZE):
                    agent = Agent(grid)
                    start_time = time()
                    moves = agent.solve()
                    end_time = time()
                    times.append(end_time - start_time)
                    len_open_nodes.append(agent.count_nodes)
                    len_moves.append(len(moves))
                
                with open(path+csv_file, "a") as f:
                    writer = csv.writer(f)
                    writer.writerow([lvl, sum(len_moves)/SAMPLE_SIZE, sum(len_open_nodes)/SAMPLE_SIZE, sum(times)/SAMPLE_SIZE])

if __name__ == "__main__":
    main()