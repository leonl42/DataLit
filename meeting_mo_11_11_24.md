# Meeting Sa 09.11.24
- We'll do protocols for every meeting to have structure.
- We'll go with the math representational complexity project for now. If it doesn't work out, we'll pick something else.

## [Project-Pitch](https://docs.google.com/presentation/d/1E7IsnVVx13HaP29kQKn5R657Bob60zTWs-cjA9dyKjI/edit#slide=id.p) (5min, earliest DEADline: Mo 18.11.24)
### HYPOTHESIS: "Our hypothesis is..."  (1min) ✓
- GUIDELINES:
  - SHOULD NOT BE vague, infeasible ✓
  - SHOULD BE original, relevant, and challenging (yet feasible) ✓
- HOOK: "Have you ever read a paper and felt that the math is needlessly complicated? Or have you ever WRITTEN a paper and asked yourself if you've put enough math in there?" (maybe put [tweet](https://x.com/PatrickKidger/status/1833840946896666730) of researcher whose paper was rejected because the math wasn't complicated enough on here)
- HYPOTHESIS: 'More complex mathematics in ML Papers leads to better acceptance rates at conferences.'
- MOTIVATION and the real-world APPLICATION/PROBLEM?
  - Analytics for specific venues (NeurIPS, ICLR).
  - Data-driven insights to authors.
  - Solace to people who face statements like "limited novelty, not enough math" from Reviewer 2.

### DATA(SET): (2min)
- GUIDELINES:
  - Appropriate Size and credibility 
  - SHOULD NOT BE inappropriate for research question, dubious source, too small
  - SHOULD BE exceptional effort in sourcing/preprocessing data
- WHAT are we collecting? NeurIPS and ICLR Data from year(s)
- FROM? 
  - Jsons for acceptance/rejection and scores from [paperlists](https://github.com/papercopilot/paperlists?tab=readme-ov-file) 
  - TeX Source Files from arXiv
- HOW are we doing the collection?
  - Parse the jsons for NeurIPS and ICLR for scores and acceptance status, saving tex source files from arXiv 
  - Extract all Latex Equations out of the tex source files 
- HOW are we measuring complexity? 
  - [Paper](https://www.mdpi.com/2073-8994/13/2/188) containing info about representational complexity 
  - We need a script to assign complexity scores per equation and paper and save those to the paper json
  
### ANALYSIS (2min)
- Guidelines:
  - What analysis method are we doing? Why have we chosen this one? Compare alternative ones.
  - SHOULD NOT BE incorrect or poorly implemented
  - SHOULD BE Exceptionally well-designed and use complementary approaches
- What is equation complexity?
    - Confidence value analysis between the 2 different conferences (and/or years)
    - We can make a feature vector out of our features and do regression analysis
    - Maybe analyze the review texts as well (probably out of scope)

## TODO:
- Figure out how we'll measure complexity conceptually
- Figure out what we'll do for Analysis conceptually
- Decide on what format we'll use to represent the data throughout our process
### Code:
- Parse the jsons for NeurIPS and ICLR for scores and acceptance status, saving tex source files from arXiv (Linus)
- Extract Formulas from the tex source files per paper
- Calculate complexities for each paper
### Presentation
- Make Hypothesis/Intro Slides
  - Use hook as described
- Make Dataset Slides
  - Show where the data is from and how we're fetching it
  - Show examples of Formula Complexity
- Make Analysis Slides
  - What are we doing?
  - How does this test our hypothesis?


# Future Meetings
## Report
- What is our concrete HYPOTHESIS: "Our hypothesis is..."  (1min)
    - What's our motivation and the real-world application/problem?
    - How is it testable? Clear objectives for testing that hypothesis.
    - SHOULD NOT BE vague, infeasible
    - SHOULD BE original, relevant, and challenging (yet feasible)

- What DATA(SET) are we using, how/from where are we collecting it? [Conference, Timespan, Categories] (2min)
    - Appropriate Size and credibility
    - What pre-processing steps are we taking?
    - SHOULD NOT BE innapropriate for research question, dubious source, too small
    - SHOULD BE exceptional effort in sourcing/preprocessing data

- What ANALYSIS  are we performing? (2min)
    - What is equation complexity?
    - What analysis method are we doing? Why have we chosen this one? Compare alternative ones.
    - SHOULD NOT BE incorrect or poorly inmplemented
    - SHOULD BE Exceptionally well-designed and use complementary approaches

- What are LIMITATIONS in our process and results (biases, weaknesses)
   - We can't control what the reviewers already know and how they're cognitive load is decreased

- Write a comprehensive report with standart paper structure (Abstract, Introduction, Methods, Results, Discussion/Limitations)

- Effectively VISUALIZE data
