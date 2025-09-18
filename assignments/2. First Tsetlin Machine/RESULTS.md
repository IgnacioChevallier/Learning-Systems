# Learning Systems Assignment 2

## Task 1
### 1. Classify all the 6 patients with the three rules
- R1 if Deg-malign 3 and not Menopause lt40 then Recurrence,
- R2 if Deg-malign 3 then Recurrence,
- R3 if Inv-nodes 0-2 then Non-Recurrence.

```
Predictions:
Patient 1: Recurrence      Votes:  2
Patient 2: Recurrence      Votes:  0
Patient 3: Recurrence      Votes:  2
Patient 4: Non-Recurrence  Votes: -1
Patient 5: Recurrence      Votes:  1
Patient 6: Non-Recurrence  Votes: -1
```
This shows the different predictions the Tsetlin Machine achieved on each one of the patients whether there is Recurrece or not. 
On top of this, it shows the amount of votes it got from which we can now how certain of the decition made is.

## Task 2

### 1. Mix Type I and Type II Feedback with forget value 0.8 and memorize value 0.2 to learn a rule for Recurrence

```IF Deg_malig_3 AND NOT Menopause_lt40 THEN Recurrence```


### 2. Mix Type I and Type II Feedback with forget value 0.8 and memorize value 0.2 to learn a rule for Non-recurrence
```IF Deg_malig_3 AND Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Non-Recurrence```

This are the rules the Tsetlin Machine learnt from the breast_cancer_dataset.json with different aproaches, positive and negative reinforcment.
The conclusion is to train with both to achieve better accuracy.

## Task 3

### 1. Repeat Task 2 with forget value 0.5 and memorize value 0.5

```
Recurrence rules:
IF Deg_malig_3 AND NOT Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Recurrence
Non-Recurrence rules:
IF Deg_malig_3 AND Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Non-Recurrence
```

## 2. Repeat Task 2 with forget value 0.2 and memorize value 0.8

```
Recurrence rules:
IF Deg_malig_3 AND NOT Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Recurrence
Non-Recurrence rules:
IF Deg_malig_3 AND Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Non-Recurrence
```

The results of task 3 being similar show that the Tsetlin Machine is robust to variations in forget and memorize parameters. 
Even when we change the balance between forgetting and memorization the machine converges to nearly the same rules. 
This indicates that the core learning dynamics are stable, and the system consistently extracts the same underlying patterns from the data.