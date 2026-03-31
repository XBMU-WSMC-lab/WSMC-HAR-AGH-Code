#ifndef __DS1302_H
#define __DS1302_H
#include "stm32f10x.h"

#define DS1302_CLK_RCC		RCC_APB2Periph_GPIOB		//??
#define DS1302_CLK_PORT		GPIOB						//??
#define DS1302_CLK_PIN		GPIO_Pin_13					//??

#define DS1302_DAT_RCC		RCC_APB2Periph_GPIOB		//??
#define DS1302_DAT_PORT		GPIOB						//??
#define DS1302_DAT_PIN		GPIO_Pin_14					//??

#define DS1302_RST_RCC		RCC_APB2Periph_GPIOB		//??
#define DS1302_RST_PORT		GPIOB						//??
#define DS1302_RST_PIN		GPIO_Pin_15					//??


#define DS1302_CLK_HIGH		GPIO_SetBits(DS1302_CLK_PORT, DS1302_CLK_PIN)			//???????
#define DS1302_CLK_LOW		GPIO_ResetBits(DS1302_CLK_PORT, DS1302_CLK_PIN)			//???????

#define DS1302_DAT_HIGH		GPIO_SetBits(DS1302_DAT_PORT, DS1302_DAT_PIN)			//???????
#define DS1302_DAT_LOW		GPIO_ResetBits(DS1302_DAT_PORT, DS1302_DAT_PIN)			//???????

#define DS1302_RST_HIGH		GPIO_SetBits(DS1302_RST_PORT, DS1302_RST_PIN)			//???????
#define DS1302_RST_LOW		GPIO_ResetBits(DS1302_RST_PORT, DS1302_RST_PIN)			//???????

#define DS1302_SET_IN		ds1302_set_input_mode()							//??????
#define DS1302_SET_OUT 		ds1302_set_output_mode()						//??????		


/*????????*/
#define DS1302_READ_SECOND 	0X81   	//?
#define DS1302_READ_MINUTE 	0X83	//?
#define DS1302_READ_HOUR   	0X85	//?
#define DS1302_READ_DAY		0X87	//?
#define DS1302_READ_MONTH 	0X89	//?
#define DS1302_READ_WEEK 	0X8B	//?
#define DS1302_READ_YEAR 	0X8D	//?
//#define DS1302_READ_TIME 	0XBF	//??????

/*????????*/
#define DS1302_WRITE_SECOND 0X80   	//?
#define DS1302_WRITE_MINUTE 0X82	//?
#define DS1302_WRITE_HOUR   0X84	//?
#define DS1302_WRITE_DAY	0X86	//?
#define DS1302_WRITE_MONTH 	0X88	//?
#define DS1302_WRITE_WEEK 	0X8A	//?
#define DS1302_WRITE_YEAR 	0X8C	//?
#define DS1302_WRITE_PROTECT 0X8E	//??
//#define DS1302_WRITE_TIME 	0XBE 	//?????


extern uint8_t ds1302_time[8];	//???????

void ds1302_write_byte(uint8_t addr_or_data);			//DS1302 ???? ??
void ds1302_write_cmd(uint8_t addr,uint8_t dat);		//DS1302 ???	  ??
uint8_t ds1302_read_byte(void);							//DS1302 ???? ??
uint8_t ds1302_read_data(uint8_t addr);					//DS1302 ???? ??
void bcd_to_dec(uint8_t *bcd,uint8_t times);			//BCD ? ??? ??
void dec_to_bcd(uint8_t *dec,uint8_t times);			//??? ? BCD ??
void ds1302_init(void);									//DS1302 ???????? ??
void ds1302_read(void);									//DS1302 ??  ????? ??

#endif

