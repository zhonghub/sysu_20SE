//
//  myViewController.h
//  hw2
//
//  Created by sushan on 2022/9/20.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef MyViewController_h
#define MyViewController_h
//#include "BaseViewController.h"
#import <UIKit/UIKit.h>
@interface MyViewController : UIViewController
@property(nonatomic,strong) UINavigationController *nav;
@property(nonatomic,strong) UIView * view1;
@property(nonatomic,strong) UIButton * btn; //圆形登录按钮
@property(nonatomic,strong) UIViewController *vc;
@end

#endif /* myViewController_h */
