from simamics.population import *
from simamics.virus import *
from simamics.dynamics import simulate
from simamics.interaction import interactionFunc3

random.seed(777)


population = Population(initialCases=20, populationSize=1000, space=500)

virus = Virus(
    lifeTime=15, deathRate=0.01, lightPercentage=0.25, mildPercentage=0.45, severePercentage=0.2,
    asymptomaticPercentage=0.1, transmissionPercentage=1)

report = simulate(population=population, virus=virus, iterations=30, populationActivity=0.8,
                  interaction=interactionFunc3, diagnosisPercentage=1)


report.backend = "matplotlib"
report.plotStatistics()

