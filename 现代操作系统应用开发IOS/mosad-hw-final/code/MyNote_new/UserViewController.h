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
#import "RecordStorage.h"

@interface UserViewController : UIViewController
@property(nonatomic,strong) UIView *view1;
@property(nonatomic,strong) UINavigationController *nav;
@property(nonatomic,strong) RecordStorage *store;
@property(nonatomic,strong) UITableView *tableview;
@end

#endif /* UserViewController_h */
