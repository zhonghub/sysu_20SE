//
//  DetailsViewController.m
//  hw2
//
//  Created by sushan on 2022/9/29.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "DetailsViewController.h"
@implementation DetailsViewController
-(DetailsViewController*)initWithItem:(Record *) r1{
    NSLog(@"打卡详情");
    self.navigationItem.title=@"打卡详情";
    self.view=[[UIView alloc]initWithFrame:CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height)];
    _vc = [[PostViewController alloc] init];
    [_vc showWith:r1];
    [self.view addSubview:_vc.view];
    return self;
}

@end
