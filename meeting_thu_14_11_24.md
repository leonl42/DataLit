# Meeting 14.11.24

- We only have data for NeurIPS and ICLR
  - Not an issue, as there's enough data.
  - Should put into discussion that these 2 conferences are pretty theory heavy
- TeX fetching script is done
  - Most papers have many different files => Need for import parsing
 
  - Analysis
    - Descriptive Analysis of the data:
      - Visualize the data distribution
    - To Answer Hypothesis:
      - Divide the data into different subsets (high novely score, ...) and see if there's correlation there
      - Probability of being accepted/rejected given score(s) (we need the other probabilities using bayes theorem)
      - Use the results from the 2 different conferences to see if our analysis method is sound and doesn't just work for one of the conferences
      - Make a feature vector out of all math notation related features of a paper and do a regression analysis on it (logistic: accepted  or not, linear: mean review score)
