//
//  mainTabBarController.h
//  hw2
//
//  Created by sushan on 2022/9/22.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef MainTabBarController_h
#define MainTabBarController_h

#import <UIKit/UIKit.h>
#import "DetailsViewController.h"
#import "FindViewController.h"
#import "MyViewController.h"
#import "PostViewController.h"
#import "RecordStorage.h"

@interface MainTabBarController :  UITabBarController
@property(nonatomic,strong) FindViewController*vc1;
@property(nonatomic,strong) PostViewController*vc2;
@property(nonatomic,strong) MyViewController*vc3;

@end

#endif /* mainTabBarController_h */
