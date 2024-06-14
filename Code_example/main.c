// File Name: main.c 
// Author:	 vorname nachname
// Kanidaten nummer: kannum
// Date:	xx.xx.20xx

//=========================================================
//Includes
//=========================================================

#include "mcc_generated_files/mcc.h" //Used for uC
#include "zyklus.h"		     //Used for timer

//=========================================================
//Defines
//=========================================================

//Define ports
#define LED PORTA
#define BUTTON PORTC

//Standard
#define TRUE 1
#define FALSE 0
#define ON 1
#define OFF 0

//Timer names
#define get_Zyklus_name() get_Zyklus()         //use_case_Zyklus0
#define get_Zyklus1_name() get_Zyklus1()		//use_case_Zyklus1
#define get_Zyklus2_name() get_Zyklus2()		//use_case_Zyklus2

#define reset_Zyklus_name()  reset_Zyklus()	 //use_case_Zyklus0
#define reset_Zyklus1_name() reset_Zyklus1()	//use_case_Zyklus1
#define reset_Zyklus2_name() reset_Zyklus2()	//use_case_Zyklus2

//Timers for blink
#define getBlink() get_Zyklus()               //Used for blink
#define getBlink1() get_Zyklus1()             //Used for blink 1
#define getBlink2() get_Zyklus2()             //Used for blink 2

#define resetBlink() reset_Zyklus()           //Used for blink
#define resetBlink1() reset_Zyklus1()         //Used for blink 1
#define resetBlink2() reset_Zyklus2() 		//Used for blink 2

//Switch case states 
#define device_states1 1
#define device_states2 2
#define device_states3 3
#define device_states4 4
#define device_states5 5
#define device_states6 6
#define device_states7 7
#define device_states8 8
#define device_states9 9

//Blinking names
#define name1_blink() blink(NewValueTon,NewValueToff) //in ms, Hz , :
#define name2_blink() blink1(NewValueTon,NewValueToff) //in ms, Hz , :
#define name3_blink() blink2(NewValueTon,NewValueToff) //in ms, Hz , :
		   

#define MASK7 0x80
#define MASK6 0x40
#define MASK5 0x20
#define MASK4 0x10
#define MASK3 0x08
#define MASK2 0x04
#define MASK1 0x02
#define MASK0 0x01

//Project specific

//=========================================================
//Global Variables
//=========================================================

//Standard
uint8_t copyOutput = 0;
uint8_t copyInput = 0;

//Input Variables (PosEdge)
uint8_t button_7_PosEdge = 0;	//S7
uint8_t button_6_PosEdge = 0;	//S6
uint8_t button_5_PosEdge = 0;	//S5
uint8_t button_4_PosEdge = 0;	//S4
uint8_t button_3_PosEdge = 0;	//S3
uint8_t button_2_PosEdge = 0;	//S2
uint8_t button_1_PosEdge = 0;	//S1
uint8_t button_0_PosEdge = 0;	//S0

//Input Variables (NegEdge)
uint8_t button_7_NegEdge = 0;	//S7
uint8_t button_6_NegEdge = 0;	//S6
uint8_t button_5_NegEdge = 0;	//S5
uint8_t button_4_NegEdge = 0;	//S4
uint8_t button_3_NegEdge = 0;	//S3
uint8_t button_2_NegEdge = 0;	//S2
uint8_t button_1_NegEdge = 0;	//S1
uint8_t button_0_NegEdge = 0;	//S0

//Input Variables (Button State)
uint8_t switch_7 = 0;	//S7
uint8_t switch_6 = 0;	//S6
uint8_t switch_5 = 0;	//S5
uint8_t switch_4 = 0;	//S4
uint8_t switch_3 = 0;	//S3
uint8_t switch_2 = 0;	//S2
uint8_t switch_1 = 0;	//S1
uint8_t switch_0 = 0;	//S0

//Output Variables
uint8_t led_7_init = statled7;	//LED7
uint8_t led_6_init = statled6;	//LED6
uint8_t led_5_init = statled5;	//LED5
uint8_t led_4_init = statled4;	//LED4
uint8_t led_3_init = statled3;	//LED3
uint8_t led_2_init = statled2;	//LED2
uint8_t led_1_init = statled1;	//LED1
uint8_t led_0_init = statled0;	//LED0

//Device State
uint8_t deviceState = start_state;

//Project specific

//=========================================================
//Prototypes
//=========================================================

//Standard
void initializing();
void readInput();
void process();
void writeOutput();

uint8_t blink(unsigned int tOn, unsigned int tOff);
uint8_t blink1(unsigned int tOn, unsigned int tOff);
uint8_t blink2(unsigned int tOn, unsigned int tOff);

//=========================================================
//Name: initializing
//Function: Initialise the MicroController and System.
//Return Value: None
//=========================================================

void initializing()
{
    SYSTEM_Initialize(); //Initialise uC
    ZYKLUS_Initialize(); //Initialise Timer

    //Call function reset_Zyklus & get_Zyklus to avoid warnings if they aren't used.
    //These functions are used for timing and work as 3 different, individual timers.
    get_Zyklus();
    get_Zyklus1();
    get_Zyklus2();
    reset_Zyklus();
    reset_Zyklus1();
    reset_Zyklus2();
    
    //Project specific
}

//=========================================================
//Name: main
//Function: main function
//Return Value: None
//=========================================================

void main()
{
    initializing();
    while (1)
    {
	readInput();
	process();
	writeOutput();
    }
}

//=========================================================
//Name: readInput
//Function:Read Input from Switches (P2)
//Return Value: None
//=========================================================

void readInput()
{
    static uint8_t oldInput = 0; //"static" to make sure variable only gets defined and initialised  once
    uint8_t posEdge = 0;
    uint8_t negEdge = 0;

    copyInput = BUTTON; //Create Copy of Buttons/Switches
    
    //Button Positive Edge Detections
    posEdge = (~oldInput) & copyInput;
    button_7_PosEdge = (posEdge & MASK7) >> 7;	//button S7 PosEdge
    button_6_PosEdge = (posEdge & MASK6) >> 6;	//button S6 PosEdge
    button_5_PosEdge = (posEdge & MASK5) >> 5;	//button S5 PosEdge
    button_4_PosEdge = (posEdge & MASK4) >> 4;	//button S4 PosEdge
    button_3_PosEdge = (posEdge & MASK3) >> 3;	//button S3 PosEdge
    button_2_PosEdge = (posEdge & MASK2) >> 2;	//button S2 PosEdge
    button_1_PosEdge = (posEdge & MASK1) >> 1;	//button S1 PosEdge
    button_0_PosEdge = posEdge & MASK0;		//button S0 PosEdge
    
    //Button Negative Edge Detections
    negEdge = oldInput & (~copyInput);
    button_7_NegEdge = (negEdge & MASK7) >> 7;	//button S7 NegEdge
    button_6_NegEdge = (negEdge & MASK6) >> 6;	//button S6 NegEdge
    button_5_NegEdge = (negEdge & MASK5) >> 5;	//button S5 NegEdge
    button_4_NegEdge = (negEdge & MASK4) >> 4;	//button S4 NegEdge
    button_3_NegEdge = (negEdge & MASK3) >> 3;	//button S3 NegEdge
    button_2_NegEdge = (negEdge & MASK2) >> 2;	//button S2 NegEdge
    button_1_NegEdge = (negEdge & MASK1) >> 1;	//button S1 NegEdge
    button_0_NegEdge = negEdge & MASK0;		//button S0 NegEdge

    oldInput = copyInput;
    
    //Button State
    switch_7 = (copyInput & MASK7) >> 7;   //button S7
    switch_6 = (copyInput & MASK6) >> 6;   //button S6
    switch_5 = (copyInput & MASK5) >> 5;   //button S5
    switch_4 = (copyInput & MASK4) >> 4;   //button S4
    switch_3 = (copyInput & MASK3) >> 3;   //button S3
    switch_2 = (copyInput & MASK2) >> 2;   //button S2
    switch_1 = (copyInput & MASK1) >> 1;   //button S1
    switch_0 = copyInput & MASK0;	   //button S0

}

//=========================================================
//Name: process
//Function: Process the main Code
//Return Value: None
//=========================================================

void process()
{

    //turn all Outputs to OFF to later turn them ON in the individual cases
    led_7_init = statled7;
    led_6_init = statled6;
    led_5_init = statled5;
    led_4_init = statled4;
    led_3_init = statled3;
    led_2_init = statled2;
    led_1_init = statled1;
    led_0_init = statled0;
    
    switch (deviceState)
    {
	case device_states1: //state explanation
	    
	break;

	case device_states2: //state explanation
	    
	break;

	case device_states3: //state explanation
	    
	break;

	case device_states4: //state explanation
	    
	break;

	case device_states5: //state explanation
	    
	break;

	case device_states6: //state explanation
	    
	break;

	case device_states7: //state explanation
	    
	break;

	case device_states8: //state explanation
	    
	break;

	case device_states9: //state explanation
	    
	break;

	default:
	    //only for debug
	break;
    }

}

//=========================================================
//Name: writeOutput
//Function: Write Output to LED (P1)
//Return Value: None
//=========================================================

void writeOutput()
{
    //Project specific

    //Standard
    copyOutput = led_7<<7;	//LED 7
    copyOutput = copyOutput | (led_6<<6);	//LED 6
    copyOutput = copyOutput | (led_5<<5);	//LED 5
    copyOutput = copyOutput | (led_4<<4);	//LED 4
    copyOutput = copyOutput | (led_3<<3);	//LED 3
    copyOutput = copyOutput | (led_2<<2);	//LED 2
    copyOutput = copyOutput | (led_1<<1);	//LED 1
    copyOutput = copyOutput | led_0;	//LED 0

    LED = copyOutput; //Write Copy to the LEDs
}

//=========================================================
//Name: functions
//Function: process the functions
//Return Value: depending on the function
//=========================================================

uint8_t blink(unsigned int tOn, unsigned int tOff)
{
    uint8_t statusBlink = 0;

    if (getBlink <= tOn)
    {
	statusBlink = ON;
    }
    else
    {
	statusBlink = OFF;
    }

    if (getBlink >= tOn + tOff)
    {
	resetBlink;
    }
    return statusBlink;
}

uint8_t blink1(unsigned int tOn, unsigned int tOff)
{
    uint8_t statusBlink = 0;

    if (getBlink1 <= tOn)
    {
	statusBlink = ON;
    }
    else
    {
	statusBlink = OFF;
    }

    if (getBlink1 >= tOn + tOff)
    {
	resetBlink1;
    }
    return statusBlink;
}

uint8_t blink2(unsigned int tOn, unsigned int tOff)
{
    uint8_t statusBlink = 0;

    if (getBlink2() <= tOn)
    {
	statusBlink = ON;
    }
    else
    {
	statusBlink = OFF;
    }

    if (getBlink2() >= tOn + tOff)
    {
	resetBlink2;
    }
    return statusBlink;
}