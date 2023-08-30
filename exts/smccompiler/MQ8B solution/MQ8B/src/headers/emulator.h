#pragma once
#include <string>


extern "C" {
	__declspec(dllexport) const char* emulate_mq8b(uint16_t* insts);
	__declspec(dllexport) void delete_buffer(const char* _ch);
}

