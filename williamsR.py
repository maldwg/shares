#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
class WilliamsR:
    """
    WilliamsR -> Williams R indicator
    Williams R is tries to determine overbought and oversold levels of an asset.\n
    \n Links:
        http://www.ta-guru.com/Book/TechnicalAnalysis/TechnicalIndicators/WilliamsAccumulationDistribution.php5\n
        https://www.investopedia.com/terms/w/williamsr.asp\n
        https://en.wikipedia.org/wiki/Williams_%25R\n
    """

    def __init__(self):
        self.df = pd.DataFrame()

    def info(self):
        """
        Provides basic information about the indicator
        """

        info = (
        "Williams R is tries to determine overbought and oversold levels of an asset.\n"

        "\n Links:\n"
                "http://www.ta-guru.com/Book/TechnicalAnalysis/TechnicalIndicators/WilliamsAccumulationDistribution.php5\n"
                "https://www.investopedia.com/terms/w/williamsr.asp\n"
                "https://en.wikipedia.org/wiki/Williams_%25R\n"
            )

        return info

    def get_value_df(self, df: pd.DataFrame, time_period: int = 14):
        """
        Get The expected indicator in a pandas dataframe.
        Args:
            df(pandas.DataFrame): pandas Dataframe with high, low, and close values\n
            time_period: look back time period
        Returns:
            pandas.DataFrame: new pandas dataframe adding WilliamsR as new column, preserving the columns which already exists\n
        """

        self.df["highest high"] = df["high"].rolling(
            window=time_period).max()
        self.df["lowest low"] = df["low"].rolling(
            window=time_period).min()
        df["WilliamsR"] = 100 * (df["close"] - self.df["highest high"]) /             (self.df["highest high"] - self.df["lowest low"])
        self.df = pd.DataFrame(None)

    def get_value_list(self, high_values: pd.Series, low_values: pd.Series, close_values: pd.Series, time_period: int = 14):
        """
        Get The expected indicator in a pandas series.\n\n
        Args:
            high_values(pandas.Series): 'High' values\n
            low_values(pandas.Series): 'Low' values\n
            close_values(pandas.Series): 'Close' values\n
            time_period: look back time period
        Returns:
            pandas.Series: A pandas Series of Williams R values
        """

        self.df = pd.DataFrame({
            "high": high_values,
            "low": low_values,
            "close": close_values
        })
        self.df["highest high"] = self.df["high"].rolling(
            window=time_period).max()
        self.df["lowest low"] = self.df["low"].rolling(
            window=time_period).min()
        williams_r_values = 100 * (self.df["close"] - self.df["highest high"]) /             (self.df["highest high"] - self.df["lowest low"])
        self.df = pd.DataFrame(None)
        return williams_r_values

