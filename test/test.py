max_val = 255  # Maximum sum value allowed
a_vals = [i for i in range(max_val + 1)]  # Fix range to include 255
b_vals = [j for j in range(max_val + 1)]  # Fix range to include 255

for i in range(len(a_vals)):
    for j in range(len(b_vals)):
        dut.ui_in.value = a_vals[i]
        dut.uio_in.value = b_vals[j]

        await ClockCycles(dut.clk, 20)  # Allow enough time for DUT processing

        dut._log.info(f"Test case ui_in={a_vals[i]}, uio_in={b_vals[j]} -> uo_out={dut.uo_out.value}")

        binary_A = format(a_vals[i], '08b')
        binary_B = format(b_vals[j], '08b')

        dut._log.info(f"Value: {a_vals[i]} -> Binary: {binary_A}")
        dut._log.info(f"Value: {b_vals[j]} -> Binary: {binary_B}")

        select_line_one = (a_vals[i] >> 7) & 1
        select_line_two = (a_vals[i] >> 6) & 1

        output_arr = []
        
        for k in range(4):
            if select_line_one == 0:
                output_arr.append((a_vals[i] >> k) & 1)
            else:
                output_arr.append((b_vals[j] >> k) & 1)

        for v in range(4, 8):
            if select_line_two == 0:
                output_arr.append((a_vals[i] >> v) & 1)
            else:
                output_arr.append((b_vals[j] >> v) & 1)

        assert len(output_arr) == 8, f"output_arr length mismatch: {output_arr}"

        expected_out = 0
        for bit_pos in range(8):  # Fix naming issue
            expected_out |= output_arr[bit_pos] << (7 - bit_pos)

        dut._log.info(f"Expected output in binary: {''.join(map(str, output_arr))} ({expected_out})")

        assert int(dut.uo_out.value) == expected_out, (
            f"Test failed for ui_in={a_vals[i]}, uio_in={b_vals[j]}. Expected {expected_out}, "
            f"but got {dut.uo_out.value}"
        )

        dut._log.info(f"Test passed for ui_in={a_vals[i]}, uio_in={b_vals[j]} with uo_out={dut.uo_out.value}")
