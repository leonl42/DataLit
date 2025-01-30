Data lit notes

Current observations:
- Feature creation is not perfect, fix the issue that stuff within {} is not treated as one symbol
- On the current features, linear regression ~ random, logistic regression ~ random (ICLR)
- On the current features, linear / logistic regression = random (NeurIPs)

Reminder: the answer “can’t say/hard to conclude” is still a finding.

Todos:

- [x] Decide whether to tinker with the {} issue in the feature extraction script - LEON’s idea
- [x] Correlation analysis and p-value b/w feature populations
- [ ] Database overview diagram - IDEAS COME FROM EVERYONE, JAISIDH DRAWS
- [ ] Which part of analysis to present when and how
- [ ] I will make a section in the repo README, where everyone of us will drop in the limitations that we think the work has.

Intro: problem
Dataset: statistics, (scraping, preprocessing, feature engineering)
Analysis:
-  Imbalances and skewness in samples
-  Box plot, or a histogram - JAISIDH
-  Correlation and p-values - JAISIDH
-  Linear regression, logistic, decision tree, and then say that you can’t say - ANUPAM + LEON
Limitations

For each experiment that we do, logging it like this can be helpful:
- Experiment setup
- Method
- Observation
- Conclusion


 Also For each type of analysis, we are doing it b/w accept/reject or regressing against recommendation scores. We should also see if poster and top-25 are separable or not. Basically we try to find any two classes, or any metric that can definitively be predicted.

 # What are the limitations of our work?

 Everyone adds here.
