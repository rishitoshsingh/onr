import pandas as pd
def analyze_scoreboard(scoreboard_path, num_trials):
    scoreboard_df = pd.read_csv(scoreboard_path)
    last_n_records = scoreboard_df.iloc[-num_trials:, :].values

    # Display the last N records
    print("")
    for idx, record in enumerate(last_n_records, start=1):
        scores = ' '.join(map(str, record[:5]))
        print(f"Trial {idx} | {scores} |")

    # Calculate metrics
    max_scores = last_n_records[:, :5].max(axis=1)
    min_scores = last_n_records[:, :5].min(axis=1)
    avg_scores = last_n_records[:, :5].mean(axis=1)

    print("\nMetrics:")
    print(f"Maximum score received in 5 moves: {max_scores.max()}")
    print(f"Average score across all trials: {avg_scores.mean():.2f}")