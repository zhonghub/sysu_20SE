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
@property(nonatomic,strong) CAGradientLayer * gradient;// 渐变层
@property(nonatomic,strong) NSDictionary * r0;
-(void) setOnlyPost;
-(void) setTableView:(UITableView *) table0;
-(void) setStore:(RecordStorage *) store1;
-(void) setVc1:(UIViewController *) vc;
-(void) setVc1Nav:(UINavigationController *) nav;
-(void) setAddButton; // 打卡页面使用，设置添加图片按钮
-(void) showWith:(NSDictionary *) r1; // 详情页面使用，将记录r1展示出来
-(void) closeInput;
-(CGRect) getPos:(unsigned long)i; // 图片的自动布局使用，返回第i张图片的自动布局
-(PostViewController*)initWithItem:(NSDictionary *) r1;
-(void) setEditorButton;
-(void) setBtnClearAndPost;
// 隐藏打卡页面键盘
-(void)hidKeyboard;
// 打卡页面清空输入框和图片
-(void)clearInput;
@end

#endif /* postViewController_h */
