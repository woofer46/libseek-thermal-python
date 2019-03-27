/*
 *  Test program SEEK Thermal Compact/CompactXR
 *  Author: Maarten Vandersteegen
 */
#include <opencv2/highgui/highgui.hpp>
#include "seek.h"
#include <iostream>
#include <unistd.h>
static int show_frames = 0;
int main(int argc, char** argv)
{
    if(argc > 1) {
        show_frames = 1;
    }
    LibSeek::SeekThermalPro seek(argc == 2 ? argv[1] : "");
    cv::Mat frame, grey_frame;

    if (!seek.open()) {
        std::cerr << "failed to open seek cam" << std::endl;
        return -1;
    }

    while(1) {
        if (!seek.read(frame)) {
            std::cout << "no more LWIR img" << std::endl;
            return -1;
        }
        std::cerr << "rows: " << frame.rows << " coloumns: " << frame.cols << std::endl;
        
        cv::normalize(frame, grey_frame, 0, 65535, cv::NORM_MINMAX);
        ssize_t res = ::write(1, grey_frame.data, (size_t)((grey_frame.rows * grey_frame.cols) * 2));
        std::cerr << "res: " << res << std::endl;

        /*if(show_frames){
            cv::imshow("LWIR", grey_frame);

            char c = cv::waitKey(1);
            if (c == 's') {
               return -1;
            }
        }*/
    }
}
