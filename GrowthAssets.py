import matplotlib.pyplot as plt
import numpy as np
import random as rnd

class DataManager:
    _instance = None
    # Should handle arbitrary data plotting and statistics
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DataManager, cls).__new__(cls)
        return cls.instance

    def plot(self, data, title="Data Plot", x_label="X-axis", y_label="Y-axis", filename=None, logy=False, logx=False):
        """
        Plot a single asset value history.
        Args:
            data (2D list): Contains the value and time history of the asset.
            title (str): Title of the plot.
            x_label (str): Label for the x-axis.
            y_label (str): Label for the y-axis.
            filename (str): Path to save the plot image.
            logy (bool): Whether to use logarithmic scale for y-axis.
            logx (bool): Whether to use logarithmic scale for x-axis.
        """
        plt.figure(figsize=(10, 6))
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        if logy:
            data[0] = self.convert_linear_to_log(data[0], exponent=10)
        if logx:
            data[1] = self.convert_linear_to_log(data[1], exponent=10)
        plt.plot(data[1], data[0], marker='o', linestyle='-', color='b')
        plt.savefig(filename)
        plt.close()

    def plot_multiple_assets(self, assets_data, title, x_label, y_label, filename, logy=False, logx=False):
        """
        Plot multiple asset value histories on the same graph.
        Args:
            assets_data (list of 2D lists): Each 2Dlist contains the value and time history of an asset.
            title (str): Title of the plot.
            x_label (str): Label for the x-axis.
            y_label (str): Label for the y-axis.
            filename (str): Path to save the plot image.
            logy (bool): Whether to use logarithmic scale for y-axis.
            logx (bool): Whether to use logarithmic scale for x-axis.
        """
        plt.figure(figsize=(10, 6))
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(True)
        for data in assets_data:
            if logy:
                data[0] = self.convert_linear_to_log(data[0], exponent=10)
            if logx:
                data[1] = self.convert_linear_to_log(data[1], exponent=10)
            plt.plot(data[1], data[0], linestyle='-', alpha=0.7)
        plt.savefig(filename)
        plt.close()

    def get_statistics(self, y_data):
        mean = np.mean(y_data)
        median = np.median(y_data)
        std_dev = np.std(y_data)
        return {
            "mean": mean,
            "median": median,
            "std_dev": std_dev
        }

    def convert_linear_to_log(self, data, exponent=10):
        return [np.log(value)/np.log(exponent) for value in data]
    
    def rolling_average(self, y_data, window_size=5):
        return np.convolve(y_data, np.ones(window_size)/window_size, mode='valid')

class Asset:
    def __init__(self, name, value = 100, up_move = 1.01, down_move = None, up_probability=0.5):
        self.name = name
        self.asset_type = self.__class__.__name__
        self.value = value
        self.time = 0
        self.up_move = up_move
        if down_move is None:
            self.down_move = 1 - (up_move - 1)
        else:
            self.down_move = down_move
        self.up_probability = up_probability
        self.value_history = [value]
        self.time_history = [self.time]
    
    def get_history(self):
        return [self.value_history, self.time_history]
    
    def get_value_history(self):
        return self.value_history

    def get_time_history(self):
        return self.time_history

    def display_info(self):
        print(f"Asset Name: {self.name}")
        print(f"Asset Type: {self.asset_type}")
        print(f"Initial Value: {self.value_history[0]}")
        print(f"Current Value: {self.value}")
        print(f"Up Move: {self.up_move}")
        print(f"Down Move: {self.down_move}")
        print(f"Up Probability: {self.up_probability}")

    def generate_next_value(self):
        raise NotImplementedError("This method should be implemented by subclasses.")

    def timestep(self, periods=1, value=None, time=None, save_history=True):
        """
        Simulate the asset value over a number of time periods.
        Args:
            periods (int): Number of time periods to simulate.
            value (float): Starting value for the simulation. If None, uses current asset value.
            time (int): Starting time for the simulation. If None, uses current asset time.
        Returns:
            value_history (list): Simulated asset values over the periods.
            time_history (list): Corresponding time periods.
        """
        if value is None:
            value = self.value
        if time is None:
            time = self.time
        value_history = []
        time_history = []
        for _ in range(periods):
            value, time = self.generate_next_value(value, time)
            value_history.append(value)
            time_history.append(time)
        if save_history:
            self.value = value
            self.time = time
            self.value_history.extend(value_history)
            self.time_history.extend(time_history)
        return value_history, time_history
            
    def simulate_future_values(self, periods=100, simulations=10):
        """
        Simulate multiple future asset value paths.
        Args:
            periods (int): Number of time periods to simulate for each path.
            simulations (int): Number of simulation paths to generate.
        Returns:
            simulation_results (2D list): List of simulated value histories.
        """
        simulation_results = []
        for _ in range(simulations):
            temp_value = self.value
            temp_time = self.time
            temp_value_history, temp_time_history = [temp_value], [temp_time]
            
            temp_value_history, temp_time_history = self.timestep(periods=periods, value=temp_value, time=temp_time, save_history=False)

            simulation_results.append([temp_value_history, temp_time_history])

        return simulation_results
    
class GeometricAsset(Asset):
    def __init__(self, name, value, up_move, down_move, up_probability=0.5):
        super().__init__(name, value, up_move, down_move, up_probability)

    def generate_next_value(self, value, time):
        """
        Generate the next asset value based on geometric growth.
        Args:
            value (float): Current asset value.
            time (int): Current time period.
        Returns:
            value (float): Updated asset value.
            time (int): Updated time period.
        """
        if rnd.random() <self.up_probability:
            value *= self.up_move
        else:
            value *= self.down_move
        time += 1
        return value, time

class ArithmeticAsset(Asset):
    def __init__(self, name, value, up_move = 1, down_move = 1, up_probability=0.5):
        super().__init__(name, value, up_move, down_move, up_probability)

    def generate_next_value(self, value, time):
        """
        Generate the next asset value based on arithmetic growth.
        Args:
            value (float): Current asset value.
            time (int): Current time period.
        Returns:
            value (float): Updated asset value.
            time (int): Updated time period.
        """
        if rnd.random() <self.up_probability:
            value += self.up_move
        else:
            value -= self.down_move
        time += 1
        return value, time
    