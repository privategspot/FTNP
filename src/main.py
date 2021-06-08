import json
from app import App
from app.controller import ConsoleController

from app.model import MobileNetworkEngineer
from app.view import ConsoleView
from ftnp.cluster import Cluster
from ftnp.leb import LEB
from ftnp.nsp import NSP


def main():
    """
    mn - консольная утилита для расчета основных характеристик
    сети начального приближения (частотно-территориальное планирование)
    стандарта LTE.

    Для работы с программой необходимо создать файл JSON с исходными данными.
    Путь к файлу передается как обязательный аргумент командной строки.

    Ниже приведены данные, которые должны быть представлены в файле.
    Все значения должны быть представлены на верхнем уровне файла.

    'land_area' - площадь зоны обслуживания\n
    'one_fq_ch_bandwith' - полоса частот,занимаемая одним частотным каналом\n
    'busy_hour_activity' - телефонная активность одного абонента в час наибольшей нагрузки\n
    'conv_ch_per_carriercity_type' - число разговорных каналов на одну несущую\n
    'building_penetraition_loses' - потери, связанные с проникновением волны в здание\n
    'subscriber_body_loses' - потери в теле абонента\n
    'location_coverage' - поправка, связанная с требуемым процентом покрытия местоположений\n
    'bandwidth' - ширина полосы частот, занимаемая однимчастотным каналомв системе GSM\n
    'power_to_noise_power_ratio' - отношение мощности несущей к мощности шума,требуемое на входе демодулятора\n
    'receiver_noise_figure' - коэффициент шума приемника\n
    'eqv_isotropically_radiated_pow' - эквивалентная изотропно излучаемая мощность БС и АС соответственно\n
    'useful_signal_strength' - необходимая мощность полезного сигнала для 50% вероятности обеспечения связью\n
    'transmitter_output_power' - выходная мощность передающей антенны\n
    'transmitter_antenna_gain' - коэффициент усиления передающей антенны относительно изотропной антенны\n
    'transmission_antenna_feeder_loss' - потери в фидере передающей антенны\n
    'duplex_filter_loss' - потери в дуплексном фильтре\n
    'diplexer_loss' - потери в диплексоре\n
    'radiated_power_reduction_coefficient' - коэффициент, учитывающий снижение
    излучаемой мощности, обусловленное диаграммой направленности\n
    'radio_frequency' -  частота радиосигнала\n
    'receiving_antenna_height' - высота приемной антенны\n
    'transmitting_antenna_height' - высота передающей антенны\n
    'distance_between_antennas' - расстояние между антеннами\n
    'city_type' - размер города\n
    """

    with open("./initial.json") as f:
        initial = json.load(f)

    cluster_calculator = Cluster(
        initial["cluster_dim"],
        initial["tetta"],
        initial["cell_sectors_num"],
        initial["signal_to_noise_ratio"]
    )
    nsp = NSP(
        initial["cell_sectors_num"],
        initial["sector_radio_chan"],
        initial["cluster_dim"],
        initial["traffic_transmission_ch_num"],
        initial["call_blocking_admissible_prob"],
        initial["subscribers_total"]
    )
    leb = LEB()
    mne = MobileNetworkEngineer(initial, cluster_calculator, nsp, leb)
    app = App(mne, ConsoleView(), ConsoleController())
    app.run()


if __name__ == "__main__":
    main()
