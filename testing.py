class random:

    def actualTestFunc(self,word):
        visitedSet = set([])
        return self.randomFunc(word,visitedSet)
    
    def randomFunc(self,word,visitedSet):
        visitedSet.add("another")

        if word in visitedSet:
            return False
        return True
    
def test():
    s = random()

    print("Test 1:", s.actualTestFunc("dhruv"))  # False
    print("Test 1:", s.actualTestFunc("randomassword"))  # True
    print("Test another:", s.actualTestFunc("another"))  # True


if __name__ == "__main__":
    test()
