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
    _vc1 = [[FindViewController alloc] init];
    _vc2 = [[PostViewController alloc] init];
    _vc3 = [[MyViewController alloc] init];
    // 将3个vc添加到MainTabBarController
    NSArray *array = @[_vc1.nav, _vc2.nav, _vc3.nav];
    self.viewControllers = array;
    [_vc2 setAddButton];
    // 设置标签栏按钮的图像和文字
    [self setTabBarItem];
    
    // 4个测试打卡，无图片
    [_vc1.store storeWithData:@"2022/9/18" andPlace:@"place1" andSights:@"sights1" andExp:@"nice1" andImgs:[[NSMutableArray alloc] init]];
    [_vc1.store storeWithData:@"2022/9/20" andPlace:@"place2" andSights:@"sights2" andExp:@"nice2" andImgs:[[NSMutableArray alloc] init]];
    [_vc1.store storeWithData:@"2022/9/23" andPlace:@"place3" andSights:@"sights3" andExp:@"nice3" andImgs:[[NSMutableArray alloc] init]];
    [_vc1.store storeWithData:@"2022/10/2" andPlace:@"place4" andSights:@"sights4" andExp:@"nice4" andImgs:[[NSMutableArray alloc] init]];
    
    // 给vc2增加一个“返回顶部”按钮
    _vc1.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"返回顶部" style:UIBarButtonItemStyleDone target:self action:@selector(returnTop)];
    
    // 给vc2增加一个“发布”按钮
    _vc2.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"发布" style:UIBarButtonItemStyleDone target:self action:@selector(btnClick1)];
    
    // 给vc2增加一个“清空”按钮
    _vc2.navigationItem.leftBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"清空"  style:UIBarButtonItemStyleDone target:self action:@selector(btnClick2)];
    
    NSLog(@"MainTabBarController");
}

//点击空白处键盘隐藏
-(void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event{
    [self hidKeyboard];
    [_vc1.search resignFirstResponder];
}
// 隐藏打卡页面键盘
-(void)hidKeyboard{
    [_vc2.inputDate resignFirstResponder];
    [_vc2.inputPlace resignFirstResponder];
    [_vc2.inputSights resignFirstResponder];
    [_vc2.inputExp resignFirstResponder];
}
// 打卡页面清空输入框和图片
-(void)clearInput{
    NSLog(@"clearInput");
    self.vc2.inputDate.text=@"";
    self.vc2.inputPlace.text=@"";
    self.vc2.inputSights.text=@"";
    self.vc2.inputExp.text = @"";
    // 删除图片在打卡页面的子视图
    for(UIView *mylabelview in [_vc2.view1 subviews]){
        if ([mylabelview isKindOfClass:[UIImageView class]]) {
            [mylabelview removeFromSuperview];
        }
    }
    // 清空选择的图片
    self.vc2.imgs = [[NSMutableArray<UIImage *> alloc] init];
    // 添加按钮回到起点
    self.vc2.addButton.frame = [self.vc2 getPos:0];
    // 添加按钮设为可用
    self.vc2.addButton.enabled=true;
}

// 发现页面返回顶部并更新UItableView
-(void)returnTop{
    // 发现页面转到最顶部,并更新tableView
    [UIView animateWithDuration:0 animations:^{
        [self.vc1.tableview setContentOffset:CGPointZero animated:NO];
    } completion:^(BOOL finished) {
        [self.vc1.tableview reloadData];// 更新tableView
    }];
}

//发布按钮
- (void)btnClick1{
    // 隐藏键盘
    [self hidKeyboard];
    NSLog(@"button1 is click");
    // 如果时间、地点、景点存在为空的情况，不能发布，需要继续编辑打卡
    if( [_vc2.inputDate.text isEqual:@""] || [_vc2.inputPlace.text isEqual:@""] || [_vc2.inputSights.text isEqual:@""]){
        UIAlertController *alertVC0 = [UIAlertController alertControllerWithTitle:@"提示" message:@"时间、地点、景点不能为空！" preferredStyle:UIAlertControllerStyleAlert];
        UIAlertAction *comfirmAc0 = [UIAlertAction actionWithTitle:@"继续编辑"     style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {}];
        [alertVC0 addAction:comfirmAc0];
        [_vc2 presentViewController:alertVC0 animated:YES completion:nil];
        return;
    }
    UIAlertController *alertVC = [UIAlertController alertControllerWithTitle:@"提示" message:@"是否发布打卡？" preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *comfirmAc = [UIAlertAction actionWithTitle:@"是，查看最新打卡"     style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        // 代码块隐式地保留'self'; 明确地使用“self”来表示这是有意的行为
        // 将数据添加到数据源
        [self.vc1.store storeWithData:self.vc2.inputDate.text andPlace:self.vc2.inputPlace.text andSights:self.vc2.inputSights.text andExp:self.vc2.inputExp.text andImgs:self.vc2.imgs];
        // 发现页面先返回根视图tableView（如果当前页面不是tableView）
        [self.vc1.nav popToRootViewControllerAnimated:YES];
        // 发现页返回顶部并更新数据源
        [self returnTop];
        // 转到发现页面
        self.vc2.tabBarController.selectedIndex=0;//tabBarController
        DetailsViewController *dectrl = [[DetailsViewController alloc] initWithItem:self.vc1.store.records[0]];
        // 再进入打卡详情页面，查看最新打卡
        [self.vc1.nav pushViewController:dectrl animated:YES];
        // 0.5s的弹窗
        UIAlertController *alert1 = [UIAlertController alertControllerWithTitle:@"提示" message:@"发布成功" preferredStyle:UIAlertControllerStyleAlert];
        // 弹窗以浮动形式加到vc1
        [self.vc1 presentViewController:alert1 animated:YES completion:nil];
        [self performSelector:@selector(delayAlert1) withObject:nil afterDelay:0.5f];
        // 清除输入框和图片
        [self clearInput];
    }];
    UIAlertAction *comfirmAc2 = [UIAlertAction actionWithTitle:@"否，继续编辑" style:UIAlertActionStyleDefault handler:nil];
    [alertVC addAction:comfirmAc];
    [alertVC addAction:comfirmAc2];
    [_vc2 presentViewController:alertVC animated:YES completion:nil];
}
// 去除弹窗
-(void) delayAlert1{
    [self.vc1 dismissViewControllerAnimated:YES completion:nil];
}

// 清空按钮
- (void)btnClick2{
    [self hidKeyboard];
    NSLog(@"button2 is click");
    UIAlertController *alertVC = [UIAlertController alertControllerWithTitle:@"提示" message:@"是否清空打卡内容？" preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *comfirmAc = [UIAlertAction actionWithTitle:@"是" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        // 清除输入框
        [self clearInput];
    }];
    UIAlertAction *comfirmAc2 = [UIAlertAction actionWithTitle:@"否" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {}];
    [alertVC addAction:comfirmAc];
    [alertVC addAction:comfirmAc2];
    [_vc2 presentViewController:alertVC animated:YES completion:nil];
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
    _vc3.nav.tabBarItem.title = @"我的";
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
