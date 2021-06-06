from typing import Tuple
from enum import Enum
import numpy as np


class CityType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


class LEB:
    """
    Класс для оценки энергетического бюджета линий
    """

    def compute_total_losses(
        self,
        eqv_isotropically_radiated_pow: Tuple[float, float],   # 𝑃БСизл, 𝑃АСизл
        useful_signal_strength: Tuple[float, float],    # 𝑃𝑚𝑖𝑛−БС, 𝑃𝑚𝑖𝑛−АС
        line_loss_margin: Tuple[float, float],  # 𝑍БС−АС, 𝑍АС−БС
    ) -> Tuple[float, float]:
        """
        Суммарные потери радиосигнала при распространении радиоволн от 
        базовой станции к абонентской станции

        :param eqv_isotropically_radiated_pow:
            эквивалентная изотропно излучаемая мощность БС и АС соответственно
        :param useful_signal_strength:
            необходимая мощность полезного сигнала для 50% вероятности обеспечения связью
        :param line_loss_margin: запас по потерям в линии
        """
        temp1 = eqv_isotropically_radiated_pow[0] - useful_signal_strength[1] - line_loss_margin[0]
        temp2 = eqv_isotropically_radiated_pow[1] - useful_signal_strength[0] - line_loss_margin[1]
        return (temp1, temp2)

    def compute_line_loss_margin(
        self,
        building_penetraition_loses,    # 𝐿𝑏
        subscriber_body_loses,  # 𝑊𝑎
        location_coverage_location, # 𝐶𝐼
    ):
        """
        Запас по потерям в линии

        :param building_penetraition_loses:
            потери, связанные с проникновением волны в здание
        :param subscriber_body_loses: потери в теле абонента
        :param location_coverage_location:
            поправка, связанная с требуемым процентом покрытия местоположений
        """
        Z = building_penetraition_loses + subscriber_body_loses + location_coverage_location
        return Z

    def compute_receiver_sensitivity(
        self,
        bandwidth,  # 𝑓𝑘
        power_to_noise_power_ratio, #   C/N
        receiver_noise_figure,  # 𝑁𝐹
    ):
        """
        Чувствительность  приемника

        :param bandwidth: 
            ширина полосы частот, занимаемая одним
            частотным каналомв системе GSM
        :param power_to_noise_power_ratio:
            отношение мощности несущей к мощности шума,
            требуемое на входе демодулятора
        :param receiver_noise_figure: коэффициент шума приемника
        """
        P = -174 + 10 * np.log10(bandwidth) + power_to_noise_power_ratio + receiver_noise_figure
        return P

    def compute_useful_signal_required_power(
        self,
        receiver_sensitivity,   # 𝑃ч
        transmitter_antenna_gain,    # 𝐺И
        transmission_antenna_feeder_loss,   # 𝜂ф
        diplexer_loss,  #   𝜂дип
    ):
        """
        Необходимая мощность полезного сигнала
        для обеспечения приема в случае 50% местоположений

        :pararm receiver_sensitivity: Чувствительность приемника
        :param transmitter_antenna_gain:
            коэффициент усиления передающей антенны относительно изотропной антенны
        :param transmission_antenna_feeder_loss: потери в дуплексном фильтре
        :param diplexer_loss: потери в диплексоре
        """
        P_min = receiver_sensitivity - transmitter_antenna_gain +\
            transmission_antenna_feeder_loss + diplexer_loss
        return P_min

    def compute_EIRP(
        self,
        transmitter_output_power,   # P
        transmitter_antenna_gain,    # 𝐺И
        transmission_antenna_feeder_loss,   # 𝜂ф
        duplex_filter_loss, # 𝜂дф
        diplexer_loss,  #   𝜂дип
        radiated_power_reduction_coefficient    # 𝐹(𝜙,Δ)
    ):
        """
        Эквивалентная изотропно излучаемая мощность ЭИИМ

        :param transmitter_output_power: мощность на выходе передатчика
        :param transmitter_antenna_gain: 
            коэффициент усиления передающей антенны относительно изотропной антенны
        :param transmission_antenna_feeder_loss:
            потери в фидере передающей антенны
        :param duplex_filter_loss:
            потери в дуплексном фильтре
        :param diplexer_loss: потери в диплексоре
        :param radiated_power_reduction_coefficient: 
            коэффициент, учитывающий снижение излучаемой мощности,
            обусловленное диаграммой направленности.
            В главном направлении этот коэффициент равен нулю.
        """
        P = transmitter_output_power + transmitter_antenna_gain +\
            radiated_power_reduction_coefficient +\
            transmission_antenna_feeder_loss + duplex_filter_loss +\
            diplexer_loss
        return P

    def compute_antenna_height_correction_factor(
        self,
        radio_frequency,    # f
        receiving_antenna_height, # hпрм
        city_type: CityType
    ):
        """
        Поправочный коэффициент для высоты антенны подвижного
        объекта, зависящий от типа местности

        :param radio_frequency: частота радиосигнала
        :param receiving_antenna_height: высота приемной антенны
        :param city_type: размер города
        """
        if city_type == CityType.SMALL or city_type == CityType.MEDIUM:
            A = (1.1 * np.log10(radio_frequency) - 0.7) *\
                receiving_antenna_height - ((1.56 * np.log10(radio_frequency) -\
                0.8))
        elif city_type == CityType.LARGE:
            A = 3.2 * (np.log10(11.75 * receiving_antenna_height)) ** 2- 4.97
        return A

    def COST231_Hata(
        self,
        antenna_height_correction_factor,   # 𝐴(hпрм)
        radio_frequency,    # f
        transmitting_antenna_height,    # hпрд
        distance_between_antennas, # d
        city_type: CityType,
    ):
        """
        Метод для расчета потерь сигнала от базовой станции (БС)
        до абонентской станции (АС) на основе модели COST231-Хата
        
        :param antenna_height_correction_factor:
            Поправочный коэффициент для высоты антенны подвижного объекта,
            зависящий от типа местности
        :param radio_frequency: частота радиосигнала
        :param transmitting_antenna_height: высота передающей антенны
        :param distance_between_antennas: расстояние между антеннами
        :param city_type: размер города
        """
        if city_type == CityType.SMALL or city_type == CityType.MEDIUM:
            C = 0
        elif city_type == CityType.LARGE:
            C = 3
        L = 46.3 + 33.91 * np.log10(radio_frequency) - 13.821 *\
            np.log10(transmitting_antenna_height) -\
            antenna_height_correction_factor +\
            (44.9 - 6.55 * np.log10(transmitting_antenna_height)) *\
            np.log10(distance_between_antennas) + C
        return L
