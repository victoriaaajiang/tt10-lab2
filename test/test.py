# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    # Test all combinations of ui_in and uio_in across 256 possible values
    max_val = 256  # Maximum value for 8-bit input
    for a in range(max_val):
        for b in range(max_val):
            # Set the input values
            dut.ui_in.value = a
            dut.uio_in.value = b

            # Wait for one clock cycle to allow the output to stabilize
            await ClockCycles(dut.clk, 1)

            # Compute the expected output based on your module's logic
            # Your module uses multiplexers to select between bits of ui_in and uio_in
            # based on the value of ui_in[7] and uio_in[7].
            # For simplicity, let's assume the logic is such that:
            # uo_out[3:0] = ui_in[3:0] if ui_in[7] is 1, else uio_in[3:0]
            # uo_out[7:4] = uo_out[3:0] if uio_in[7] is 1, else uio_in[7:4]

            # Calculate the expected output
            if (a >> 7) & 1:  # Check if ui_in[7] is 1
                lower_bits = a & 0x0F  # ui_in[3:0]
            else:
                lower_bits = b & 0x0F  # uio_in[3:0]

            if (b >> 7) & 1:  # Check if uio_in[7] is 1
                upper_bits = lower_bits
            else:
                upper_bits = (b >> 4) & 0x0F  # uio_in[7:4]

            expected_output = (upper_bits << 4) | lower_bits

            # Compare the expected output with the actual output
            assert dut.uo_out.value == expected_output, f"Test failed for ui_in={a}, uio_in={b}. Expected: {expected_output}, Got: {dut.uo_out.value}"

    dut._log.info("All tests passed")
