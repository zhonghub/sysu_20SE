//
//  FindViewController.h
//  hw2
//
//  Created by sushan on 2022/9/20.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef FindViewController_h
#define FindViewController_h
#import <UIKit/UIKit.h>
#import "PostViewController.h"
#import "RecordStorage.h"

@interface FindViewController : UIViewController<UITableViewDataSource, UITableViewDelegate, UISearchBarDelegate>
@property(nonatomic,strong) RecordStorage *store;
@property(nonatomic,strong) UISearchBar *search;
@property(nonatomic,strong) UITableView *tableview;
@property(nonatomic,strong) UINavigationController *nav;
@property(nonatomic, strong)CAGradientLayer * gradient;// 渐变层
-(void)returnTop;
+ (FindViewController *)getInstance;
@end

#endif /* FindViewController_h */
