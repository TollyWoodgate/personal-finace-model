import GrowthAssets as ga

def main():
    path = "figures/"
    print("Financial Asset Growth Simulation")
    geometric_asset = ga.GeometricAsset("Stock Geo", 1000, 1.01, 0.99, 0.5)
    arithmetic_asset = ga.ArithmeticAsset("Bond Arith", 100, 1, 1, 0.5)
    time_periods = 5000
    geometric_asset.timestep(time_periods)
    arithmetic_asset.timestep(time_periods)
    geometric_asset.display_info()
    print()
    arithmetic_asset.display_info()
    geometric_asset.plot_value_history(path)
    arithmetic_asset.plot_value_history(path)

main()