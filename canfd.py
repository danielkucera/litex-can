import os
from migen import *

from litex.soc.interconnect.csr import *
from litex.soc.interconnect import wishbone

class CANFD(Module, AutoCSR):
   
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
            "rst_sync.vhd",
            "clk_gate.vhd",
            "inf_ram_wrapper.vhd",
            "sig_sync.vhd",
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

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "memory_registers", "generated"),
            "can_registers_pkg.vhd",
            "control_registers_reg_map.vhd",
            "cmn_reg_map_pkg.vhd",
            "test_registers_reg_map.vhd",
            "address_decoder.vhd", # badly included
            "memory_reg.vhd", # badly included
            "data_mux.vhd", # badly included
            "access_signaler.vhd", # badly included
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "memory_registers"),
            "memory_registers.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "rx_buffer"),
            "rx_buffer.vhd",
            "rx_buffer_fsm.vhd",
            "rx_buffer_pointers.vhd",
            "rx_buffer_ram.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "txt_buffer"),
            "txt_buffer.vhd",
            "txt_buffer_fsm.vhd",
            "txt_buffer_ram.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "tx_arbitrator"),
            "tx_arbitrator.vhd",
            "tx_arbitrator_fsm.vhd",
            "priority_decoder.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "frame_filters"),
            "frame_filters.vhd",
            "bit_filter.vhd",
            "range_filter.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "interrupt_manager"),
            "int_manager.vhd",
            "int_module.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "prescaler"),
            "prescaler.vhd",
            "bit_time_cfg_capture.vhd",
            "synchronisation_checker.vhd",
            "bit_segment_meter.vhd",
            "bit_time_counters.vhd",
            "bit_segment_meter.vhd",
            "bit_time_counters.vhd",
            "segment_end_detector.vhd",
            "bit_time_fsm.vhd",
            "trigger_generator.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src", "bus_sampling"),
            "bus_sampling.vhd",
            "trv_delay_meas.vhd",
            "data_edge_detector.vhd",
            "ssp_generator.vhd",
            "tx_data_cache.vhd",
            "bit_err_detector.vhd",
            "sample_mux.vhd",
            library="ctu_can_fd_rtl"
        )

        platform.add_sources(os.path.join(os.path.abspath(os.path.dirname(__file__)), "ctucanfd_ip_core", "src"),
            "can_top_level.vhd",
            library="ctu_can_fd_rtl"
        )

        #self.res_n = Signal()
        #self.data_in = Signal(32)
        #self.data_out = Signal(32)
        #self.adress = Signal(16)
        #self.scs = Signal()
        #self.srd = Signal()
        #self.swr = Signal()
        #self.sbe = Signal(4)
        self.int = Signal()
        self.can_tx = Signal()
        self.can_rx = Signal()

        self.comb += tx.eq(self.can_tx)
        self.comb += self.can_rx.eq(rx)

        self.bus = bus = wishbone.Interface(data_width=32, adr_width=16)

        self.res_n = CSRStorage(description="""Reset.\n
            Write ``0`` to reset.""")

        self.specials += Instance("can_top_level",
            i_clk_sys   = ClockSignal(),
            i_res_n     = self.res_n.storage,
            i_data_in   = self.bus.dat_w,
            o_data_out  = self.bus.dat_r,
            i_adress    = self.bus.adr,
            i_scs       = self.bus.sel,
            i_srd       = ~self.bus.we,
            i_swr       = self.bus.we,
            i_sbe       = self.bus.stb,
            i_int       = self.int,

            i_can_rx    = self.can_rx,
            o_can_tx    = self.can_tx,
        )
