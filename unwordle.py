class Node:
    def __init__(self, letters, parent=None) -> None:
        self.letters = letters
        self.child_word_count = 0
        self.children = {}
        self.parent = parent

    def print(self, intermediate=False):
        if len(self.children.keys()) == 0:
            print('leaf node:', self.letters)
        else:
            if intermediate:
                print('not leaf node:', 'child_words:', self.child_word_count, 'children:', self.children.keys())
        for key in self.children.keys():
            self.children[key].print()

    def add_word(self, word) -> None:
        self.child_word_count += 1
        letter = word[0]
        new_letters = self.letters + letter
        if not new_letters in self.children:
            self.children[new_letters] = Node(new_letters, self)
        next_word = word[1:]
        if len(next_word) > 0:
            self.children[new_letters].add_word(next_word)

    def isolate(self, letter, position):
        keys = list(self.children.keys())
        if position > 0:
            for key in keys:
                self.children[key].isolate(letter, position - 1)
        else:
            for key in keys:
                if key[-1] != letter:
                    self.children[key].delete()

    def check_leaves(self, letter):
        if letter in self.letters:
            return
        if len(self.children) == 0:
            if not letter in self.letters:
                self.delete()
        else:
            keys = list(self.children.keys())
            for key in keys:
                self.children[key].check_leaves(letter)

    def delete(self):
        parent_node = self.parent
        self.decrement_parents(self.child_word_count)
        parent_node.children.pop(self.letters)
        if len(parent_node.children.keys()) == 0:
            parent_node.delete()
    
    def decrement_parents(self, num):
        if self.parent:
            self.parent.child_word_count -= num
            self.parent.decrement_parents(num)

    def remove(self, letter, position=None):
        keys = list(self.children.keys())
        for key in keys:
            if position == None:
                if key[-1] == letter:
                    self.children[key].delete()
                else:
                    self.children[key].remove(letter)
            else:
                if position != 0:
                    self.children[key].remove(letter, position - 1)
                else:
                    if key[-1] == letter:
                        self.children[key].delete()

    def pick_best_word(self) -> str:
        score = {}
        if len(self.children.keys()) == 0:
            return self.letters
        for child_key in self.children.keys():
            curr_child = self.children[child_key]
            if not curr_child.child_word_count in score.keys():
                score[str(curr_child.child_word_count)] = [curr_child.letters]
            else:
                score[str(curr_child.child_word_count)].append(curr_child.letters)

        int_scores = [int(score) for score in score.keys()]
        high_score = max(int_scores)
        high_key = score[str(high_score)][0] # Do a tie breaker later. Random?
        return self.children[high_key].pick_best_word()


def apply_result(attempt, result, tree):
    for i in range(len(attempt)):
        if result[i] == '1':
            # keep only branches with this letter in this position
            tree.isolate(attempt[i], i)
        if result[i] == '0':
            # remove all branches with this letter starting at root node
            tree.remove(attempt[i])
        if result[i] == '2':
            # remove any branch with the letter in this position
            # remove any branches WITHOUT this letter
            tree.remove(attempt[i], i)
            tree.check_leaves(attempt[i])


def main(num_letters=5, num_rounds=6):
    word_list = []
    dictionary_file = open('wordle_dictionary.txt', 'r')
    for line in dictionary_file:
        word = line.strip()
        if len(word) == num_letters:
            word_list.append(word)
    print('found ' + str(len(word_list)) + ' words of proper length')

    root_node = Node('')

    # Build a massive tree of every word in the WORD_LIST
    for word in word_list:
        root_node.add_word(word)
    
    solved = False
    round = 1

    while not solved and round <= num_rounds:
        best_word = root_node.pick_best_word()
        print('Round: ' + str(round) + '. Best word to try: ' + best_word + " (" + str(root_node.child_word_count) + " possible words)")

        attempt = input("Enter your attempted word: ")
        if len(attempt) != num_letters:
            raise Exception("Your attempts should all be " + str(num_letters) + " letters long.")

        result = input("Enter your result in the form ##### (1 = Letter in correct position, 0 = Letter not in word, 2 = Letter in wrong position): ")
        if len(result) != num_letters:
            raise Exception("Your result should be " + str(num_letters) + " characters long.")
        if not set(result).issubset(set(['1', '2', '0'])):
            raise Exception("Your result should only be formed with the characters (0, 1, 2).")

        print("")

        if result == '11111':
            print('Congratulations!')
            solved = True
        else:
            try:
                apply_result(attempt, result, root_node)
                round += 1
            except AttributeError:
                print('All words eliminated -- could not solve')
            
main()
