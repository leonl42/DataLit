## Links
1. [Progress Report slides](https://docs.google.com/presentation/d/1_PjO-GfJQZqyeoo8zNLkMZTwyhgaAacsFf13Zkqffbw)
2. [Pitch slides](https://docs.google.com/presentation/d/1bfmJSNTjsVf3nUE4XK-0xGi1dQ5PNYb1yLFsbIL4m-Y)

## TODO:
### Dataset
#### arXiv Downloads
- [x] Write script to check downloaded papers for matching titles **LINUS**
#### Math Extraction
- [x] Update Math-Extraction Script to parse properly **LEON**
- [x] Run the script again **LINUS**
- [ ] Check 10 pandoc parsed papers for correct math extraction.
- [ ] Check 10 LateXML parsed papers for correct math extraction.

#### Feature Extraction
- [x] Run the script **LEON**
- [x] Check 10 files for whether feature Extraction is correct **LINUS**
- [ ] => Find and fix bugs in feature extraction code.
- [ ] Run the script (again)
- [x] Update script to append normalized dependent variable values to predict (accepted/rejected) to csv **LEON**

### Analysis/Validation (PRELIMINARY - We stil need to discuss if these features are enough)
- [ ] Correlation Analysis - **JAISIDH**
- [x] Linear Regression with Review Scores **LEON**
- [x] Logistic Regression with Accept/Reject **LEON**
- [ ] Hypothesis Testing to get p-values for how separated the accepted/rejections populations are - **JAISIDH**
- [ ] Test hypothesis about variances

### Visualization 
- [ ] Decide which visualizations will be best in a meeting

### Report (**DEADLINE Su 09.02.25**)
- [ ] First, _very_ rough draft **LINUS**
- [ ] Discuss each point of the requirements below in a meeting and split up writing
#### Requirements
![{F11BD02C-8F08-42EB-89C2-68D604533A1E}](https://github.com/user-attachments/assets/640ab4c4-2b49-46ed-8ff3-95cdf685ba9d)
![{E660C9A4-6B2F-4FEF-BEE2-346F23EB4BCF}](https://github.com/user-attachments/assets/38bb40a7-ed35-478a-af74-b26208f3630f)

#### Evaluation Criteria
![{30862622-EBCE-4DF4-A0AB-03F8C1933B8F}](https://github.com/user-attachments/assets/5dbab0f0-5e1d-40d7-b1a4-9facf17c3fb3)

### Code
- [ ] Remove any references to LLM written code.
- [ ] Put some comments. Should be readable.
- [ ] Make sure only the code we actually used is submitted. 
