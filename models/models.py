hue = 20.26
sat = 132

# if Clay prediction is available from lab report, use it, if not use this eq to predict clay from image saturation 
clay = round((-0.0853*sat) + 37.1,2)
print("Clay (%) : ", clay)

# SOC to SOM conversion function 
def SOM (SOC):
	SOM = round(SOC * 1.72,2)
	if SOM > 10:
		SOM = 10
	return SOM

# SOC (%) to SOC (tC/ha)
def SOCWeight (depth, BD, SOC):
	depthC = depth*2.54
	socWeight = round((SOC*0.01) * ((BD*(depthC/100)*10000)),2)
	return socWeight


# SOC eq 1 ==> Original eq. Textures used to train include Fine sandy loam and Silt loam 
SOC1 = round((0.0772*hue) + 1.72, 2)

if SOC1 > 5.8:
	SOC1 = 5.8	

print("SOC (%) Prediction 1: ", SOC1)
print("SOM (%) Prediction 1: ", SOM(SOC1))
print("________________________________")


# SOC eq 2 ==> Updated eq from Dan's Farm. Textures used to train include Silt clay loam and Silt loam.
# if clay percent is available use multiple regression model, if not -- use simple regression 

try:
	SOC2 = round((0.05262*hue) + (0.11041*clay) + -2.76983, 2)
except:
	SOC2 = round((0.05902*hue) + -0.04238, 2)
print("SOC (%) Prediction 2: ", SOC2)
print("SOM (%) Prediction 2: ", SOM(SOC2))
print("________________________________")

# SOC eq 3 = Average of eq 1 and eq 2 predictions 

SOC3 = round(((SOC1+SOC2)/2),2)
print("SOC (%) Prediction 3: ", SOC3)
print("SOM (%) Prediction 3: ", SOM(SOC3))
print("________________________________")

# BULK Density eq 1 ==> predict BD using clay and saturation inputs 

BD = round((0.0129651*clay) + (0.0030006*sat) + 0.4401499,2)
print("Bulk Density (g/cm3): ", BD)

# SOC tons Carbon per hectare 
# input depth of soil sample in inches 
depth = 6
print("SOC Prediction 3 (tC/ha): ", SOCWeight(depth, BD, SOC3))