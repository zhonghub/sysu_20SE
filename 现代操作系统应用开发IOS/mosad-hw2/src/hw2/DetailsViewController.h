//
//  DetailsViewController.h
//  hw2
//
//  Created by sushan on 2022/9/29.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef DetailsViewController_h
#define DetailsViewController_h
#import <UIKit/UIKit.h>
#import "RecordStorage.h"
#import "PostViewController.h"

@interface DetailsViewController : UIViewController
@property(nonatomic,strong) PostViewController * vc;
-(DetailsViewController*)initWithItem:(Record *) r1;
@end

#endif /* DetailsViewController_h */
