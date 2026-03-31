/**
  ******************************************************************************
  * @file    main.c
  * @author  LYC
  * @version V1.0
  * @date    2014-04-22
  * @brief   MPU6050 软件IIC测试
  ******************************************************************************
  * @attention
  * 实验平台:野火 霸道 STM32 开发板 
  ******************************************************************************
  */
  
#include "stm32f10x.h"
#include "stm32f10x_it.h"
#include "./systick/bsp_SysTick.h"
#include "./led/bsp_led.h"
#include "./usart/bsp_usart.h"
#include "./mpu6050/mpu6050.h"
#include "./i2c/bsp_i2c.h"
#include "ds1302.h"
#include "MAX30102.h"

/* MAX30102数据 */
extern int32_t n_heart_rate, n_sp02;
uint32_t heart_rate_raw, sp02_raw, heart_rate_filt, sp02_filt;
/* MPU6050数据 */
short Accel[3];
short Gyro[3];
float Temp;


/**
  * @brief  主函数
  * @param  无  
  * @retval 无
  */
int main(void)
{
	/* LED 端口初始化 */
	LED_GPIO_Config();
	/* 串口1通信初始化 */
	USART_Config();
	
	//心率血氧模块初始化
	MAX30102_Init();

  //ds1302初始化
  ds1302_init();	 

	//I2C初始化
	i2c_GPIO_Config();
  //MPU6050初始化
	MPU6050_Init();
  //检测MPU6050
	if(MPU6050ReadID() == 0)
  {
    printf("\r\n没有检测到MPU6050传感器！\r\n");
    LED_RED; 
		while(1);	
	}
  
  /* 配置SysTick定时器和中断 */
  SysTick_Init(); //配置 SysTick 为 1ms 中断一次，在中断里读取传感器数据
  SysTick->CTRL |= SysTick_CTRL_ENABLE_Msk; //启动定时器
  
  while(1)
  {
    if(task_readdata_finish) //task_readdata_finish = 1 表示读取MPU6050数据完成
    {
//			HeartRate_SpO2_Read();	//获取心率和血氧数据(处理后的)
			while(max30102_INTPin==1);   //等待MAX30102中断引脚拉低
			maxim_max30102_read_fifo(&heart_rate_raw, &sp02_raw);  //read from MAX30102 FIFO
			heart_rate_filt = low_pass_filter(heart_rate_raw);
			sp02_filt = low_pass_filter(sp02_raw);
      ds1302_read();
      printf("1     ");
      
      printf("20%d-%d-%d %d-%d-%d   ",ds1302_time[0],ds1302_time[1],ds1302_time[2],ds1302_time[3],ds1302_time[4],ds1302_time[5]);
			printf("%4d %4d %4d  ",Accel[0],Accel[1],Accel[2]);
      printf("%4d %4d %4d  ",Gyro[0],Gyro[1],Gyro[2]);
//			printf("心率：%d 次/min  血氧：%d %%\r\n",n_heart_rate,n_sp02);	//打印心率和血氧数据(处理后的)
      printf("%d   %d \r\n",heart_rate_filt,sp02_filt);	//打印心率和血氧数据(滤波后原始数据)
			
      task_readdata_finish = 0; // 清零标志位
    }

	}
	
}

/*********************************************END OF FILE**********************/
