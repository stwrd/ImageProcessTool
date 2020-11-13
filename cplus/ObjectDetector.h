//
// Created by stwrd on 2019/6/12.
//

#ifndef THROW_DETECT_INFERENCE_OBJECTDETECTOR_H
#define THROW_DETECT_INFERENCE_OBJECTDETECTOR_H

#include <opencv2/opencv.hpp>
#include <torch/script.h>
#include <string>

using std::string;
using std::vector;
using namespace cv;

class ObjectDetector {
public:
    void init(string model_path, int ,int );
    Mat resize_for_srcImg(const cv::Mat& src_img, int yolo_width, int yolo_height);
    Mat resize_square_for_imgList(const vector<cv::Mat>& imgList, int tar_width, int tar_height);
    Mat resize_square_for_img(const cv::Mat& img, int tar_width, int tar_height);
    torch::Tensor predict_imglist(std::vector<Mat>& img_list);
    torch::Tensor predict(Mat& img);

    std::shared_ptr<torch::jit::script::Module> m_module;
    int m_yolo_width;
    int m_yolo_height;
    float *m_PredictData;
};


#endif //THROW_DETECT_INFERENCE_OBJECTDETECTOR_H
