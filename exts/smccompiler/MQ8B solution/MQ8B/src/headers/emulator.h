#pragma once
#include <string>


#if defined(_WIN32)
#  define DLL_EXPORT __declspec(dllexport)
#else
#  define DLL_EXPORT
#endif


extern "C" {
	DLL_EXPORT const char* emulate_mq8b(uint16_t* insts);
	DLL_EXPORT void delete_buffer(const char* _ch);
}

