# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Starting Test")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset sequence
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Testing Multiplexer Logic")

    # Testing various input combinations
    for a in range(256):  # 8-bit ui_in
        for b in range(256):  # 8-bit uio_in
            dut.ui_in.value = a
            dut.uio_in.value = b

            await ClockCycles(dut.clk, 2)  # Allow time for propagation

            expected_out = [
                (a & 0x01 if not (a & 0x80) else b & 0x01),
                (a & 0x02 if not (a & 0x80) else b & 0x02),
                (a & 0x04 if not (a & 0x80) else b & 0x04),
                (a & 0x08 if not (a & 0x80) else b & 0x08),
                ((a & 0x01 if not (a & 0x80) else b & 0x01) if not (b & 0x80) else b & 0x10),
                ((a & 0x02 if not (a & 0x80) else b & 0x02) if not (b & 0x80) else b & 0x20),
                ((a & 0x04 if not (a & 0x80) else b & 0x04) if not (b & 0x80) else b & 0x40),
                ((a & 0x08 if not (a & 0x80) else b & 0x08) if not (b & 0x80) else b & 0x80)
            ]

            expected_value = sum([bit << i for i, bit in enumerate(expected_out)])
            actual_value = int(dut.uo_out.value)

            assert actual_value == expected_value, (
                f"Mismatch: ui_in={a}, uio_in={b} -> Expected uo_out={expected_value}, Got {actual_value}")

            dut._log.info(f"Passed: ui_in={a}, uio_in={b}, uo_out={actual_value}")
