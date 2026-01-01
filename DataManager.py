import matplotlib.pyplot as plt
import numpy as np

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
