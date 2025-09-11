# Learning Systems Assignment 2

## 4. Classify all the 6 patients with the three rules
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

## 5. Mix Type I and Type II Feedback with forget value 0.8 and memorize value 0.2 to learn a rule for Recurrence

```IF Deg_malig_3 AND NOT Menopause_lt40 THEN Recurrence```

## 6. Mix Type I and Type II Feedback with forget value 0.8 and memorize value 0.2 to learn a rule for Non-recurrence
```IF Deg_malig_3 AND Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Non-Recurrence```

## 7. Repeat 5. and 6. with forget value 0.5 and memorize value 0.5
```
Recurrence rules:
IF Deg_malig_3 AND NOT Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Recurrence
Non-Recurrence rules:
IF Deg_malig_3 AND Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Non-Recurrence
```

## 8. Repeat 5. and 6. with forget value 0.2 and memorize value 0.8
```
Recurrence rules:
IF Deg_malig_3 AND NOT Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Recurrence
Non-Recurrence rules:
IF Deg_malig_3 AND Menopause_lt40 AND NOT Inv_nodes_0_2 THEN Non-Recurrence
```


