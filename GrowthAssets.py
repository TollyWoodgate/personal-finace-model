import numpy as np
import random as rnd

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
    