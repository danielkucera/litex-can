#!/usr/bin/env python3

from migen import *

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.cores.clock import S6PLL

from litex.build.generic_platform import *

import platform

import canfd

# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.clock_domains.cd_sys    = ClockDomain()
        self.clock_domains.cd_sys_ps = ClockDomain()

        # # #

        clk25 = platform.request("clk25")
        platform.add_period_constraint(clk25, 1e9/25e6)

        self.submodules.pll = pll = S6PLL(speedgrade=-2)
        pll.register_clkin(clk25, 25e6)
        pll.create_clkout(self.cd_sys, sys_clk_freq)

# CANSoC -------------------------------------------------------------------------------------

class CANSoC(SoCMini):
    mem_map = {
        "canfd": 0xb0000000,
    }
    mem_map.update(SoCMini.mem_map)

    def __init__(self, platform):
        sys_clk_freq = int(27e6)
        SoCMini.__init__(self, platform, sys_clk_freq)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq)

        platform.add_extension([("can_tx", 0, Pins("A4"), IOStandard("LVCMOS33"), Misc("DRIVE=4"))])
        platform.add_extension([("can_rx", 0, Pins("B5"), IOStandard("LVCMOS33"), Misc("DRIVE=4"))])

        can = canfd.CANFD(platform, platform.request("can_tx"), platform.request("can_rx"))
        self.submodules += can

        self.add_memory_region("canfd", self.mem_map["canfd"], 0x100000, type="io")

        self.add_wb_slave(self.mem_map["canfd"], can.bus)
        self.add_csr("canfd")

# Build --------------------------------------------------------------------------------------------

def main():
    plat = platform.Platform()
    soc = CANSoC(plat)
    builder = Builder(soc, output_dir="build")
    vns = builder.build()

if __name__ == "__main__":
    main()

