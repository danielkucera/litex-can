import os
from migen import *

class CANFD(Module):
   
    def  __init__(self, platform, tx, rx):
        # Verilog sources from ProjectVault ORP
        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "packages"),
            "can_fd_frame_format.vhd",
            "id_transfer_pkg.vhd",
            "can_config_pkg.vhd",
            "can_constants_pkg.vhd",
            "can_types_pkg.vhd",
            "drv_stat_pkg.vhd",
            "unary_ops_pkg.vhd",
            "can_fd_register_map.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "common_blocks"),
            "endian_swapper.vhd",
            "dlc_decoder.vhd",
            "shift_reg_preload.vhd",
            "dff_arst.vhd",
            "mux2.vhd",
            "shift_reg_byte.vhd",
            "dff_arst_ce.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "can_core"),
            "control_counter.vhd",
            "reintegration_counter.vhd",
            "retransmitt_counter.vhd",
            "err_detector.vhd",
            "tx_shift_reg.vhd",
            "rx_shift_reg.vhd",
            "protocol_control_fsm.vhd",
            "protocol_control.vhd",
            "operation_control.vhd",
            "err_counters.vhd",
            "fault_confinement_fsm.vhd",
            "fault_confinement_rules.vhd",
            "fault_confinement.vhd",
            "crc_calc.vhd",
            "can_crc.vhd",
            "bit_stuffing.vhd",
            "bit_destuffing.vhd",
            "bus_traffic_counters.vhd",
            "trigger_mux.vhd",
            "can_core.vhd",
            library="ctu_can_fd_rtl"
        )

        self.can_tx = Signal()
        self.can_rx = Signal()

        self.comb += tx.eq(self.can_tx)
        self.comb += self.can_rx.eq(rx)

        self.specials += Instance("can_core",
            i_clk_sys = ClockSignal(),
            i_rx_data_wbs = self.can_rx,
            o_tx_data_wbs = self.can_tx,
        )
