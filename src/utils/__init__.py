from .Node import Node
from .Edge import Edge

def save_trials_to_csv(trial_record, filename, sep=","):
    """
    Save the trials to a CSV file.
    """
    with open(filename, 'a') as f:
        f.write(sep.join(str(item) if item is not None else '' for item in trial_record) + '\n')