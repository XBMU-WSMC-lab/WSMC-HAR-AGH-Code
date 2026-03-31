#ifndef __SYSTICK_H
#define __SYSTICK_H

#include "stm32f10x.h"

void SysTick_Init(void);
void delay_us(u16 us);
void delay_ms(u16 ms);

#endif /* __SYSTICK_H */
