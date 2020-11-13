//
// Created by stwrd on 2019/6/12.
//

#include "ObjectDetector.h"

typedef struct _DET_OUTPUT {
    float x1;
    float y1;
    float x2;
    float y2;
    float conf;
    int cls;
}*pDET_OUTPUT, DET_OUTPUT;

void ObjectDetector::init(string model_path, int yolo_width, int yolo_height)
{
    m_module = torch::jit::load(model_path.c_str());
    m_yolo_width = yolo_width;
    m_yolo_height = yolo_height;
}

//按长边对齐缩放
cv::Mat ObjectDetector::resize_for_srcImg(const cv::Mat& src_img, int yolo_width, int yolo_height)
{
    int new_w = 0;
    int new_h = 0;
    if (((float)yolo_width/src_img.cols) < ((float)yolo_height/src_img.rows)) {
        new_w = yolo_width;
        new_h = (src_img.rows * yolo_width)/src_img.cols;
    } else {
        new_h = yolo_height;
        new_w = (src_img.cols * yolo_height)/src_img.rows;
    }
    Mat resize_img;
    cv::resize(src_img,resize_img,cv::Size(new_w,new_h));
    return resize_img;
}

cv::Mat ObjectDetector::resize_square_for_imgList(const vector<cv::Mat>& imgList, int tar_width, int tar_height)
{
    //添加resize函数
    vector<cv::Mat> resize_imgList;
    for(auto i = 0; i < imgList.size(); i++)
    {
        Mat tmp = resize_for_srcImg(imgList[i],tar_width,tar_height);
        resize_imgList.emplace_back(tmp);//还未做填充
    }

    //初始化需要填充的边界
    int src_height = resize_imgList[0].rows;
    int src_width = resize_imgList[0].cols;
    assert(src_height <= tar_height && src_width <= tar_width);
    int top = (tar_height-src_height)/2;
    int bottom = tar_height - top - src_height;
    int left = (tar_width-src_width)/2;
    int right = tar_width - left - src_width;

    //融合图片，并填充
    Mat result(tar_height,tar_width,CV_32FC3, cv::Scalar(0));
    int tar_img_size = tar_height*tar_width*sizeof(float);
    vector<vector<int> > bgr_vec{ { 0, 1, 2 }, { 3, 4, 5}, { 6, 7, 8 } };  //BGR分别对应的通道

    for (int i = 0; i < 3; i++)
    {
        Mat color_Mat(src_height, src_width, CV_32FC1, cv::Scalar(0));
        for (int j = 0; j < bgr_vec[i].size(); j++)
        {
            Mat tmp;
            cvtColor(imgList[bgr_vec[i][j]], tmp, cv::COLOR_BGR2GRAY);
            tmp.convertTo(tmp, CV_32FC1);
            color_Mat += tmp;
        }
        color_Mat = color_Mat/bgr_vec[i].size()/255.0;

        Mat fill_img;
        cv::copyMakeBorder(color_Mat,fill_img,top,bottom,left,right,cv::BORDER_CONSTANT,cv::Scalar::all(0.5));
//		printf("fill_img size is %d     %d\n",fill_img.rows,fill_img.cols);
        memcpy(result.data + (2-i)*tar_img_size, fill_img.data, tar_img_size);
    }
    return result;
}

cv::Mat ObjectDetector::resize_square_for_img(const cv::Mat& img, int tar_width, int tar_height)
{
    //添加resize函数
    cv::Mat resize_img = resize_for_srcImg(img,tar_width,tar_height);
    resize_img.convertTo(resize_img,CV_32FC1);

    //初始化需要填充的边界
    int src_height = resize_img.rows;
    int src_width = resize_img.cols;
    assert(src_height <= tar_height && src_width <= tar_width);
    int top = (tar_height-src_height)/2;
    int bottom = tar_height - top - src_height;
    int left = (tar_width-src_width)/2;
    int right = tar_width - left - src_width;

    Mat fill_img;
    cv::copyMakeBorder(resize_img,fill_img,top,bottom,left,right,cv::BORDER_CONSTANT,cv::Scalar::all(128));

    fill_img = fill_img/255.0;
    return fill_img;
}

torch::Tensor ObjectDetector::predict_imglist(std::vector<Mat>& img_list)
{
    Mat fuse_img = resize_square_for_imgList(img_list,m_yolo_width,m_yolo_height);
    return predict(fuse_img);;
}

torch::Tensor ObjectDetector::predict(Mat& img)
{
    Mat square_img = resize_square_for_img(img,416,416);
//    std::cout<<square_img.size()<<std::endl;
    for (int i = 0; i < square_img.rows; ++i) {
        float* pImg = square_img.ptr<float>(i);
        for (int j = 0; j < square_img.cols; ++j) {
            float v = pImg[j*3];
            pImg[j*3] = pImg[j*3+2];
            pImg[j*3+2] = v;
        }
    }
//    cv::imwrite("xxx.jpg",square_img*255);
//    square_img.setTo(0.3);
//    std::cout<<img.size()<<std::endl;
    torch::Tensor tensor_image = torch::from_blob(square_img.data,{1,square_img.rows,square_img.cols,3},torch::kFloat);
    tensor_image = tensor_image.permute({0,3,1,2});
//    std::cout<<tensor_image<<std::endl;
    std::cout<<"upload to gpu"<<std::endl;
    tensor_image = tensor_image.to(torch::kCUDA);
    std::cout<<"begin to foward"<<std::endl;
    torch::Tensor output = m_module->forward({tensor_image}).toTensor();
//    auto output = m_module->forward({inputs});

    std::cout<<output.sizes()<<std::endl;
    return output;
}

//void ObjectDetector::correctionBbox(int src_height, int src_weight) {
//    pDET_OUTPUT pYolo_Data = (pDET_OUTPUT)m_PredictData;
//    float pad_x = MAX(src_height - src_weight, 0) * ((float)STANDARD_SIZE / MAX(src_height, src_weight));
//    float pad_y = MAX(src_weight - src_height, 0) * ((float)STANDARD_SIZE / MAX(src_height, src_weight));
//    float unpad_h = STANDARD_SIZE - pad_y;
//    float unpad_w = STANDARD_SIZE - pad_x;
//
//    for (int i = 0; i < mTagetNum; ++i) {
//        float box_h = ((pYolo_Data[i].y2 - pYolo_Data[i].y1) / unpad_h) * src_height;
//        float box_w = ((pYolo_Data[i].x2 - pYolo_Data[i].x1) / unpad_w) * src_weight;
//        pYolo_Data[i].y1 = ((int(pYolo_Data[i].y1 - pad_y / 2) / unpad_h) * src_height);
//        pYolo_Data[i].x1 = ((int(pYolo_Data[i].x1 - pad_x / 2) / unpad_w) * src_weight);
//        pYolo_Data[i].x2 = (pYolo_Data[i].x1 + box_w);
//        pYolo_Data[i].y2 = (pYolo_Data[i].y1 + box_h);
//        pYolo_Data[i].x1 = MAX(pYolo_Data[i].x1, 0);
//        pYolo_Data[i].y1 = MAX(pYolo_Data[i].y1, 0);
//        pYolo_Data[i].x2 = MIN(pYolo_Data[i].x2, src_weight);
//        pYolo_Data[i].y2 = MIN(pYolo_Data[i].y2, src_height);
//    }
//}
