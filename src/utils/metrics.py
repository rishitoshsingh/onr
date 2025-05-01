import pandas as pd

def get_scoreboard(scoreboard_path, max_attacks):
    """
    Read the scoreboard from a CSV file and return it as a DataFrame.
    """
    scoreboard_df = pd.read_csv(scoreboard_path)

    moves_df = scoreboard_df[["Move_1","Move_2","Move_3","Move_4","Move_5","Move_6","Move_7","Move_8","Move_9","Move_10","Move_11","Move_12","Move_13","Move_14","Move_15","Move_16","Move_17"]]
    scores_df = scoreboard_df[["Score_1","Score_2","Score_3","Score_4","Score_5","Score_6","Score_7","Score_8","Score_9","Score_10","Score_11","Score_12","Score_13","Score_14","Score_15","Score_16","Score_17"]]

    # Select only the first num_trials columns
    moves_df = moves_df.iloc[:, :max_attacks]
    scores_df = scores_df.iloc[:, :max_attacks]

    # Drop rows with None values in moves_df or scores_df
    valid_rows = ~moves_df.isnull().any(axis=1)
    moves_df = moves_df[valid_rows]
    scores_df = scores_df[valid_rows]
    return moves_df, scores_df


def analyze_scoreboard(scoreboard_path, max_attacks):
    moves_df, scores_df = get_scoreboard(scoreboard_path, max_attacks)

    # Find the maximum score in the last column of scores_df and its index
    max_score_index = scores_df.iloc[:, -1].idxmax()
    # Get the corresponding data from moves_df at that index
    corresponding_moves = moves_df.loc[max_score_index]

    print(f"Maximum score achieved in {max_attacks}: {scores_df.iloc[max_score_index, -1]}")    
    print("Data of moves_df at the index of maximum score in the last column:")
    
    print(corresponding_moves)


def get_scoreboard_save_our_system(scoreboard_path):
    """
    Read the scoreboard from a CSV file and return it as a DataFrame.
    """
    scoreboard_df = pd.read_csv(scoreboard_path, index_col=False, sep=";")
    moves_df = scoreboard_df[["Move_1","Move_2","Move_3","Move_4","Move_5","Move_6","Move_7","Move_8","Move_9","Move_10"]]
    scores_df = scoreboard_df[["Score_1","Score_2","Score_3","Score_4","Score_5","Score_6","Score_7","Score_8","Score_9","Score_10"]]
    return moves_df, scores_df


def analyze_scoreboard_save_our_system(scoreboard_path):
    moves_df, scores_df = get_scoreboard_save_our_system(scoreboard_path)
    # Find the maximum score in the last column of scores_df and its index
    max_score_index = scores_df.iloc[:, -1].idxmax()
    corresponding_moves = moves_df.loc[max_score_index]

    print(f"Maximum score achieved: {scores_df.iloc[max_score_index, -1]}")    
    print("Data of moves_df at the index of maximum score in the last column:")
    print(corresponding_moves)


