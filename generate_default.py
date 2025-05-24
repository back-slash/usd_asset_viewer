from pxr import Usd, UsdGeom

# Create a new USD stage
stage = Usd.Stage.CreateNew("default.usda")

# Define a cube at the root prim
UsdGeom.Cube.Define(stage, '/Cube')

# Save the stage to disk
stage.GetRootLayer().Save()