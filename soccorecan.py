#!/usr/bin/env python3

from migen import *

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.clock import S6PLL

from litedram.modules import _TechnologyTimings
from litedram.modules import _SpeedgradeTimings
from litedram.modules import SDRAMModule
from litedram.phy import GENSDRPHY
from litedram.frontend.bist import LiteDRAMBISTGenerator, LiteDRAMBISTChecker

from litex.build.generic_platform import *

import qm_xc6slx16_sdram

import canfd

# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.clock_domains.cd_sys    = ClockDomain()
        self.clock_domains.cd_sys_ps = ClockDomain()

        # # #

        clk50 = platform.request("clk50")
        platform.add_period_constraint(clk50, 1e9/50e6)

        self.submodules.pll = pll = S6PLL(speedgrade=-2)
        pll.register_clkin(clk50, 50e6)
        pll.create_clkout(self.cd_sys,    sys_clk_freq)
        pll.create_clkout(self.cd_sys_ps, sys_clk_freq, phase=270)

        self.specials += Instance("ODDR2",
            p_DDR_ALIGNMENT="NONE",
            p_INIT=0, p_SRTYPE="SYNC",
            i_D0=0, i_D1=1, i_S=0, i_R=0, i_CE=1,
            i_C0=self.cd_sys.clk, i_C1=~self.cd_sys.clk,
            o_Q=platform.request("sdram_clock"))

class SoCCoreCAN(SoCCore):
    mem_map = {
        "canfd": 0xb0000000,
    }
    mem_map.update(SoCMini.mem_map)

    def __init__(self, platform):
        sys_clk_freq = int(50e6)

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform, cpu_type = "vexriscv", cpu_variant = "minimal", clk_freq = sys_clk_freq, integrated_rom_size = 0x8000, with_sdram=True, sdram_module="MT48LC16M16")

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)

        # SDRAM ------------------------------------------------------------------------------------
        # phy
        #self.submodules.sdrphy = GENSDRPHY(platform.request("sdram"))
        # module
        #sdram_module = M12L64322A(sys_clk_freq, "1:1")
        # controller
        #self.register_sdram(self.sdrphy, sdram_module.geom_settings, sdram_module.timing_settings)

        # bist
        #self.submodules.sdram_generator = LiteDRAMBISTGenerator(self.sdram.crossbar.get_port())
        #self.submodules.sdram_checker   = LiteDRAMBISTChecker(self.sdram.crossbar.get_port())
        #self.add_csr("sdram_generator")
        #self.add_csr("sdram_checker")

        # Led --------------------------------------------------------------------------------------
        counter = Signal(32)
        self.sync += counter.eq(counter + 1)
        self.comb += platform.request("user_led").eq(counter[26])

        # CAN --------------------------------------------------------------------------------------

        platform.add_extension([("can_tx", 0, Pins("A4"), IOStandard("LVCMOS33"), Drive('24'), Misc('SLEW=QUIETIO'))])
        platform.add_extension([("can_rx", 0, Pins("B5"), IOStandard("LVCMOS33"), Drive('24'), Misc('SLEW=QUIETIO'))])

        tx = platform.request("can_tx")
        rx = platform.request("can_rx")

        can = canfd.CANFD(platform, tx, rx)
        self.submodules += can

        self.add_memory_region("canfd", self.mem_map["canfd"], 0x100000, type="io")

        self.add_wb_slave(self.mem_map["canfd"], can.bus)
        self.add_csr("canfd")


# Build --------------------------------------------------------------------------------------------

def main():
    soc     = SoCCoreCAN(qm_xc6slx16_sdram.Platform())
    builder = Builder(soc, output_dir="build")
    builder.build()

if __name__ == "__main__":
    main()
