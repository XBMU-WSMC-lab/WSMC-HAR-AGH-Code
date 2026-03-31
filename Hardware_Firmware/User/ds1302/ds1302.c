#include "ds1302.h"

// ???????(??????????????)
uint8_t ds1302_time[8] = {0x19, 0x03, 0x1E, 0x0A, 0x23, 0x00, 0x02}; // 2025Äê2ÔÂ28ÈÕ   19:22:00 ???

// ?? DAT ?????
void ds1302_set_input_mode(void) {
    GPIO_InitTypeDef DS1302_Structure;
    RCC_APB2PeriphClockCmd(DS1302_DAT_RCC, ENABLE); // ?? DAT ????

    DS1302_Structure.GPIO_Pin = DS1302_DAT_PIN; // ?? DAT ??
    DS1302_Structure.GPIO_Mode = GPIO_Mode_IPU; // ?????????

    GPIO_Init(DS1302_DAT_PORT, &DS1302_Structure); // ??? DAT ??
}

// ?? DAT ?????
void ds1302_set_output_mode(void) {
    GPIO_InitTypeDef DS1302_Structure;
    RCC_APB2PeriphClockCmd(DS1302_DAT_RCC, ENABLE); // ?? DAT ????

    DS1302_Structure.GPIO_Pin = DS1302_DAT_PIN; // ?? DAT ??
    DS1302_Structure.GPIO_Mode = GPIO_Mode_Out_PP; // ?????????
    DS1302_Structure.GPIO_Speed = GPIO_Speed_50MHz; // ?? GPIO ??

    GPIO_Init(DS1302_DAT_PORT, &DS1302_Structure); // ??? DAT ??
}

// DS1302 ????
void ds1302_config(void) {
    GPIO_InitTypeDef DS1302_Structure;

    // ?????? GPIO ??
    RCC_APB2PeriphClockCmd(DS1302_CLK_RCC, ENABLE);
    RCC_APB2PeriphClockCmd(DS1302_DAT_RCC, ENABLE);
    RCC_APB2PeriphClockCmd(DS1302_RST_RCC, ENABLE);

    // ?? CLK ??
    DS1302_Structure.GPIO_Pin = DS1302_CLK_PIN;
    DS1302_Structure.GPIO_Mode = GPIO_Mode_Out_PP;
    DS1302_Structure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(DS1302_CLK_PORT, &DS1302_Structure);

    // ?? DAT ?????
    DS1302_Structure.GPIO_Pin = DS1302_DAT_PIN;
    DS1302_Structure.GPIO_Mode = GPIO_Mode_Out_PP;
    DS1302_Structure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(DS1302_DAT_PORT, &DS1302_Structure);

    // ?? RST ??
    DS1302_Structure.GPIO_Pin = DS1302_RST_PIN;
    DS1302_Structure.GPIO_Mode = GPIO_Mode_Out_PP;
    DS1302_Structure.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_Init(DS1302_RST_PORT, &DS1302_Structure);
}

// ??????
void ds1302_write_byte(uint8_t addr_or_data) {
    uint8_t i;
    ds1302_set_output_mode(); // ?? DAT ???
    for (i = 0; i < 8; i++) {
        if (addr_or_data & 0x01) {
            DS1302_DAT_HIGH; // ?????
        } else {
            DS1302_DAT_LOW; // ?????
        }
        addr_or_data >>= 1; // ??
        DS1302_CLK_HIGH; // CLK ??
        DS1302_CLK_LOW; // CLK ??
    }
}

// ???
void ds1302_write_cmd(uint8_t addr, uint8_t dat) {
    DS1302_RST_LOW; // ?? RST
    DS1302_CLK_LOW; // ?? CLK ??
    DS1302_RST_HIGH; // ?? RST
    ds1302_write_byte(addr); // ????
    ds1302_write_byte(dat); // ????
    DS1302_RST_LOW; // ?? RST
}

// ??????
uint8_t ds1302_read_byte(void) {
    uint8_t i;
    uint8_t dat = 0;
    ds1302_set_input_mode(); // ?? DAT ???
    for (i = 0; i < 8; i++) {
        dat >>= 1; // ??
        if (GPIO_ReadInputDataBit(DS1302_DAT_PORT, DS1302_DAT_PIN) == SET) {
            dat |= 0x80; // ??????,????
        }
        DS1302_CLK_HIGH; // CLK ??
        DS1302_CLK_LOW; // CLK ??
    }
    return dat;
}

// ????
uint8_t ds1302_read_data(uint8_t addr) {
    uint8_t dat = 0;
    DS1302_RST_LOW; // ?? RST
    DS1302_CLK_LOW; // ?? CLK ??
    DS1302_RST_HIGH; // ?? RST
    ds1302_write_byte(addr); // ????
    dat = ds1302_read_byte(); // ????
    DS1302_RST_LOW; // ?? RST
    return dat;
}

// BCD ????
void bcd_to_dec(uint8_t *bcd, uint8_t times) {
    uint8_t i;
    for (i = 0; i < times; i++) {
        bcd[i] = ((bcd[i] >> 4) * 10) + (bcd[i] & 0x0f);
    }
}

// ???? BCD
void dec_to_bcd(uint8_t *dec, uint8_t times) {
    uint8_t i;
    for (i = 0; i < times; i++) {
        dec[i] = ((dec[i] / 10) << 4) | (dec[i] % 10);
    }
}

// DS1302 ???
void ds1302_init(void) {
    ds1302_config(); // ?? GPIO

    dec_to_bcd(ds1302_time, 7); // ?????? BCD ?



//    ds1302_write_cmd(DS1302_WRITE_PROTECT, 0x00); // ?????

//    // ??????
//    ds1302_write_cmd(DS1302_WRITE_YEAR, ds1302_time[0]); // ????
//    ds1302_write_cmd(DS1302_WRITE_MONTH, ds1302_time[1]); // ????
//    ds1302_write_cmd(DS1302_WRITE_DAY, ds1302_time[2]);   // ????
//    ds1302_write_cmd(DS1302_WRITE_HOUR, ds1302_time[3]);  // ????
//    ds1302_write_cmd(DS1302_WRITE_MINUTE, ds1302_time[4]); // ????
//    ds1302_write_cmd(DS1302_WRITE_SECOND, ds1302_time[5]); // ????
//    ds1302_write_cmd(DS1302_WRITE_WEEK, ds1302_time[6]);   // ????

//    ds1302_write_cmd(DS1302_WRITE_PROTECT, 0x80); // ?????
}

// DS1302 ????
void ds1302_read(void) {
    ds1302_time[0] = ds1302_read_data(DS1302_READ_YEAR);  // ????
    ds1302_time[1] = ds1302_read_data(DS1302_READ_MONTH); // ????
    ds1302_time[2] = ds1302_read_data(DS1302_READ_DAY);   // ????
    ds1302_time[3] = ds1302_read_data(DS1302_READ_HOUR);  // ????
    ds1302_time[4] = ds1302_read_data(DS1302_READ_MINUTE);// ????
    ds1302_time[5] = ds1302_read_data(DS1302_READ_SECOND);// ????
    ds1302_time[6] = ds1302_read_data(DS1302_READ_WEEK);  // ????

    bcd_to_dec(ds1302_time, 7); // ? BCD ??????

}
