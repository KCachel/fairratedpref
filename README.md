# Group Fair Rated Preference Aggregation: Ties are (Mostly) All You Need


Code and data for "Group Fair Rated Preference Aggregation: Ties are (Mostly) All You Need". To reproduce
the experiments run `electronics.py` (electronics data), `modcloth.py` (modcloth data), `hranalytics.py` (hr data),
`xwines.py` (xwines data), `tie_size_analysis.py` (tiesize data), `tie_count_analysis.py` (tiecount data). The ablation results are included in each dataset's corresponding script. Next to produce the plots
used in the paper run the script `Plotting_Script.R` in the `results/` folder. To reproduce the Appendix E results, in the `comparedmethods/` folder uncomment the section stating "to process the random break method" in the `EPIRA.py` and `epsilon_greedy.py` scripts.

All FATE source code is in the `src/` folder, and all compared methods are in the `comparedmethods/` folder. The EPIRA methods use the code from
[EPIRA](https://github.com/KCachel/Fairer-Together-Mitigating-Disparate-Exposure-in-Kemeny-Aggregation) and other methods without public implementations we code here.

The xwines and hr datasets are provided in the `datasets/` folder and the electronics and modcloth experiment scripts pull directly from their public github repository. 