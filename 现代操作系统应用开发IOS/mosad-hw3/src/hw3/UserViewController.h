//
//  UserViewController.h
//  hw3
//
//  Created by sushan on 2022/10/19.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef UserViewController_h
#define UserViewController_h

#import <UIKit/UIKit.h>

@interface UserViewController : UIViewController
@property(nonatomic,strong) UIScrollView * view1;
@property(nonatomic,strong) NSDictionary *dic;
-(instancetype)initWithFrame:(CGRect)frame andInfo:(NSDictionary *) dic1;
@end


#endif /* UserViewController_h */
