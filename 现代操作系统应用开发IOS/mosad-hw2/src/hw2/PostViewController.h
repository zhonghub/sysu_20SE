//
//  postViewController.h
//  hw2
//
//  Created by sushan on 2022/9/22.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef PostViewController_h
#define PostViewController_h
#import <UIKit/UIKit.h>
#import "RecordStorage.h"

@interface PostViewController : UIViewController<UINavigationControllerDelegate,UIImagePickerControllerDelegate>
@property(nonatomic,strong) UIView *view1;
@property(nonatomic,strong) UINavigationController *nav;
@property(nonatomic,strong) UITextField * inputDate;  // 打卡文字输入
@property(nonatomic,strong) UITextField * inputPlace;
@property(nonatomic,strong) UITextField * inputSights;
@property(nonatomic,strong) UITextView * inputExp;
@property(nonatomic,strong) NSMutableArray<UIImage *> * imgs; // 打卡图片
@property(nonatomic,strong) UIButton * addButton;
@property(nonatomic,strong) UIImagePickerController *imagePicker;// 图片选择控制器
@property(nonatomic,strong)CAGradientLayer * gradient;// 渐变层
-(void) setAddButton; // 打卡页面使用，设置添加图片按钮
-(void) showWith:(Record *) r1; // 详情页面使用，将记录r1展示出来
-(CGRect) getPos:(unsigned long)i; // 图片的自动布局使用，返回第i张图片的自动布局
@end

#endif /* postViewController_h */
