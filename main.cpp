#include <stdio.h>
#include <termios.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <iostream>
#include <thread>
#include <mutex>
#include <condition_variable>
#include <chrono>
#include <random>
#include <deque>
#include <iomanip>
#include <signal.h>
#include <JetsonGPIO.h>

#include "opencv2/opencv.hpp"
#include "opencv2/highgui.hpp"
#include "TeliCamApi.h"
#include "TeliCamUtl.h"

using namespace Teli;

std::mutex mtx;
std::condition_variable sv;
bool thread2_started = false;
std::chrono::milliseconds shared_sleep_time(0);
int last_random_value = 0;
std::deque<int> last_ten_random_values;

bool8_t SetExposureTime();
bool8_t SetFrameRate();
uint32_t Initialize();
uint32_t SetTriggerMode();
uint32_t OpenStream();
uint32_t CloseStream();
uint32_t StartAcquisition();
uint32_t StopAcquisition();
uint32_t ImageHandling();
void thread2();
void Terminate();

CAM_EXPOSURE_TIME_CONTROL_TYPE peExpControl = CAM_EXPOSURE_TIME_CONTROL_MANUAL;
static CAM_API_STATUS uiStatus = CAM_API_STS_SUCCESS;
static uint8_t *s_pucImgBuf = NULL;
static uint8_t *pucImgBGR;
static uint32_t s_uiImgBufSize = 0;
static CAM_HANDLE s_hCam = (CAM_HANDLE)NULL;
static CAM_STRM_HANDLE s_hStrm = (CAM_STRM_HANDLE)NULL;
static SIGNAL_HANDLE s_hStrmEvt = NULL;
static CAM_PIXEL_FORMAT s_pixelFormat;
static uint32_t count = 0;
const uint32_t gCamWidth = 2448;
const uint32_t gCamHeight = 2048;

static cv::Mat s_openCvImage;
static char s_szWindowTitle[] = "OpenCV Test";
static double      s_dMultDspExp = 0.001;  

// Pin Definitions
int led_pin1 = 7;
int led_pin2 = 11;
// Flag to determine when user wants to end program
bool done = false;
 
// Function called by Interrupt
void signalHandler (int s){
  done = true;
}

int main(){

    uint32_t uiStatus = 0; 
    signal(SIGINT, signalHandler);

    GPIO::setmode(GPIO::BOARD);
    GPIO::setup(led_pin1, GPIO::OUT, GPIO::LOW);
    GPIO::setup(led_pin2, GPIO::OUT, GPIO::LOW);

    uiStatus = Initialize();
    printf("done: Initialize()\n\n");

    // Set software one-shot trigger mode.
    uiStatus = SetTriggerMode();
    if (uiStatus != 0) {
        printf("Failed to set trigger mode, Status = 0x%08X.\n", uiStatus);
        return 1;
    }

    // Open stream.
    uiStatus = OpenStream();
    if (uiStatus != 0) {
        printf("Failed to open stream, Status = 0x%08X.\n", uiStatus);
        return 1;
    }

    // Start acquisition
    uiStatus = StartAcquisition();
    if (uiStatus != 0) {
        printf("Failed to start acquisition, Status = 0x%08X.\n", uiStatus);
        return 1;
    }
    printf("done: StartAcquisition\n");

    std::thread t1(ImageHandling);
    std::thread t2(thread2);

    t1.join();
    t2.join();

    // Stop acquisition.
    uiStatus = StopAcquisition();
    
    GPIO::cleanup();
    // Close stream.
    CloseStream();

    // Terminate.
    Terminate();

    return 0;
}

// ImageHandling 함수에서 필요한 부분만 thread1에서 수행
uint32_t ImageHandling() {
    
    uint32_t uiSize = s_uiImgBufSize;
    CAM_IMAGE_INFO imageInfo;


    while (true) {
        {
            std::lock_guard<std::mutex> lk(mtx);
        }
        GPIO::output(led_pin1, 1);
        printf("스레드 1 시작\n"); 
        thread2_started = true;
        sv.notify_one();
        //auto start = std::chrono::high_resolution_clock::now();

        uiStatus = ExecuteCamSoftwareTrigger(s_hCam);
        // Wait for receiving image completion event.
        uiStatus = Sys_WaitForSignal(s_hStrmEvt, 2000);
        

        // Copy received image data to local buffer, and get size of received image.
        uiStatus = Strm_ReadCurrentImage(s_hStrm, s_pucImgBuf, &uiSize, &imageInfo);
   
        uiStatus = ConvImage(DST_FMT_BGR24, imageInfo.uiPixelFormat, true,
                              (void *)pucImgBGR, s_pucImgBuf, imageInfo.uiSizeX, imageInfo.uiSizeY);
        
        /*
        char* filenameData = static_cast<char*>(malloc(imageInfo.uiSizeX * imageInfo.uiSizeY * 3));
        if (!filenameData) {
            printf("Cannot allocate memory for filename\n");
            
            break;
        }
         
         // Save as bitmap with adjusted color
        uiStatus = SaveBmpRGB(image, sImageInfo.uiSizeX, sImageInfo.uiSizeY, filename.c_str());
        if (uiStatus) {
            printf("SaveBmpRGB error: 0x%08x\n", uiStatus);
            break;
        }
        */
        for(int j=0; j < 10000; j++){
            for(int y=0; y < 10000; y++){
                int jy = 0;
                jy++;
            }
        }
        /*
        auto end = std::chrono::high_resolution_clock::now();
        auto duration_6 = std::chrono::duration_cast<std::chrono::milliseconds>(end - start);
        double fps = 1000 / duration_6.count();
        */
        GPIO::output(led_pin1, 0);
        //printf("스레드 1 전체시간 : %.1lf FPS : %.1lf\n", static_cast<double>(duration_6.count()), fps);

        shared_sleep_time = std::chrono::milliseconds(3000) - duration_6;  // 15초를 ms로 변환
        //printf("공유시간 :  %.1ld\n", shared_sleep_time.count());

        if (shared_sleep_time.count() > 0) {
            std::this_thread::sleep_for(shared_sleep_time);
        }
        else if (shared_sleep_time.count() < 0) {
            printf("인터벌 시간 초과 프로그램 종료\n");
            break; // 인터벌 시간을 초과했으므로 프로그램 종료
        }
        else {
            printf("경고: 실행 시간이 설정된 인터벌을 초과했습니다!\n");
        }     
         // 스레드 2에게 대기 시간을 알림
        sv.notify_one();
    }
}

// 스레드2 함수
void thread2() {
    while (true) {  // 무한 루프
        std::unique_lock<std::mutex> lk(mtx);
        sv.wait(lk, [] { return thread2_started; });  // 스레드 1이 시작될 때까지 대기
        //auto start1 = std::chrono::high_resolution_clock::now();
        GPIO::output(led_pin2, GPIO::HIGH);
        printf("스레드 2 시작 \n");

        for(int j=0; j < 1000; j++){
            for(int y=0; y < 10000; y++){
                int jy = 0;
                jy++;
            }
        }
        /*
        auto end1 = std::chrono::high_resolution_clock::now();
        auto duration_5 = std::chrono::duration_cast<std::chrono::milliseconds>(end1 - start1);
        double fps = 1000 / duration_5.count();
        printf("스레드 2 전체시간 : %.1lf FPS : %.1lf\n", static_cast<double>(duration_5.count()), fps);
        */
        thread2_started = false; // 다시 대기할 준비
        GPIO::output(led_pin2, GPIO::LOW);
        printf("스레드 2 종료\n");

    }
}

uint32_t Initialize()
{
    uint32_t uiNum;

    // API initialization.
    uiStatus = Sys_Initialize();
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 1;

    // Get uiNumber of camera.
    uiStatus = Sys_GetNumOfCameras(&uiNum);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 1;

    if (uiNum == 0)
    {
        printf(" No cameras found.\n");
        return 1;
    }
    printf(" %d camera(s) found.\n", uiNum);

    // Get camera information.
    CAM_INFO        sCamInfo;
    U3V_CAM_INFO    *psU3vCamInfo;
    GEV_CAM_INFO    *psGevCamInfo;

    for (int i = 0; i < (int)uiNum; i++)
    {
        memset((void*)&sCamInfo, 0, sizeof(CAM_INFO));
        // Get information of a camera.
        uiStatus = Cam_GetInformation((CAM_HANDLE)NULL, i, &sCamInfo);
        if (uiStatus != CAM_API_STS_SUCCESS)
        {
            return 1;
        }

        printf("\n<Camera%d information>\n", i);
        if (sCamInfo.eCamType == CAM_TYPE_U3V)
            printf(" Type                               : USB3 Vision camera\n");
        else if (sCamInfo.eCamType == CAM_TYPE_GEV)
            printf(" Type                               : GigE Vision camera\n");

        printf(" Manufacturer                       : %s\n", sCamInfo.szManufacturer);
        printf(" Model name                         : %s\n", sCamInfo.szModelName);
        printf(" Serial number                      : %s\n", sCamInfo.szSerialNumber);
        printf(" User defined name                  : %s\n", sCamInfo.szUserDefinedName);

        if (sCamInfo.eCamType == CAM_TYPE_U3V) {
            psU3vCamInfo = &sCamInfo.sU3vCamInfo;

            printf(" U3v family name                    : %s\n", psU3vCamInfo->szFamilyName);
            printf(" U3v device version                 : %s\n", psU3vCamInfo->szDeviceVersion);
            printf(" U3v manufacturer information       : %s\n", psU3vCamInfo->szManufacturerInfo);
            printf(" U3v adapter vendor ID              : 0x%04X\n", psU3vCamInfo->uiAdapterVendorId);
            printf(" U3v adapter device ID              : 0x%04X\n", psU3vCamInfo->uiAdapterDeviceId);
            printf(" U3v Adapter default MaxPacketSize  : %d\n", psU3vCamInfo->uiAdapterDfltMaxPacketSize);
        } else if (sCamInfo.eCamType == CAM_TYPE_GEV) {
            psGevCamInfo = &sCamInfo.sGevCamInfo;

            printf(" Gev display name                   : %s\n", psGevCamInfo->szDisplayName);
            printf(" Gev MAC address                    : %02X-%02X-%02X-%02X-%02X-%02X\n",
                psGevCamInfo->aucMACAddress[0],
                psGevCamInfo->aucMACAddress[1],
                psGevCamInfo->aucMACAddress[2],
                psGevCamInfo->aucMACAddress[3],
                psGevCamInfo->aucMACAddress[4],
                psGevCamInfo->aucMACAddress[5]);
            printf(" Gev support IP LLA                 : %d\n", psGevCamInfo->cSupportIP_LLA);
            printf(" Gev support IP DHCP                : %d\n", psGevCamInfo->cSupportIP_DHCP);
            printf(" Gev Support IP Persistent-IP       : %d\n", psGevCamInfo->cSupportIP_Persistent);
            printf(" Gev current IP LLA                 : %d\n", psGevCamInfo->cCurrentIP_LLA);
            printf(" Gev current IP DHCP                : %d\n", psGevCamInfo->cCurrentIP_DHCP);
            printf(" Gev current IP Persistent-IP       : %d\n", psGevCamInfo->cCurrentIP_Persistent);
            printf(" Gev IP Address                     : %d.%d.%d.%d\n",
                psGevCamInfo->aucIPAddress[0],
                psGevCamInfo->aucIPAddress[1],
                psGevCamInfo->aucIPAddress[2],
                psGevCamInfo->aucIPAddress[3]);
            printf(" Gev subnet mask                    : %d.%d.%d.%d\n",
                psGevCamInfo->aucSubnet[0],
                psGevCamInfo->aucSubnet[1],
                psGevCamInfo->aucSubnet[2],
                psGevCamInfo->aucSubnet[3]);
            printf(" Gev default gateway                : %d.%d.%d.%d\n",
                psGevCamInfo->aucGateway[0],
                psGevCamInfo->aucGateway[1],
                psGevCamInfo->aucGateway[2],
                psGevCamInfo->aucGateway[3]);
            printf(" Gev adapter MAC address            : %02X-%02X-%02X-%02X-%02X-%02X\n",
                psGevCamInfo->aucAdapterMACAddress[0],
                psGevCamInfo->aucAdapterMACAddress[1],
                psGevCamInfo->aucAdapterMACAddress[2],
                psGevCamInfo->aucAdapterMACAddress[3],
                psGevCamInfo->aucAdapterMACAddress[4],
                psGevCamInfo->aucAdapterMACAddress[5]);
            printf(" Gev adapter IP address             : %d.%d.%d.%d\n",
                psGevCamInfo->aucAdapterIPAddress[0],
                psGevCamInfo->aucAdapterIPAddress[1],
                psGevCamInfo->aucAdapterIPAddress[2],
                psGevCamInfo->aucAdapterIPAddress[3]);
            printf(" Gev adapter subnet mask            : %d.%d.%d.%d\n",
                psGevCamInfo->aucAdapterSubnet[0],
                psGevCamInfo->aucAdapterSubnet[1],
                psGevCamInfo->aucAdapterSubnet[2],
                psGevCamInfo->aucAdapterSubnet[3]);
            printf(" Gev adapter default gateway        : %d.%d.%d.%d\n",
                psGevCamInfo->aucAdapterGateway[0],
                psGevCamInfo->aucAdapterGateway[1],
                psGevCamInfo->aucAdapterGateway[2],
                psGevCamInfo->aucAdapterGateway[3]);
            printf(" Gev adapter display name           : %s\n", psGevCamInfo->szAdapterDisplayName);
        }
    }


    // Open camera that is detected first, in this sample code.
    uint32_t iCamNo = 0;
    uiStatus = Cam_Open(iCamNo, &s_hCam, NULL, false);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 6;
    
    uint32_t puiSensorWidth;
    uiStatus = GetCamSensorWidth(s_hCam, &puiSensorWidth);
    printf(" Effective Sensor Width: %d\n", puiSensorWidth);

    uint32_t puiSensorHeight;
    uiStatus = GetCamSensorHeight(s_hCam, &puiSensorHeight);
    printf(" Effective Sensor Height: %d\n", puiSensorHeight);

    // uiStatus = SetCamWidth(s_hCam, 1920);
    // uiStatus = SetCamWidth(s_hCam, 2448);
    uiStatus = SetCamWidth(s_hCam, gCamWidth);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 7;

    // uiStatus = SetCamHeight(s_hCam, 1080);
    uiStatus = SetCamHeight(s_hCam, gCamHeight);    
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 8;

    uiStatus = SetCamPixelFormat(s_hCam, PXL_FMT_BayerBG8);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 9;

    float64_t dAcqFramerate = 0;

    uiStatus = SetCamGainAuto(s_hCam, CAM_GAIN_AUTO_AUTO);

    uiStatus = SetCamBlackLevel(s_hCam, 4.2);

    uiStatus = SetCamGamma(s_hCam, 0.55);

    uiStatus = SetCamHue(s_hCam, 3.5);

    // uiStatus = SetCamBalanceWhiteAuto(s_hCam, CAM_BALANCE_WHITE_AUTO_ONCE);
    uiStatus = SetCamBalanceRatio(s_hCam, CAM_BALANCE_RATIO_SELECTOR_RED, 1.27);
    uiStatus = SetCamBalanceRatio(s_hCam, CAM_BALANCE_RATIO_SELECTOR_BLUE, 2.44);

    // uiStatus = SetCamReverseX(s_hCam, true);

    uiStatus = SetExposureTime();
    uiStatus = SetFrameRate();
    

    return 0;
}

void Terminate()
{
    // Close camera.
    // if (s_hCam != NULL)
    if (s_hCam != 0)
        Cam_Close(s_hCam);

    // Terminate system.
    Sys_Terminate();
}

uint32_t SetTriggerMode()
{
    // Set TriggerMode false, in this sample code.
    uiStatus = SetCamTriggerMode(s_hCam, false);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 40;

    return 0;
}

uint32_t OpenStream()
{
    // Create completion event for stream.
    Sys_CreateSignal(&s_hStrmEvt);

    // Open stream channel.
    uiStatus = Strm_OpenSimple(s_hCam, &s_hStrm, &s_uiImgBufSize, s_hStrmEvt);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 81;

    uint32_t uiWidth, uiHeight;

    uiStatus = GetCamWidth(s_hCam, &uiWidth);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 900;

    printf("CamWidth: %d\n", uiWidth);

    uiStatus = GetCamHeight(s_hCam, &uiHeight);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 901;

    printf("CamHeight: %d\n", uiHeight);

    uiStatus = GetCamPixelFormat(s_hCam, &s_pixelFormat);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 902;

   
    // Allocate image bufer for receiving image data from TeliCamAPI.
    s_pucImgBuf = (uint8_t *)malloc(s_uiImgBufSize);
    if (s_pucImgBuf == NULL)
        return 82;

    pucImgBGR = new uint8_t[gCamWidth * gCamHeight * 3];
    if (pucImgBGR == NULL)
        return -1;

    //image = malloc(sImageInfo.uiSizeX * sImageInfo.uiSizeY * 3);
    //s_openCvImage = cv::Mat(cv::Size(gCamWidth, gCamHeight), CV_8UC3, cv::Scalar::all(0));
    //cv::namedWindow(s_szWindowTitle, 0); // CV_WINDOW_AUTOSIZE = 0

    return 0;
}

uint32_t CloseStream()
{
    // Close stream.
    // if (s_hStrm != NULL)
    if (s_hStrm != 0)
        Strm_Close(s_hStrm);

    // Close completion event for stream.
    if (s_hStrmEvt != NULL)
        Sys_CloseSignal(s_hStrmEvt);

    // Release image buffer.
    if (s_pucImgBuf != NULL)
        free(s_pucImgBuf);

#ifdef USE_IPL_IMAGE
    if (s_pIplImage != NULL)
        ::cvReleaseImage(&s_pIplImage);
#else
        // Do Nothing
#endif

    cv::destroyWindow(s_szWindowTitle);

    return 0;
}

uint32_t StartAcquisition()
{
    uiStatus = Strm_Start(s_hStrm, CAM_ACQ_MODE_CONTINUOUS);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 100;
    return 0;
}

uint32_t StopAcquisition()
{
    uiStatus = Strm_Stop(s_hStrm);
    if (uiStatus != CAM_API_STS_SUCCESS)
        return 120;

    return 0;
}

bool8_t SetFrameRate()
{
    CAM_API_STATUS  uiStatus = CAM_API_STS_SUCCESS;
    float64_t    dFrameRate = 50.0;
    float64_t dFrameRateMin = 40.0;
    float64_t dFrameRateMax = 60.0;

    printf("\n");
    printf("SetFrameRate() started!\n");

    // Get FrameRate minimum and maximum values.
    uiStatus = GetCamAcquisitionFrameRateMinMax(s_hCam, &dFrameRateMin, &dFrameRateMax);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed GetCamAcquisitionFrameRateMinMax, Status = 0x%08X.\n", uiStatus);
        return false;
    }

    printf(" FrameRate min. :%.4lf, max. :%.4lf [fps] >>> ", dFrameRateMin, dFrameRateMax);

    // Set FrameRate.
    uiStatus = SetCamAcquisitionFrameRate(s_hCam, dFrameRate);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed SetCamAcquisitionFrameRate, Status = 0x%08X.\n", uiStatus);
        return false;
    }

    // Get current FrameRate value.
    uiStatus = GetCamAcquisitionFrameRate(s_hCam, &dFrameRate);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed GetCamAcquisitionFrameRate, Status = 0x%08X.\n", uiStatus);
        return false;
    }
    printf(" Current FrameRate : %.4lf[fps].\n", dFrameRate);

    printf("SetFrameRate() finished!\n");
    
    return true;
}


bool8_t SetExposureTime()
{
    
    float64_t       dExp = 10000, dExpMin, dExpMax;
    

    printf("\n");
    printf("SetExposureTime() started!\n");
    
    uiStatus = GetCamExposureTimeControl(s_hCam, &peExpControl);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed to set exposure control mode to MANUAL, Status = 0x%08X.\n", uiStatus);
        // 오류 처리
        return false;
    }
    
    uiStatus = SetCamExposureTimeControl(s_hCam, peExpControl);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed to set exposure control mode, Status = 0x%08X.\n", uiStatus);
        // 오류 처리
        return false;
    }
    // Get Exposure time minimum and maximum values.
    uiStatus = GetCamExposureTimeMinMax(s_hCam, &dExpMin, &dExpMax);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed GetCamExposureTimeMinMax, Status = 0x%08X.\n", uiStatus);
        return false;
    }

    // Set ExposureTime.
    uiStatus = SetCamExposureTime(s_hCam, dExp);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed SetCamExposureTime, Status = 0x%08X.\n", uiStatus);
        return false;
    }

    // Get current ExposureTime value.
    uiStatus = GetCamExposureTime(s_hCam, &dExp);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed GetCamExposureTime, Status = 0x%08X.\n", uiStatus);
        return false;
    }

    uiStatus = SetCamShortExposureMode(s_hCam, false);
    if (uiStatus != CAM_API_STS_SUCCESS)
    {
        printf("Failed SetCamShortExposureMode, Status = 0x%08X.\n", uiStatus);
        return false;
    }

    printf(" Current exposure time : %.4lf[ms].\n", dExp);

    printf("SetExposureTime() finished!\n");
    return true;
}
