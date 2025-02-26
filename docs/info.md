<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

Using two 2-1 multiplexers, I generate an 8-bit output from two 8-bit input binary numbers, A and B. The first 4 bits of the output is assigned as the first 4 bits of Input A if the eighth bit of A is 0, and if A is 1 then it is assigned as the first 4 bits of Input B. Then, the last 4 bits of the output is assigned as the first 4 bits of the output if the eighth bit of B is 0, and assigned as the last 4 bits of Input B if the eighth bit of B is 1.

Here is a diagram showing the multiplexers:
![IMG_0403](https://github.com/user-attachments/assets/f51f4d3e-33c2-46db-83b2-5166d3058a23)

## How to test

List out two numbers in 8-bit binary format, assigned as A and B. Then, according to the function, estimate the expected result and insert the inputs and expected output in the test.py file in decimal format. Check the "Actions" tab to check the results.

## External hardware

N/A
