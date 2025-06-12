from SteelCrossSection import getCrossSectionProperties
import Steel
import pandas as pd
import openpyxl

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

for i in range(len(memberType)):
    [A, Ix, Iy, Sx, Sy, Zx, Zy, J, Cw, rx, ry, xo, yo] = getCrossSectionProperties(memberType[i],d[i],b[i],t[i],w[i])
    numSymmetry = Steel.getNumSymmetry(memberType[i])

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

sortedCompressionUtilization  = [x for _, x in sorted(zip(CompressionUtilization, memberName))]
sortedTensionUtilization = [x for _, x in sorted(zip(TensionUtilization, memberName))]

for i in reversed(range(len(CompressionUtilization))):
    if CompressionUtilization[i] > 1:
        sortedCompressionUtilization.pop(i)
        CompressionUtilization.pop(i)
for i in reversed(range(len(TensionUtilization))):
    if TensionUtilization[i] > 1:
        sortedTensionUtilization.pop(i)
        TensionUtilization.pop(i)

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
