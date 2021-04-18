 





class TabuSearch:
    def __init__(self, initialSolution, solutionEvaluator, neighborOperator, acceptableScoreThreshold, tabuTenure):
        self.currSolution = initialSolution
        self.bestSolution = initialSolution
        self.evaluate = solutionEvaluator
        #self.aspirationCriteria = aspirationCriteria
        self.neighborOperator = neighborOperator
        self.acceptableScoreThreshold = acceptableScoreThreshold
        self.tabuTenure = tabuTenure
        
    def isTerminationCriteriaMet(self):
        # can add more termination criteria
        return self.evaluate(self.bestSolution) < self.acceptableScoreThreshold \
            or self.neighborOperator(self.currSolution) == 0

    def run(self):
        tabuList = {}
        
        while not self.isTerminationCriteriaMet():
            # get all of the neighbors
            neighbors = self.neighborOperator(self.currSolution)
            # find all tabuSolutions other than those
            # that fit the aspiration criteria
            tabuSolutions = tabuList.keys()
            # find all neighbors that are not part of the Tabu list

            filtered_neighbors = []
            for elemento in neighbors:
                if not str(elemento) in list(tabuList.keys()):
                    filtered_neighbors.append(elemento)
            ######neighbors = filter(lambda n: self.aspirationCriteria(n), neighbors)
            neighbors = filtered_neighbors

            # pick the best neighbor solution
            newSolution = sorted(neighbors, key=lambda n: self.evaluate(n))[0]
            # get the cost between the two solutions
            cost = self.evaluate(self.bestSolution) - self.evaluate(newSolution)
            # if the new solution is better, 
            # update the best solution with the new solution
            if cost >= 0:
                self.bestSolution = newSolution
            # update the current solution with the new solution
            self.currSolution = newSolution
            
            # decrement the Tabu Tenure of all tabu list solutions


            chaves = list(tabuList.keys())

            i=0

            if len(chaves)>0:
                while True:
                    sol = chaves[i]
                    tabuList[sol] -= 1
                    if tabuList[sol] == 0:
                        del tabuList[sol]
                        chaves = list(tabuList.keys())
                        i -=1
                    i += 1

                    if (i>=len(tabuList.keys())):
                        break


            #for sol in tabuList:
            #    tabuList[sol] -= 1
            #    if tabuList[sol] == 0:
            #        del tabuList[sol]
            # add new solution to the Tabu list


            tabuList[str(newSolution)] = self.tabuTenure

        # return best solution found
        return self.bestSolution


def vizinhos(a):
    #trocar 0 e 1; 1 e 2; 2 e 3
    vizinho1 = [a[1], a[0], a[2], a[3]]
    vizinho2 = [a[0], a[2], a[1], a[3]]
    vizinho3 = [a[0], a[1], a[3], a[2]]
    return [vizinho1, vizinho2, vizinho3]

def evaluator(a):
    _evaluator = 0
    #calcular diferenças entre os índices i+1 e i (anterior) e ver quantas diferenças são positivas
    for i in range(len(a)-1):
        diferenca = a[i+1]-a[i]
        if diferenca>0:
            _evaluator += 1
    return 3-_evaluator

#acceptableScoreThreshold = 1
#acceptableScoreThreshold = 5


solucaoInicial = [5, 3, 10, 1]

tabuSearchObject = TabuSearch(initialSolution = solucaoInicial,
                             solutionEvaluator = evaluator, 
                             neighborOperator = vizinhos, 
                             acceptableScoreThreshold = 1, 
                             tabuTenure = 5)

print(tabuSearchObject.run())


