//
//  RegisterController.h
//  hw3
//
//  Created by sushan on 2022/10/13.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef RegisterController_h
#define RegisterController_h
#import <UIKit/UIKit.h>
#import "MyHttpAPI.h"
#import "GraphicListController.h"
#import "UserViewController.h"

@interface RegisterController : UIViewController
@property(nonatomic,strong) MyHttpAPI * myAPI;// 负责网络通信
@property(nonatomic,strong) UIView * view1;// 登录前页面
@property(nonatomic,strong) UITabBarController *tab;// 登录后页面:(个人信息页面,评论图文列表页面)
@property(nonatomic,strong) UserViewController * userVc;// 个人信息页面
@property(nonatomic,strong) GraphicListController *graph;// 评论图文列表页面
@property(nonatomic) UITextField * inputName; // 输入框
@property(nonatomic) UITextField * inputPassword;
@property(nonatomic) UITextField * inputVerify;
@property(nonatomic,strong) UIButton * btn2; //刷新验证码按钮
@end

#endif /* RegisterController_h */
