class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        row_set = defaultdict(set)
        col_set = defaultdict(set)
        sq_set  = defaultdict(set)

        for r in range(9):
            for c in range(9):

                # val is the val at index of r and c
                val = board[r][c]
                
                # if val is equal to a . just continue
                if val == '.':
                    continue

                # check if val is in the sets, if it is then return false
                if (val in row_set[r] or val in col_set[c] or val in sq_set[(r//3, c//3)]):
                    return False
                
                # add the vals into each set
                row_set[r].add(val)
                col_set[c].add(val)
                sq_set[(r//3 , c//3)].add(val)

                print(col_set)
        return True