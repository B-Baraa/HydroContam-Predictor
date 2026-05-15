README.txt  
-----------

Title: Raster Data – Nitrate Concentration Maps from Groundwater Ecosystem Services Assessment in the MCGB

Authors: 
Borowiecka, Malgorzata
García Alcaraz, Mar del Mar  
Manzano Arellano, Marisol  

Contact:  
mar.alcaraz@upct.es

Description:  
This dataset contains the raster data used in the publication:  
“An application of the Ecosystem Services Assessment approach to the provision of groundwater for human supply and to support aquifer management,” submitted to *Hydrology* (MDPI), Special Issue on *Hydrological Modelling for the Sustainable Management of Water Resources in River Basins*.

The files correspond to the modelled nitrate concentration maps in the Medina del Campo Groundwater Body (MCGB) under different management scenarios and simulation years. Raster data were exported in CSV format and include spatially distributed nitrate concentrations (mg/L) for the upper and lower aquifers.

Contents:
- Each file is named according to the aquifer layer, scenario, and simulation year. For example:  
  - `Layer1_Scenario1A_2050.csv`  
  - `Layer3_Scenario2B_2350.csv`

- Each CSV file includes the following columns:  
  - `X`: X-coordinate (UTM)  
  - `Y`: Y-coordinate (UTM) 
  - `Z`: Z-coordinate (UTM)
  - Layer: Model layer number (1 = upper layer; 2 = intermediate layer;3 = lower layer)
  - `NO3`: Simulated nitrate concentration (mg/L)

X, Y, Z: Spatial coordinates in UTM (X: Easting, Y: Northing, Z: Elevation)

Coordinate system:  
- UTM Zone 30N, ED50 (EPSG:32630)

Usage Notes:  
- These data are intended for use in GIS or scientific analysis software.  
- Concentrations refer to the groundwater nitrate levels in mg/L.  
- Scenarios correspond to groundwater and fertilizer management alternatives defined in the associated manuscript.

License:  
This dataset is shared under the Creative Commons Attribution 4.0 International (CC BY 4.0) license.

Citation:  
Please cite this dataset as: 
Recommended citation for this dataset: Dataset for the publication Borowiecka et al. (2025)

Version: 1.0  
Date: 2025-04-29
