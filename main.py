import ee
import geemap.core as geemap

# Authenticate and initialize the Earth Engine library
ee.Authenticate()   # This will open a browser window for authentication. This is usually not needed if you are logged in.

# ee.Initialize()   # This initializes the library with your credentials
ee.Initialize(project='Project-ID')

dataset = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterDate(
    '2021-05-01', '2021-06-01'
)

# Applies scaling factors.
def apply_scale_factors(image):
  optical_bands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
  thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)
  return image.addBands(optical_bands, None, True).addBands(
      thermal_bands, None, True
  )

dataset = dataset.map(apply_scale_factors)

visualization = {
    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
    'min': 0.0,
    'max': 0.3,
}

m = geemap.Map()
m.set_center(-114.2579, 38.9275, 8)
m.add_layer(dataset, visualization, 'True Color (432)')
m


# --------------------------------------------------------------------------------------------------------------------------------



# import ee
# import geemap.core as geemap

# Authenticate and initialize the Earth Engine library
ee.Initialize(project='Project-ID')

# Load Landsat 8 Collection 2 Level 2 dataset
dataset = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2').filterDate(
    '2021-05-01', '2021-06-01'
)

# Applies scaling factors and computes NDMI & NBR
def apply_indices(image):
    optical_bands = image.select('SR_B.').multiply(0.0000275).add(-0.2)
    thermal_bands = image.select('ST_B.*').multiply(0.00341802).add(149.0)

    # Compute NDMI (Moisture Index)
    ndmi = image.normalizedDifference(['SR_B5', 'SR_B6']).rename('NDMI')

    # Compute NBR (Burn Ratio)
    nbr = image.normalizedDifference(['SR_B5', 'SR_B7']).rename('NBR')

    return image.addBands(optical_bands, None, True).addBands(
        thermal_bands, None, True
    ).addBands(ndmi).addBands(nbr)

# Apply processing function
dataset = dataset.map(apply_indices)

# Define visualization parameters
true_color_viz = {'bands': ['SR_B4', 'SR_B3', 'SR_B2'], 'min': 0.0, 'max': 0.3}
ndmi_viz = {'min': -1, 'max': 1, 'palette': ['blue', 'white', 'green']}
nbr_viz = {'min': -1, 'max': 1, 'palette': ['red', 'white', 'green']}

# Create a map
m = geemap.Map()
m.set_center(-114.2579, 38.9275, 8)

# Add True Color, NDMI, and NBR layers
m.add_layer(dataset.select('SR_B4', 'SR_B3', 'SR_B2'), true_color_viz, 'True Color (432)')
m.add_layer(dataset.select('NDMI'), ndmi_viz, 'NDMI (Moisture Index)')
m.add_layer(dataset.select('NBR'), nbr_viz, 'NBR (Burn Ratio)')
m
