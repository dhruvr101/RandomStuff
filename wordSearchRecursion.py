#You are given a 2D grid of letters (board) and a word.
#You can start at any cell.
#You can move up, down, left, or right to adjacent cells.
#you cannot revisit the same cell within one word path.
#Your goal is to check if the entire word can be formed by following adjacent cells in order.

class Solution:

    def runItAll(self,board,word):
        visitedSet = set([])
        return self.exist(board,word,"",visitedSet)
        
    def exist(self, board, word,currentWord,visitedSet):
        
        if self.checkDone(word,currentWord):
            return True
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                currentWord += board[i][j]
                if self.checkSoFar(word,currentWord):
                    visitedSet.add((i,j))
                
                    for eachTuple in self.adjacentCells(board,i,j):
                        for rowCoord, colCoord in eachTuple:
                            if (rowCoord,colCoord) not in visitedSet:
                                visitedSet.add((rowCoord,colCoord))
                                currentWord += board[rowCoord][colCoord]
                                if self.checkSoFar(word,currentWord):
                                    return self.exist(board,word,currentWord,visitedSet)
                                currentWord = currentWord[0:len(currentWord)-1]
                                visitedSet.remove((rowCoord,colCoord))
                    visitedSet.remove((i,j))
                currentWord = currentWord[1:len(currentWord)]
        return False

            
        

    def checkDone(self, word, currentWord):
        if word == currentWord:
            return True
        return False

    def checkSoFar(self, word, currentWord):
        if word == currentWord:
            return True
        return False
    
    #returns list fo adjacent cells in tuple format (i,j)
    def adjacentCells(self,board,i,j):
        outputList = []
        if (i-1) >= 0:
            outputList.append((i-1,j))
        if (i+1) < len(board):
            outputList.append((i+1,j))
        if (j-1) >= 0:
            outputList.append((i,j-1))
        if (j+1) < len(board[0]):
            outputList.append((i,j+1))

        return outputList




def test():
    s = Solution()  # Create instance of Solution




    board5 = [["A", "B"],
              ["C", "D"]]
    print("Test T:", s.runItAll(board5, "ABDC"))  # True
    print("Test F:", s.runItAll(board5, "ABDB"))  # False

    













    board1 = [
        ["A","B","C","E"], 
        ["S","F","C","S"], 
        ["A","D","E","E"]   
    ]
    print("Test 1:", s.runItAll(board1, "ABCCED"))  # True
    print("Test 2:", s.runItAll(board1, "SEE"))  # True
    print("Test 3:", s.runItAll(board1, "ABCB"))  # False
    board4 = [["A"]]
    print("Test 4:", s.runItAll(board4, "A"))  # True

if __name__ == "__main__":
    test()
