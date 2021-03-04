from Trindod import *


class GeneticAlgorithum:

    def __init__(self, job, paneldata):
        self.TrindodQue = job.TrindodQue
        self.paneldata = paneldata
        self.Population = job.Population
        self.Genes = job.Genes
        self.MutationRate = job.MutationRate
        self.LowLimits = job.LowLimits
        self.HighLimits = job.HighLimits
        self.Target = job.Target
        self.MaxIter = job.MaxIter
        self.Children = job.Children
        self.Generation = 0
        self.T = LCOE(self.TrindodQue, self.paneldata)
    
    def Save_Popultaion_To_Obj(self):
        Gen = 'G' + str(self.Generation)
        self.Children = np.random.randint(0, 0xFFFFFF, len(self.Population))
        vhex = np.vectorize(hex)
        self.Children = vhex(self.Children)
        if self.Generation == 0:
            self.NamedPopulation = pd.DataFrame(self.Population, index=self.Children)
            self.NamedPopulation['Mothes'] = np.zeros(len(self.Population))
            self.NamedPopulation['Fathers'] = np.zeros(len(self.Population))
            self.NamedPopulation['Generation'] = Gen
            self.NamedPopulation['Fitness'] = self.Fitness
            self.NamedPopulation['Results'] = self.Results
        else:
            self.Mothers = self.PreviousName[self.Mothers]
            self.Fathers = self.PreviousName[self.Fathers]
            NamedPopulation = pd.DataFrame(self.Population, index=self.Children)
            NamedPopulation['Mothes'] = self.Mothers
            NamedPopulation['Fathers'] = self.Fathers
            NamedPopulation['Generation'] = Gen
            NamedPopulation['Fitness'] = self.Fitness
            NamedPopulation['Results'] = self.Results
            self.NamedPopulation = self.NamedPopulation.append(NamedPopulation)
        return

    def Save_Popultaion_To_File(self):
        Gen = 'G' + str(self.Generation)
        self.Children = np.random.randint(0, 0xFFFFFF, len(self.Population))
        vhex = np.vectorize(hex)
        self.Children = vhex(self.Children)

        if self.Generation == 0:
            NamedPopulation = pd.DataFrame(self.Population, index=self.Children)
            NamedPopulation['Mothes'] = np.zeros(len(self.Population))
            NamedPopulation['Fathers'] = np.zeros(len(self.Population))

        else:
            self.Mothers = self.PreviousName[self.Mothers]
            self.Fathers = self.PreviousName[self.Fathers]
            NamedPopulation = pd.DataFrame(self.Population, index=self.Children)
            NamedPopulation['Mothes'] = self.Mothers
            NamedPopulation['Fathers'] = self.Fathers

        NamedPopulation['Fitness'] = self.Fitness
        NamedPopulation['Results'] = self.Results
        NamedPopulation.to_csv('Generations\\' + Gen + '.csv')
        return
    
    def Save_PanelData(self):
        PanelData = pd.DataFrame()
        PanelData['PanelID'] = np.arange(0, len(self.Population), 1, dtype='int')+1
        PanelData['Type'] = self.Children
        PanelData['Life'] = self.Population[:, 0]
        PanelData['Burn-in'] = self.Population[:, 1]
        PanelData['Long-termDegradation'] = self.Population[:, 2]
        PanelData['Burn-inPeakSunHours'] = 500
        PanelData['Cost'] = 0.245
        PanelData['PowerDensity'] = self.Population[:, 3]
        PanelData['EnergyEfficiency'] = self.Population[:, 3] / 9.8 / 100
        PanelData.to_csv(self.paneldata, index=False)
        return
    
    def Breed_Population(self):
        self.Mothers = np.random.choice(range(len(self.Population)), int(len(self.Population)), p=self.Fitness)
        self.Fathers = np.random.choice(range(len(self.Population)), int(len(self.Population)), p=self.Fitness)

        NP = np.zeros(np.shape(self.Population))
        i = 0
        CrosoverPoints = np.random.randint(0, self.Genes+1, len(self.Population))
        for NPp, P1, P2, CrosoverPoint in zip(NP, self.Mothers, self.Fathers, CrosoverPoints):
            NPp[:CrosoverPoint] = self.Population[P1, :CrosoverPoint]
            NPp[CrosoverPoint:] = self.Population[P2, CrosoverPoint:]
            NP[i] = NPp
            i = i + 1
        self.Population = NP
        return
    
    def Mutate_Population(self):
        for idx, Pop in enumerate(self.Population):
            Mutation = np.random.uniform(0, 1)
            if Mutation > 1 - self.MutationRate:
                MutatedGene = np.random.randint(0, self.Genes)
                NewGene = np.random.uniform(self.LowLimits[MutatedGene], self.HighLimits[MutatedGene])
                Pop[MutatedGene] = NewGene
                self.Population[idx] = Pop
        return 

    def Test_Population(self):
        self.Fitness = np.zeros(len(self.Population))
        self.Fitness[:] = np.abs(self.Results[:] - self.Target)
        Finf = np.where(self.Fitness == np.inf)
        self.Fitness[Finf] = 100000000000000
        Fmax = np.amax(self.Fitness)
        Fmin = np.amin(self.Fitness)
        self.Fitness[:] = (Fmax - self.Fitness[:])/(Fmax - Fmin)
        self.Fitness[:] = self.Fitness[:] / self.Fitness.sum()
        return 

    def Itterate(self):
        self.T.LoadJBS()
        while self.Generation < self.MaxIter:
            self.Save_PanelData()
            self.T.LoadJBS()
            self.T.Run()
            self.Results = self.T.FetchReults()
            self.Test_Population()
            self.Save_Popultaion_To_Obj()
            self.PreviousName = self.Children
            self.Breed_Population()
            self.Mutate_Population()
            self.Generation = self.Generation + 1
        return


class GeneticAlgorithumJob:

    def __init__(self, tq, population, genes, mutationrate, target, maxiter):
        self.TrindodQue = tq
        self.Population = population
        self.Genes = genes
        self.MutationRate = mutationrate
        self.Target = target
        self.MaxIter = maxiter
        self.Children = np.random.randint(0, 0xFFFFFF, population)
        vhex = np.vectorize(hex)
        self.Children = vhex(self.Children)

    def Random_Popultaion(self, lowlimits, highlimits):
        self.LowLimits = lowlimits
        self.HighLimits = highlimits
        self.Create_Population()
        return self

    def Load_Population(self, filepath):
        self.FilePath = filepath
        PanelData = pd.read_csv(self.FilePath, index_col=False)
        PanelData = PanelData.iloc[0:self.Population]
        PanelData = PanelData.drop(columns=['PanelID', 'Type', 'Burn-inPeakSunHours', 'Cost', 'EnergyEfficiency'])
        PanelData = PanelData.to_numpy()
        self.Population = PanelData
        self.LowLimits = np.amin(PanelData, axis=0)
        self.HighLimits = np.amax(PanelData, axis=0)
        return self

    def Create_Population(self):
        Pop = np.zeros((self.Population, self.Genes))
        for Gene in range(self.Genes):
            Pop[:, Gene:Gene+1] = np.random.uniform(self.LowLimits[Gene], self.HighLimits[Gene], (self.Population, 1))
        self.Population = Pop