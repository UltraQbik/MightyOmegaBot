#include "headers/emulator.h"
//#include <chrono>
//#include <iostream>


const char* emulate_mq8b(uint16_t* insts) {
	// Memory
	uint8_t cache[256];
	uint8_t stack[256];

	// Registers
	uint8_t A = 0;
	uint8_t IP = 0;
	uint8_t SP = 0;
	bool CF = false;

	// cpu emulation
	uint16_t A_16;
	uint8_t negative;
	bool mem_flag = 0;
	uint8_t op_code = 0;
	uint8_t data = 0;

	// python things
	std::string cmd_out = "";
	uint64_t iteration = 0;

	// compute loop
	while (true) {
		// mem_flag | op_code | data
		// 1 bit    | 7 bits  | 8 bits			| 16 bits total

		mem_flag = insts[IP] >> 15;
		op_code  = (insts[IP] >> 8) & 0x7f;
		data = insts[IP] & 0xff;

		// in the real MQ8B this is a bus switcher
		// if memory flag is on, then we use 'data' as an address to the cache
		// SRA will not work the same way it does in the real MQ8B, due to double memory access
		if (mem_flag)
			data = cache[data];

		// instructions themselfes
		switch (op_code)
		{
		case 0:				// NOP
			break;
		case 1:				// LRA
			A = data;
			break;
		case 2:				// SRA
			cache[data] = A;
			break;
		case 3:				// CALL
			stack[SP] = IP;
			SP++;
			IP = data - 1;
			break;
		case 4:				// RET
			SP--;
			IP = stack[SP] - 1;
			A = data;
			break;
		case 5:				// JMP
			IP = data - 1;
			break;
		case 6:				// JMPP
			if ((A & 0x80) == 0)
				IP = data - 1;
			break;
		case 7:				// JMPZ
			if (A == 0)
				IP = data - 1;
			break;
		case 8:				// JMPN
			if ((A & 0x80) > 0)
				IP = data - 1;
			break;
		case 9:				// JMPC
			if (CF)
				IP = data - 1;
			break;
		case 10:			// CCF
			CF = false;
			break;

		case 16:			// AND
			A = A & data;
			break;
		case 17:			// OR
			A = A | data;
			break;
		case 18:			// XOR
			A = A ^ data;
			break;
		case 19:			// NOT
			A = ~A;
			break;
		case 20:			// LSC
			A = A << data;
			break;
		case 21:			// RSC
			A = A >> data;
			break;
		case 22:			// CMP
			negative = (A >> 7) << 1;

			if ((A & 0x7F) > data)
				A = 1 - negative;
			else if (A == data)
				A = 0;
			else
				A = negative - 1;
			break;

		case 32:			// ADC
			A_16 = (uint16_t)A + data;

			if ((A_16 & 0x100) > 0)
				CF = true;
			else
				CF = false;

			A = (uint8_t)A_16;
			break;
		case 33:			// SBC
			A_16 = (uint16_t)A - data;

			if ((A_16 & 0x100) > 0)
				CF = false;
			else
				CF = true;

			A = (uint8_t)A_16;
			break;
		case 34:			// INC
			A++;
			break;
		case 35:			// DEC
			A--;
			break;
		case 36:			// ABS
			if ((A & 0x80) > 0)
				A = (~A) + 1;
			break;

		case 48:			// UI (todo)
			break;
		case 49:			// UO
			cmd_out += std::to_string(A);
			cmd_out += "\n";
			break;
		case 50:			// UOC
			cmd_out += (char)A;
			break;
		case 51:			// UOCR
			cmd_out += (char)A;
			cmd_out += "\n";
			break;

		case 112:			// PRW (todo)
			break;
		case 113:			// PRR (todo)
			break;

		case 127:			// HALT
			goto ret;

		default:			// unrecognized
			goto ret;
		}

		// increment the instruction pointer (IP)
		IP++;

		// idiot checks
		if (cmd_out.length() >= 1048576)
			goto ret;

		iteration++;
		if (iteration >= 16777216)
			goto ret;
	}
	
ret:
	// return as const char*
	auto length = cmd_out.length() + 1;

	auto* out = new char[length];
	memcpy(out, cmd_out.data(), length);

	return out;
}


void delete_buffer(const char* _ch) {
	delete[] _ch;
}


//int main() {
//	uint16_t insts[] = {
//		0b0000010100000000
//	};
//
//	double avg = .0;
//
//	for (uint16_t i = 0; i < 1000; i++) {
//		auto start = std::chrono::high_resolution_clock::now();
//
//		auto ret = emulate_mq8b(insts);
//		// std::cout << ret << "\n";
//		delete_buffer(ret);
//
//		auto stop = std::chrono::high_resolution_clock::now();
//		auto duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start);
//
//		avg = (avg + duration.count()) / 2.;
//	}
//
//	std::cout << avg;
//}
