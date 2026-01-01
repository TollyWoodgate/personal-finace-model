

def sim10(path="figures/", data_manager=None):
    print("Financial Asset Growth Simulation")
    DataManager = dm.DataManager()
    geo_data = []
    arith_data = []
    for _ in range(10):
        geometric_asset = ga.GeometricAsset("Stock Geo", 1000, 1.01, 0.99, 0.55)
        arithmetic_asset = ga.ArithmeticAsset("Bond Arith", 100, 1, 1, 0.55)
        time_periods = 5000 
        geometric_asset.timestep(time_periods)
        arithmetic_asset.timestep(time_periods)
        geo_data.append(geometric_asset.get_value_history())
        arith_data.append(arithmetic_asset.get_value_history())
        
    data_manager.plot_multiple_assets(
        geo_data,
        title="Geometric Asset Value Histories",
        x_label="Time Periods",
        y_label="Asset Value",
        filename=f"{path}geometric_assets.png"
    )
    
    data_manager.plot_multiple_assets(
        arith_data,
        title="Arithmetic Asset Value Histories",
        x_label="Time Periods",
        y_label="Asset Value",
        filename=f"{path}arithmetic_assets.png"
    )

def sim_futures(path="figures/", data_manager=None):

    print("Financial Futures Asset Growth Simulation")
    
    futures_data = []
    
    futures_asset = ga.GeometricAsset("Futures", 500, 1.02, 0.98, 0.55)
    time_periods = 2000
    futures_asset.timestep(time_periods)
    
    data_manager.plot(
        futures_asset.get_history(),
        title="Futures Asset Value History",
        x_label="Time Periods",
        y_label="Asset Value",
        filename=f"{path}future_asset.png",
        logy=True
    )
    
    futures_data.append(futures_asset.get_history())
    tempdata = futures_asset.simulate_future_values(periods=2000, simulations=25)
    
    futures_data.extend(tempdata)
    
    data_manager.plot_multiple_assets(
    futures_data,
    title="Futures Asset Value Histories",
    x_label="Time Periods",
    y_label="Log Asset Value",
    filename=f"{path}futures_assets.png",
    logy=True
    )

import GrowthAssets as ga
import DataManager as dm
def main():
    DataManager = dm.DataManager()
    #sim10(data_manager=DataManager)
    sim_futures(data_manager=DataManager)
if __name__ == "__main__":
    main()