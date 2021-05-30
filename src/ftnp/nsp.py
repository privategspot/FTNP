class NSP:
    """
    Класс для расчета пространственных параметров
    сетей подвижной связи
    """

    def __init__(
        self,
        cell_sectors_count,
        radio_chan_per_sector
    ):
        # количество секторов в соте
        self.cell_sectors_count = cell_sectors_count

        # количество радиоканалов на 1 сектор
        self.radio_chan_per_sector = radio_chan_per_sector

    def calc_total_num_of_fq_chan(self, cluster_dim):
        """
        Расчет общего числа частотных каналов, выделяемых для развертывания сети.

        :param cluster_dim: размер кластера
        """

    def calc_minimum_bandwidth(self, bandwidth_occupied_by_one_fq_ch):
        """
        Минимальная полоса частот необходимая для развертывания сети

        :param bandwidth_occupied_by_one_fq_ch: полоса частот,занимаемая одним частотным каналом
        """

    def calc_total_num_of_conversation_chan(self, conversation_ch_num_per_carrier):
        """
        Общее число разговорных каналов в одном секторе

        :param conversation_ch_num_per_carrier: число разговорных каналов на одну несущую
        """

    def calc_telephone_load_per_sector(self, traffic_transmission_ch_num, call_blocking_admissible_prob):
        """
        Расчет телефонной нагрузки на один сектор соты

        :param traffic_transmission_ch_num: число  каналов  для передачи  трафика
        :param call_blocking_admissible_prob: допустимая  вероятность блокировки вызова
        """

    def calc_num_of_subscibers_per_cell(self, busy_hour_activity):
        """
        Расчет количества абонентов в одной ячейке

        :param busy_hour_activity: телефонная активность одного абонента в час наибольшей нагрузки
        """

    def calc_total_num_of_base_stations(self, subscribers_total_num):
        """
        Расчет общего числа базовых станций

        :param subscribers_total_num: общее число абонентов
        """

    def calc_base_station_coverage_radius(self, land_area):
        """
        Расчет радиуса зоны покрытия одной базовой станции

        :param land_area: площадь территории, на которой проектируется сеть
        """
