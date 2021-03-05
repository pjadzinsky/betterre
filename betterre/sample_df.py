import pandas as pd
import numpy as np


def fake_df(gammas, col_names, N):
    ss = []
    for gamma, col_name in zip(gammas, col_names):
        s = pd.Series(np.random.gamma(gamma, size=(N,)))
        s.name = col_name
        ss.append(s)
    df = pd.concat(ss, axis=1)
    return df