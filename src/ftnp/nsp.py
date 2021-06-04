import numpy as np


class NSP:
    """
    Класс для расчета пространственных параметров
    сетей подвижной связи
    """

    def __init__(
        self,
        cell_sectors_count,
        radio_chan_per_sector,
        cluster_dim,
        traffic_transmission_ch_num,
        call_blocking_admissible_prob,
        subscribers_total_num
    ):
        # количество секторов в соте
        self.cell_sectors_count = cell_sectors_count

        # количество радиоканалов на 1 сектор
        self.radio_chan_per_sector = radio_chan_per_sector
        self.cluster_dim = cluster_dim
        self.traffic_transmission_ch_num = traffic_transmission_ch_num
        self.call_blocking_admissible_prob = call_blocking_admissible_prob,
        self.subscribers_total_num = subscribers_total_num

    def calc_total_num_of_fq_chan(self):
        """
        Расчет общего числа частотных каналов, выделяемых для развертывания сети.
        """
        number_channels_per_sector = self.cell_sectors_count * self.cluster_dim * 2
        return number_channels_per_sector

    def calc_minimum_bandwidth(self, bandwidth_occupied_by_one_fq_ch):
        """
        Минимальная полоса частот необходимая для развертывания сети

        :param bandwidth_occupied_by_one_fq_ch: полоса частот,занимаемая одним частотным каналом
        """
        n = self.calc_total_num_of_fq_chan()
        delta_F = n * bandwidth_occupied_by_one_fq_ch
        return delta_F

    def calc_total_num_of_conversation_chan(self, conversation_ch_num_per_carrier):
        """
        Общее число разговорных каналов в одном секторе

        :param conversation_ch_num_per_carrier: число разговорных каналов на одну несущую
        """
        number_of_conversation_channels = conversation_ch_num_per_carrier  # <<<<< nc???
        return number_of_conversation_channels

    def calc_telephone_load_per_sector(self):
        """
        Расчет телефонной нагрузки на один сектор соты
        """
        traffic_transmission_ch_num = self.traffic_transmission_ch_num
        call_blocking_admissible_prob = self.call_blocking_admissible_prob
        if call_blocking_admissible_prob <= np.sqrt(2/(traffic_transmission_ch_num * np.pi)):
            A = traffic_transmission_ch_num * int(
                1 - np.sqrt(1 - (call_blocking_admissible_prob * np.sqrt(
                    (traffic_transmission_ch_num * np.pi) /2  ))**(
                        1/traffic_transmission_ch_num)
                    )
                )
            return A
        elif call_blocking_admissible_prob > np.sqrt(2/(traffic_transmission_ch_num * np.pi)):
            A = traffic_transmission_ch_num + np.sqrt(
                np.pi/2 + 2 * traffic_transmission_ch_num * np.log10(
                    call_blocking_admissible_prob * np.sqrt(
                        (traffic_transmission_ch_num * np.pi)/2))) - np.sqrt(np.pi/2)
            return A

    def calc_num_of_subscibers_per_cell(self, busy_hour_activity):
        """
        Расчет количества абонентов в одной ячейке

        :param busy_hour_activity: телефонная активность одного абонента в час наибольшей нагрузки
        """
        A = self.calc_telephone_load_per_sector()
        N_ab = A / busy_hour_activity * self.cluster_dim
        return N_ab

    def calc_total_num_of_base_stations(self):
        """
        Расчет общего числа базовых станций
        """
        N_bc = self.subscribers_total_num / (25000 + 3000 * 7)
        return N_bc 

    def calc_base_station_coverage_radius(self, land_area):
        """
        Расчет радиуса зоны покрытия одной базовой станции

        :param land_area: площадь территории, на которой проектируется сеть
        """
        N_bc = self.calc_total_num_of_base_stations()
        R_c = np.sqrt((2/(3 / np.sqrt(3)) * (land_area / N_bc)))
        return R_c
