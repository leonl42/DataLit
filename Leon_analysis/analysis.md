

### Motivation 
From an intuitive point of view one can easily argue that the relation between math complexity and acceptance/rejectance is complex.
Furthermore, even the notion of math complexity is complex enough. A single feature might simply be not enough to answer our hypothesis. 
In order to counter this issue, we train multiple models to predict if a paper was accepted or rejected. 
If we get a good enough performance, we are able to draw conclusions based on how the model weights the features for each class.

### Methods
We opted for white box models because we want to analyse the importance of each feature. 
More specifically, we used a support vector machine with a linear kernel, a decision tree and logistic regression.

To counter the class imbalances, we additionally tried SMOTEEN, which combines over- and undersampling. 

In order to evaluate the models, we plotted 4 different measures. Accuracy, f1 score, roc-auc and metthews-corrcoff. 

For ICLR we removed all papers that had the status "Withdraw" or "Desk Reject".

### Results

![image info]("./ICLR predict acceptance.png")
![image info]("./Neurips predict acceptance.png")

For NEURIPS the models performance is almost equal to guessing (roc-auc approx = 0.5, metthew-corrcoff approx = 0). 
So we wont make any assumptions about NEURIPS from this point on. 


For ICLR the plots show a performance somewhat better than guessing (roc-auc > 0.5, metthew-corrcoff > 0.1).

As for the models coefficients, all models had a combination of negative and positive coefficients. 

### Limitations

This makes reasoning about our hypothesis hard, as math complexity is a hard to define term. 
We cant possibly say which of our features represents math complexity best. 
If we wanted to say anything about our hypothesis, we would need all coefficients to be negative or positive.
