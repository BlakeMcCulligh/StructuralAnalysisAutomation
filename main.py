from SteelCrossSection import getCrossSectionProperties
import SteelCode
import pandas as pd
import openpyxl

massWeight = 1
deformationWeight = 1

K = 1
L = 10000
F = 10000000

SectionData= pd.read_excel('SectionDimentions.xlsx')

memberName = list(SectionData['memberName'])
memberType = list(SectionData['memberType'])
d = list(SectionData['d'])
b = list(SectionData['b'])
t = list(SectionData['t'])
w = list(SectionData['w'])

Cr = []
Tr = []
deformation = []
CompressionUtilization = []
TensionUtilization = []
mass = []

for i in range(len(memberType)):
    [A, Ix, Iy, Sx, Sy, Zx, Zy, J, Cw, rx, ry, xo, yo] = getCrossSectionProperties(memberType[i],d[i],b[i],t[i],w[i])
    numSymmetry = Steel.getNumSymmetry(memberType[i])
    mass.append(A*785)
    Cr.append(Steel.getCompressionResistance(numSymmetry, K, L, rx, ry, xo, yo, A, J, Cw))
    CompressionUtilization.append(F/Cr[i])
    Tr.append(Steel.getTensionResistance(A))
    TensionUtilization.append(F/Tr[i])
    deformation.append(Steel.getAxialDef(A, L, F))

SectionData["Cr"] = Cr
SectionData["Tr"] = Tr
SectionData["deformation"] = deformation
SectionData["CompressionUtilization"] = CompressionUtilization
SectionData["TensionUtilization"] = TensionUtilization
SectionData.to_excel('SectionDimentions.xlsx', index=False)

memberNameC = memberName*1
memberNameT = memberName*1
massC = mass*1
massT = mass*1
deformationC = deformation*1
deformationT = deformation*1
utilizationC = CompressionUtilization*1
utilizationT = TensionUtilization*1

for i in reversed(range(len(CompressionUtilization))):
    if CompressionUtilization[i] > 1:
        CompressionUtilization.pop(i)
        utilizationC.pop(i)
        memberNameC.pop(i)
        massC.pop(i)
        deformationC.pop(i)

for i in reversed(range(len(TensionUtilization))):
    if TensionUtilization[i] > 1:
        utilizationT.pop(i)
        memberNameT.pop(i)
        TensionUtilization.pop(i)
        massT.pop(i)
        deformationT.pop(i)


sortedCompressionUtilization  = [x for _, x in sorted(zip(CompressionUtilization, memberNameC))]
sortedTensionUtilization = [x for _, x in sorted(zip(TensionUtilization, memberNameT))]

sortedCompressionUtilization.reverse()
CompressionUtilization.reverse()
sortedTensionUtilization.reverse()
TensionUtilization.reverse()

dataOut = {
       "SectionNamesC": sortedCompressionUtilization,
       "CompressionUtilization": CompressionUtilization,
       "SectionNamesT": sortedTensionUtilization,
       "TensionUtilization": TensionUtilization
   }

SectionDataOutput = pd.DataFrame(dataOut)
SectionDataOutput.to_excel('Output.xlsx', index=False)

CScore = []
for i in range(len(massC)):
    CScore.append(massC[i]*massWeight+deformationC[i]*deformationWeight)

dataOutC = {
    "SectionNames": memberNameC,
    "Score": CScore,
    "Mass": massC,
    "Deformation": deformationC,
    "Utilization": utilizationC
}

dataOutC = pd.DataFrame(dataOutC)
dataOutC = dataOutC.sort_values("Score")

print(dataOutC)
dataOutC.to_excel('Output.xlsx', sheet_name='SortedByScoreCompression', index=False)

TScore = []
for i in range(len(massT)):
    TScore.append(massT[i]*massWeight+deformationT[i]*deformationWeight)

dataOutT = {
    "SectionNames": memberNameT,
    "Score": TScore,
    "Mass": massT,
    "Deformation": deformationT,
    "Utilization": utilizationT
}

dataOutT = pd.DataFrame(dataOutT)
dataOutT = dataOutT.sort_values("Score")

print(dataOutT)
dataOutT.to_excel('Output.xlsx', sheet_name='SortedByScoreTension', index=False)