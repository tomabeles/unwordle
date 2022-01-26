## A Decision Tree Implementation of Wordle Solver

### Example run

The solution is 'sugar'

```
$ python3 unwordle.py
found 8636 words of proper length
Round: 1. Best word to try: story (8636 possible words)
Enter your attempted word: story
Enter your result in the form ##### (1 = Letter in correct position, 0 = Letter not in word, 2 = Letter in wrong position): 10020

Round: 2. Best word to try: sarks (135 possible words)
Enter your attempted word: sarks
Enter your result in the form ##### (1 = Letter in correct position, 0 = Letter not in word, 2 = Letter in wrong position): 12202

Round: 3. Best word to try: shear (18 possible words)
Enter your attempted word: shear
Enter your result in the form ##### (1 = Letter in correct position, 0 = Letter not in word, 2 = Letter in wrong position): 10011

Round: 4. Best word to try: simar (4 possible words)
Enter your attempted word: simar
Enter your result in the form ##### (1 = Letter in correct position, 0 = Letter not in word, 2 = Letter in wrong position): 10011

Round: 5. Best word to try: sugar (1 possible words)
Enter your attempted word: sugar
Enter your result in the form ##### (1 = Letter in correct position, 0 = Letter not in word, 2 = Letter in wrong position): 11111

Congratulations!
```

### Potential Improvements

1. Use a better dictionary -- this one has weird words in it, ex: aahing, which is technically a word, but would never be used
2. Add common use frequencies to dictionary -- pick the word with the highest frequency score