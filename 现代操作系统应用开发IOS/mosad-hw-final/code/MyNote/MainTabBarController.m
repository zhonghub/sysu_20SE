//
//  mainTabBarController.m
//  hw2
//
//  Created by sushan on 2022/9/22.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "MainTabBarController.h"

@interface MainTabBarController ()
@end


@implementation MainTabBarController
- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    _store = [[RecordStorage alloc] init];//初始化数据源
    _vc1 = [[FindViewController alloc] init];
    _vc2 = [[PostViewController alloc] init];
    _vc3 = [[UserViewController alloc] init];
    [_vc2 setOnlyPost];
    [_vc2 setTableView:_vc1.tableview];
    [_vc2 setStore:_store];
    [_vc2 setVc1:_vc1];
    [_vc2 setVc1Nav:_vc1.nav];
    _vc1.store = _store;
    _vc2.store = _store;
    _vc3.store = _store;
    _vc3.tableview = _vc1.tableview;
    // 将3个vc添加到MainTabBarController
    NSArray *array = @[_vc1.nav, _vc2.nav, _vc3.nav];
    self.viewControllers = array;
    [_vc2 setAddButton];
    [_vc2 setBtnClearAndPost];
    // 设置标签栏按钮的图像和文字
    [self setTabBarItem];
    
    //self.selectedIndex = 2;
    NSLog(@"MainTabBarController");
}

//点击空白处键盘隐藏
-(void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event{
    [self.vc2 hidKeyboard];
    [_vc1.search resignFirstResponder];
}

// 调整图像大小
- (UIImage *)scaleToSize:(UIImage *)img size:(CGSize)newsize{
    // 创建一个bitmap的context
    // 并把它设置成为当前正在使用的context
    UIGraphicsBeginImageContext(newsize);
    // 绘制改变大小的图片
    [img drawInRect:CGRectMake(0, 0, newsize.width, newsize.height)];
    // 从当前context中创建一个改变大小后的图片
    UIImage* scaledImage = UIGraphicsGetImageFromCurrentImageContext();
    // 使当前的context出堆栈
    UIGraphicsEndImageContext();
    // 返回新的改变大小后的图片
    return scaledImage;
}
// 以newsize大小获取图像
- (UIImage *)getImg:(NSString*) name size:(CGSize)newsize{
    UIImage *image1 = [UIImage imageNamed:name];
    image1 = [self scaleToSize:image1 size:newsize];
    return image1;
}
// 设置标签栏按钮的图像和文字
-(void) setTabBarItem{
    _vc1.nav.tabBarItem.title = @"发现";
    _vc2.nav.tabBarItem.title = @"打卡";
    _vc3.nav.tabBarItem.title = @"用户";
    UIImage *img1_selected = [self getImg:@"test1_selected.png" size:CGSizeMake(30, 30)];
    UIImage *img1 = [self getImg:@"test1.png" size:CGSizeMake(30, 30)];
    [_vc1.nav.tabBarItem setImage:[img1 imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    [_vc1.nav.tabBarItem setSelectedImage:[img1_selected imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    UIImage *img2_selected = [self getImg:@"test2_selected.png" size:CGSizeMake(30, 30)];
    UIImage *img2 = [self getImg:@"test2.png" size:CGSizeMake(30, 30)];
    [_vc2.nav.tabBarItem setImage:[img2 imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    [_vc2.nav.tabBarItem setSelectedImage:[img2_selected imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    UIImage *img3_selected = [self getImg:@"test3_selected.png" size:CGSizeMake(30, 30)];
    UIImage *img3 = [self getImg:@"test3.png" size:CGSizeMake(30, 30)];
    [_vc3.nav.tabBarItem setImage:[img3 imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    [_vc3.nav.tabBarItem setSelectedImage:[img3_selected imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    //[_vc3.nav.tabBarItem setFinishedSelectedImage:img3_selected  //已弃用的API     withFinishedUnselectedImage:img3];
}

@end
