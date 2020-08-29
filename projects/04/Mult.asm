// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.


// let's assume R0 is less than R1

@0
D=A
@i
M=D 	// set i = 0

@res
M=0

@respositive     // respositive & 1 == 0 -> res positive
M=0

// if any of the number is 0 goto end

@R0
D=M
@ZERO
D;JEQ

@R1
D=M
@ZERO
D;JEQ

// make the numbers positive
@R0
D=M
@POSITIVE_R0
D;JLE

(AFTER_R0)

@R1
D=M
@POSITIVE_R1
D;JLE


(LOOP)
	@i
	D=M
	@R0
	D=D-M
	@BEFORE_END
	D;JEQ

	@R1
	D=M
	@res
	M=M+D

	@i
	M=M+1

	@res
	D=M
	@R2
	M=D


	@LOOP
	0;JMP

(POSITIVE_R0)
	@0
	D=A
	@R0
	M=D-M
	@respositive
	M=1
	@AFTER_R0
	0;JMP
	
(POSITIVE_R1)
	@0
	D=A
	@R1
	M=D-M
	@respositive
	M=M+1
	@LOOP
	0;JMP

(ZERO)
	@R2
	M=0
	@END
	0;JMP

(BEFORE_END)
	@1
	D=A
	@respositive
	D=M&D
	@MAKE_NEG
	D;JNE
	@END
	0;JMP

(MAKE_NEG)
	@0
	D=A
	@R2
	M=D-M
	@END
	0;JMP

(END)
	@END
	0;JMP
