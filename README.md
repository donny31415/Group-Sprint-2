# Set vs graph neural networks for expected goals (xG)

Data Science Toolbox, Assessment 2 (Data at Scale).

**Question:** does modelling the players around a shot as a graph predict goals better than treating them as an
unordered set? Data: StatsBomb open-data freeze frames from the men's top-5 European leagues.

## Project group
- Luke
- Don
- Pietro
- Dylan

*(contributions to be added)*

## Preparation
Python 3.9+ with:

```
pip install numpy pandas matplotlib requests tqdm scikit-learn torch
```

No GPU is needed. `02-Analysis.ipynb` runs in about 25–45 minutes on a laptop CPU.

## Reading order
1. `01-Data.ipynb`: downloads the StatsBomb open data from GitHub (a few minutes on the first run, cached after
   that), builds `data/processed/shot_table.csv`, `player_table.csv` and `feature_columns.json`.
2. `02-Analysis.ipynb`: graph construction, the set and graph models, tuning experiments, the final set-vs-graph
   test, and the scaling analysis.
   Must be run after `01-Data.ipynb`.

Figures are saved to `figures/` (numbered as in the notebooks) and result tables to `results/`.

## Notes on the data
Most matches come from four complete 2015/16 seasons (Premier League, La Liga, Serie A, Ligue 1). The remaining
seasons contain only one club's matches (for example Barcelona in the Messi era and Arsenal's 2003/04 "Invincibles"
season), so they are a biased sample. The notebooks flag these and use the complete 2015/16 matches for evaluation.

Data: StatsBomb open data, https://github.com/hudl/open-data (attribution required).
