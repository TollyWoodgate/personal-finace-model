import matplotlib.pyplot as plt
import numpy as np
import random as rnd

class DataManager:
    def __init__(self, x_data, y_data, title="Data Plot", x_label="X-axis", y_label="Y-axis"):
        self.x_data = x_data
        self.y_data = y_data
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
      
    def save_plot(self, filename):
        plt.figure(figsize=(10, 6))
        plt.plot(self.x_data, self.y_data, marker='o', linestyle='-', color='b')
        plt.title(self.title)
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        plt.grid(True)
        plt.savefig(filename)
        plt.close()

    def get_statistics(self):
        mean = np.mean(self.y_data)
        median = np.median(self.y_data)
        std_dev = np.std(self.y_data)
        return {
            "mean": mean,
            "median": median,
            "std_dev": std_dev
        }


class Asset:
    def __init__(self, name, value = 100, up_move = 1.01, down_move = None, up_probability=0.5):
        self.name = name
        self.asset_type = self.__class__.__name__
        self.value = value
        self.up_move = up_move
        if down_move is None:
            self.down_move = 1 - (up_move - 1)
        else:
            self.down_move = down_move
        self.up_probability = up_probability
        self.value_history = [value]
        
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
    
    def timestep(self, periods=1):
        for _ in range(periods):
            value = self.generate_next_value()
            self.value_history.append(value)
            
    def plot_value_history(self, location="/figures/"):
        data_manager = DataManager(
            x_data=list(range(len(self.value_history))),
            y_data=self.value_history,
            title=f"Value History of {self.name}",
            x_label="Time Periods",
            y_label="Asset Value"
        )
        data_manager.save_plot(f"{location}{self.name}_value_history.png")
    
class GeometricAsset(Asset):
    def __init__(self, name, value, up_move, down_move, up_probability=0.5):
        super().__init__(name, value, up_move, down_move, up_probability)

    def generate_next_value(self):
        if rnd.random() <self.up_probability:
            self.value *= self.up_move
        else:
            self.value *= self.down_move
        return self.value
    
class ArithmeticAsset(Asset):
    def __init__(self, name, value, up_move = 1, down_move = 1, up_probability=0.5):
        super().__init__(name, value, up_move, down_move, up_probability)

    def generate_next_value(self):
        if rnd.random() <self.up_probability:
            self.value += self.up_move
        else:
            self.value -= self.down_move
        self.value_history.append(self.value)
        return self.value
    
