import os

HIGH_SCORES_FILE = "high_scores.txt"

def initialize_high_scores():
    if not os.path.exists(HIGH_SCORES_FILE):
        with open(HIGH_SCORES_FILE, 'w') as f:
            f.write("0\n" * 10) 

def read_high_scores():
    with open(HIGH_SCORES_FILE, 'r') as f:
        scores = [int(line.strip()) for line in f.readlines()]
    return scores

def write_high_scores(scores):
    with open(HIGH_SCORES_FILE, 'w') as f:
        for score in scores:
            f.write(f"{score}\n")

def update_high_scores(new_score):
    scores = read_high_scores()
    scores.append(new_score)
    scores.sort(reverse=True)
    scores = scores[:10]  
    write_high_scores(scores)


initialize_high_scores()
