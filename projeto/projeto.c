#include <stdio.h>        
#include "pico/stdlib.h"  
#include "hardware/adc.h" 

#define VRX_PIN 26
#define VRY_PIN 27

int main()
{
    stdio_init_all();

    adc_init();
    adc_gpio_init(VRX_PIN);
    adc_gpio_init(VRY_PIN);


    while (true)
    {
        adc_select_input(0);
        uint16_t vrx_value = adc_read();

        adc_select_input(1);
        uint16_t vry_value = adc_read();

        printf("%u, %u\n", vrx_value, vry_value);

        sleep_ms(250);
    }

    return 0;
}
