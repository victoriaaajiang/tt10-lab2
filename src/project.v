/*
 * Copyright (c) 2024 Your Name
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_example (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  // assign uo_out  = ui_in + uio_in;  // Example: ou_out is the sum of ui_in and uio_in
  assign uio_out = 0;
  assign uio_oe  = 0;

  xor bit1 (ui_in[0], uio_in[0], 1'b0, uo_out[0], uio_out[0]);
  xor bit2 (ui_in[0], uio_in[0], 1'b0, uo_out[0], uio_out[0]);
  xor bit3 (ui_in[0], uio_in[0], 1'b0, uo_out[0], uio_out[0]);
  xor bit4 (ui_in[0], uio_in[0], 1'b0, uo_out[0], uio_out[0]);
  xor bit5 (ui_in[0], uio_in[0], 1'b0, uo_out[0], uio_out[0]);
  xor bit6 (ui_in[0], uio_in[0], 1'b0, uo_out[0], uio_out[0]);
  xor bit7 (ui_in[0], uio_in[0], 1'b0, uo_out[0], uio_out[0]);
  xor bit8 (ui_in[0], uio_in[0], 1'b0, uo_out[0], uio_out[0]);



  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0, uio_oe};

endmodule

module xor(input ded_input, 
            input io_input, 
            input carry_in,
            output ded_output,
            output carry_out);
  assign ded_output = (~ded_input & io_input) | (ded_input & ~io_input);
  assign carry_out = ded_input & io_input | ded_input & carry_in | io_input & carry_in;
  
endmodule
