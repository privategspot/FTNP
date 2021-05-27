import math as m
import numpy as np
from scipy.integrate import quad


class Cluster:
    
    def __init__(self, cluster_dim, tetta, cell_sectors_num) -> None:
        self.cluster_dim = cluster_dim
        self.tetta = tetta
        self.cell_sectors_num = cell_sectors_num # --> M

    def get_attenuation_of_interfering_signals(self):
        """Ослабление мешающих сигналов q """
        q = m.sqrt(3 * self.cluster_dim)
        return q
    
    def derive_betta_i(self):
        q = self.get_attenuation_of_interfering_signals()
        if self.cell_sectors_num == 3:
            return (2, (q + 0.7) ** (-4), q ** (-4))
        elif self.cell_sectors_num == 6:
            return (1, (q + 1) ** (-4))
    
    def get_main_reception_channel_deviation(self):
        """тетта^2 с индексом e,отклонения велечины уровня суммарной помехи по основному каналу приема"""
        betta_i = self.derive_betta_i()
        sum_one = 0
        sum_two = 0
        for i in range(1, betta_i[0] + 1):
            sum_one += betta_i[i] ** 2
            sum_two += betta_i[i]
        sum_two = sum_two ** 2
        tetta_e_squared = (1/0.053) * m.log10(set(1 + int(np.exp(0.053 * self.tetta **2 ) - 1 ) * sum_one / sum_two))
        return tetta_e_squared

    def get_betta(self, betta_i,):
        """относительный уровень суммарной помехи по основному канала приема"""
        sum_b = 0
        for i in range(betta_i[0]-1,1):
            sum_b = betta_i[i]
        tetta = self.get_main_reception_channel_deviation()
        betta = np.exp(set(0.053 * ((tetta**2 - tetta**2) / 2)))
        return betta
    
    def derive_x1(self):
        tetta = self.get_signal_to_noise_failure_probability()
        b = self.get_betta   
        x1 = (10 * m.log10(1/b) - 9) / m.sqrt(tetta**2 + tetta**2)
        return x1

    def get_signal_to_noise_failure_probability(self):

        def integrand(x, n):
            return np.exp((-x**2) / 2) * n
    
        pi = 3.14
        x1 = self.derive_x1()
        I = quad(integrand, x1, np.inf, args=(1,))[0]
        return int(1/m.sqrt(2*pi)*I) * 100


if __name__ == "__main__":
    pass