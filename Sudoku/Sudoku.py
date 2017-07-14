import time
from collections import deque
import random

goal_test_counter = 0
constructor_counter = 0
start = 8
end = 400
skip = 1

class Sudoku:
    def __init__(self, state = None, choices=None, n=81, parent = None, cursor = 0):
        global constructor_counter
        constructor_counter+=1
        if choices is None:
            self.choices = [set(range(9)) for i in range(n)]
            #print(self.choices)
        else:
            self.choices = choices
        if state is None:
            self.state = [-1] * n
        else:
            self.state = state
        self.n = n
        self.parent = None
        self.cursor = cursor
        assert (all([type(s) == set for s in self.choices]))

    def correctIndex(self, number):
        if number < 3:
            return 0
        if number < 6:
            return 3
        if number < 9:
            return 6


    def updateChoices(self,var,value):
        #does rows and columns
        for k in range((var//9) *9, ((var//9)*9)+9):
            self.choices[k].difference_update({value})
        for i in range(var%9, 81, 9):
            self.choices[i].difference_update({value})

        #gets index to remove choices for box
        row = var//9
        col = var%9

        assignVar = self.correctIndex(row)*9 + self.correctIndex(col)
        assignVar = (row // 3) * 3 * 9 + (col//3) * 3

        #removes choices for box
        for j in range(assignVar, assignVar+3):
            self.choices[j].difference_update({value})
        assignVar = assignVar + 9
        for w in range(assignVar, assignVar+3):
            self.choices[w].difference_update({value})
        assignVar = assignVar + 9
        for e in range(assignVar, assignVar+3):
            self.choices[e].difference_update({value})

    def assign(self, var, value):
        startRow = 0
        startCol = 0
        self.state[var] = value
        self.choices[var] = set()
        self.updateChoices(var, value)
        for i in range(self.n):
            if len(self.choices[i]) == 1:
                val = self.choices[i].pop()
                self.assign(i, val)
                self.updateChoices(i, val)
        self.cursor +=1
        return True

    def goal_test(self):
        global goal_test_counter
        goal_test_counter +=1
        numassigned = [s!= -1 for s in self.state].count(True)
        return numassigned == self.n

    def get_next_unnasigned_var(self):
        return self.__getnext_most_constrained()

    def __getnext_most_constrained(self):
        cols = list(range(self.n))
        random.shuffle(cols)
        i_min = cols[0]
        for i in cols:
            if 0<len(self.choices[i])<len(self.choices[i_min]) or len(self.choices[i_min]) == 0:
                i_min = i
        return i_min

    def get_choices_for_var(self, var):
        return self.__sort_choices_by_constraints(var)

    def __sort_choices_by_constraints(self, var):
        l = list(self.choices[var])
        l.sort(key=lambda x: abs(x-self.n //2))
        return l


    def consistency_test(self):
        for i in range(self.n):
            if self.state[i]== -1 and len(self.choices[i]) == 0:
                return False
        return True

    def __str__(self):
        s = ""
        for i in range(self.n):
            if i%9 ==0:
                s+="\n"
                s+=str(self.state[i]) + ", "
            elif i%9 == 8:
                s+=str(self.state[i]) + " "
            else:
                s+=str(self.state[i]) + ", "
        return s

def dfs_recursive(state: Sudoku, start_state, count = 0):
    if state.goal_test(): return state, count+1
    if not state.consistency_test(): return None, count+1
    var = state.get_next_unnasigned_var()
    if state.choices[var] is None: return None, count+1
    for val in state.get_choices_for_var(var):
        child = Sudoku(state = list(state.state), choices = [set(i) for i in state.choices], parent=state, cursor= state.cursor, n = state.n)
        if child.assign(var, val):
            result, subcount = dfs_recursive(child, start_state, count)
            count = subcount
            if result is not None: return result, count+1
    return None, count+1

def search(st):
    s = Sudoku()
    for k in range(81):
        if st[k:k+1] != ".":
            s.assign(k, int(st[k:k+1])-1)
    print(s)
    sol, count = dfs_recursive(s, s)
    return sol, count
    print(sol)
    print(time.time()-t)

def main():
    t = time.time()
    x, count = search("1.....3.8.6.4..............2.3.1...........958.........5.6...7.....8.2...4.......")
    start = x.state

    for i in range(81):
        start[i]= start[i]+1

    print(x)
    print("\n")
    print(time.time()-t)
    print(count)

if __name__ == "__main__":
    # generate_tests(start, end, skip)
    main()
