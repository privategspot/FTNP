from ftnp.cluster import Cluster
from ftnp.nsp import NSP
from ftnp.leb import LEB


class MobileNetworkEngineer:
    
    def __init__(self, initial_data, cluster_calculator: Cluster, nsp: NSP, leb: LEB):
        self.initial_data = initial_data
        self.cluster_calculator = cluster_calculator
        self.nsp = nsp
        self.leb = leb

    def _determine_cluster_size(self):
        cc = self.cluster_calculator
        sn_failure_prob = cc.get_signal_to_noise_failure_probability()
        main_rec_chan_deviation = cc.get_main_reception_channel_deviation()
        interfering_signals_attenuation = cc.get_attenuation_of_interfering_signals()
        main_rec_chan_relative_total_interfer = cc.get_betta()
        return {
            "Вероятность невыполнения требований по отношению сигнал/шум": sn_failure_prob,
            "Отклонения велечины уровня суммарной помехи по основному каналу приема": main_rec_chan_deviation,
            "Ослабление мешающих сигналов": interfering_signals_attenuation,
            "Относительный уровень суммарной помехи по основному канала приема": main_rec_chan_relative_total_interfer
        }

    def _calc_nsp_spatial_parameters(self):
        nsp = self.nsp
        i = self.initial_data
        bs_coverage_radius = nsp.calc_base_station_coverage_radius(i["land_area"])
        min_bandwidth = nsp.calc_minimum_bandwidth(i["one_fq_ch_bandwith"])
        subscribers_per_cell = nsp.calc_num_of_subscibers_per_cell(i["busy_hour_activity"])
        sector_telephone_load = nsp.calc_telephone_load_per_sector()
        fq_chan_total = nsp.calc_total_num_of_fq_chan()
        bs_total =  nsp.calc_total_num_of_base_stations()
        conv_chan_total = nsp.calc_total_num_of_conversation_chan(i["conversation_ch_num_per_carrier"])
        return {
            "Минимальная полоса частот необходимая для развертывания сети": min_bandwidth,
            "Общее число частотных каналов, выделяемых для развертывания сети": fq_chan_total,
            "Количество абонентов в одной ячейке": subscribers_per_cell,
            "Телефонная нагрузка на один сектор соты": sector_telephone_load,
            "Общее число разговорных каналов в одном секторе": conv_chan_total,
            "Общее число базовых станций": bs_total,
            "Радиус зоны покрытия одной базовой станции": bs_coverage_radius,
        }

    def _conduct_leb_assessment(self):
        leb = self.leb
        i = self.initial_data
        line_loss_margin = leb.compute_line_loss_margin(
            i["building_penetraition_loses"],
            i["subscriber_body_loses"],
            i["location_coverage"]
        )
        total_loss = leb.compute_total_losses(
            i["eqv_isotropically_radiated_pow"],
            i["useful_signal_strength"],
            line_loss_margin
        )
        eirp = leb.compute_EIRP(
            i["transmitter_output_power"],
            i["transmitter_antenna_gain"],
            i["transmission_antenna_feeder_loss"],
            i["duplex_filter_loss"],
            i["diplexer_loss"],
            i["radiated_power_reduction_coefficient"]
        )
        receiver_sensitivity = leb.compute_receiver_sensitivity(
            i["bandwidth"],
            i["power_to_noise_power_ratio"],
            i["receiver_noise_figure"]
        )
        useful_sign_req_power = leb.compute_useful_signal_required_power(
            receiver_sensitivity,
            i["transmitter_antenna_gain"],
            i["transmission_antenna_feeder_loss"],
            i["diplexer_loss"]
        )
        antenna_height_correction_factor = leb.compute_antenna_height_correction_factor(
            i["radio_frequency"],
            i["receiving_antenna_height"],
            i["city_type"]
        )
        bs_as_losses = leb.COST231_Hata(
            antenna_height_correction_factor,
            i["radio_frequency"],
            i["transmitting_antenna_height"],
            i["distance_between_antennas"],
            i["city_type"]
        )
        return {
            "Запас по потерям в линии": line_loss_margin,
            "Суммарные потери радиосигнала при распространении радиоволн от базовой станции к абонентской станции": total_loss,
            "Эквивалентная изотропно излучаемая мощность ЭИИМ": eirp,
            "Чувствительность приемника": receiver_sensitivity,
            "Необходимая мощность полезного сигнала для обеспечения приема в случае 50% местоположений": useful_sign_req_power,
            "Поправочный коэффициент для высоты антенны подвижного объекта, зависящий от типа местности": antenna_height_correction_factor,
            "Потери сигнала от базовой станции (БС) до абонентской станции (АС)": bs_as_losses,
        }

    def report(self):
        result = {}
        result.update(self._determine_cluster_size())
        result.update(self._calc_nsp_spatial_parameters())
        result.update(self._conduct_leb_assessment())
        return result
