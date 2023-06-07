//
//  myViewController.m
//  hw2
//
//  Created by sushan on 2022/9/20.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "MyViewController.h"
@implementation MyViewController
-init{
    self.navigationItem.title = @"登录";
    _view1 = [[UIView alloc]initWithFrame:CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height*0.8)];
    [self setUI2];// 绘制渐变图层
    [self setBtn];// 添加登陆按钮
    self.nav = [[UINavigationController alloc]initWithRootViewController:self];
    [self.view addSubview:_view1];
    return self;
}
-(void)setBtn{
    _btn = [[UIButton alloc] initWithFrame:CGRectMake(0, 0, 130, 130)];
    [_btn addTarget:self action:@selector(logIn) forControlEvents:UIControlEventTouchUpInside];
    _btn.center=CGPointMake(_view1.center.x, _view1.center.y);
    _btn.layer.borderColor=[UIColor blackColor].CGColor;
    _btn.layer.borderWidth=2;
    _btn.layer.cornerRadius = _btn.bounds.size.width / 2.0; // 圆形按钮
    [_btn setTitle: @"登录" forState: UIControlStateNormal];
    _btn.titleLabel.font = [UIFont systemFontOfSize: 25.0];
    _btn.backgroundColor = [UIColor clearColor];
    [_btn setTitleColor:[UIColor blackColor]forState:UIControlStateNormal];
    [_view1 addSubview:_btn];
}
// 登录按钮绑定事件
-(void)logIn{
    [self setVc];
    //[self.nav pushViewController:_vc animated:YES];
    // 0.8s的弹窗,弹窗时间不能太短；或者可去除弹窗
    UIAlertController *alert1 = [UIAlertController alertControllerWithTitle:@"提示" message:@"登录成功!" preferredStyle:UIAlertControllerStyleAlert];
    // 弹窗以浮动形式加到self
    [self presentViewController:alert1 animated:YES completion:nil];
    [self performSelector:@selector(delayAlert1) withObject:nil afterDelay:0.8f];
    // 转到登录后的界面
    // [self.nav pushViewController:_vc animated:YES];//error!
}
-(void) delayAlert1{
    [self dismissViewControllerAnimated:YES completion:nil];
    [self.nav pushViewController:_vc animated:YES]; // 转到登录后的界面
}
// 设置登录后界面
-(void)setVc{
    _vc = [[UIViewController alloc]init];
    UIView *view2 = [[UIView alloc] initWithFrame:CGRectMake(0,0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height)];
    view2.backgroundColor = [UIColor colorWithRed:0xa5/255.0 green:0x75/255.0 blue:0x64/255.0 alpha:1];
    [self addImg:view2 withName:@"test3_selected.png"];
    CGFloat h = [UIScreen mainScreen].bounds.size.height; // 用于自动布局
    CGFloat w = [UIScreen mainScreen].bounds.size.width; // 用于自动布局
    UILabel *label = [[UILabel alloc] initWithFrame:CGRectMake(0.35*w,h*0.4,0.6*w,90)];
    label.layer.borderWidth = 2;
    label.layer.borderColor = [UIColor grayColor].CGColor;
    [view2 addSubview:label];
    UILabel *label2 = [[UILabel alloc] initWithFrame:CGRectMake(40,h*0.6,(w-40)*0.7,180)];
    label2.layer.borderWidth = 3;
    label2.layer.borderColor = [UIColor grayColor].CGColor;
    [view2 addSubview:label2];
    
    [self addLabel:view2 withText:@"用户名:test" withFrame:CGRectMake(0.35*w+10,h*0.4,0.6*w-10,30) withFont:16.0];
    [self addLabel:view2 withText:@"邮箱:12345@qq.com" withFrame:CGRectMake(0.35*w+10,h*0.4+30,0.6*w-10,30) withFont:16.0];
    [self addLabel:view2 withText:@"电话:12345" withFrame:CGRectMake(0.35*w+10,h*0.4+60,0.6*w-10,30) withFont:16.0];
    [self addLabel:view2 withText:@"关于" withFrame:CGRectMake(40,h*0.5,52,h*0.1) withFont:25.0];
    [self addLabel:view2 withText:@"版本" withFrame:CGRectMake(50,h*0.6,200,40) withFont:20.0];
    [self addLabel:view2 withText:@"隐私和cookie" withFrame:CGRectMake(50,h*0.6+40,200,40) withFont:20.0];
    [self addLabel:view2 withText:@"清除缓存" withFrame:CGRectMake(50,h*0.6+80,200,40) withFont:20.0];
    [self addLabel:view2 withText:@"同步" withFrame:CGRectMake(50,h*0.6+120,200,40) withFont:20.0];
    _vc.navigationItem.title=@"我的";
    [_vc.view addSubview:view2];
}

// 通过：内容、框架、字号添加一个label
-(void)addLabel:(UIView*)view2 withText:(NSString*)str withFrame:(CGRect)r1 withFont:(CGFloat)f1{
    UILabel *label1 = [[UILabel alloc] initWithFrame:r1];
    label1.text = str;//text是输入的结果
    label1.font = [UIFont systemFontOfSize: f1];
    label1.textAlignment = NSTextAlignmentLeft;
    [view2 addSubview:label1];
}
// 增加一个圆形图像
-(void)addImg:(UIView*)view2 withName:(NSString*)str{
    CGFloat h = [UIScreen mainScreen].bounds.size.height; // 用于自动布局
    UIImageView *v1 = [[UIImageView alloc] initWithFrame:CGRectMake(0,0,h*0.24,h*0.24)];
    v1.center=CGPointMake(self.view.bounds.size.width/2,h*0.24);
    v1.backgroundColor = [UIColor clearColor];
    v1.layer.masksToBounds = YES;
    v1.layer.cornerRadius = h*0.12;
    v1.layer.borderColor=[UIColor grayColor].CGColor;
    v1.layer.borderWidth=2;
    UIImage *image1 = [UIImage imageNamed:str];
    [v1 setImage:image1];
    [view2 addSubview:v1];
    
}
// 画出圆半径方向渐变图层
- (void)drawRadialGradient:(CGContextRef)context path:(CGPathRef)path
    startColor:(CGColorRef)startColor endColor:(CGColorRef)endColor{
    CGColorSpaceRef colorSpace = CGColorSpaceCreateDeviceRGB();
    CGFloat locations[] = { 0.0, 1.0 };
    NSArray *colors = @[(__bridge id) startColor, (__bridge id) endColor];
    CGGradientRef gradient = CGGradientCreateWithColors(colorSpace, (__bridge CFArrayRef) colors, locations);
    
    CGRect pathRect = CGPathGetBoundingBox(path);
    CGPoint center = CGPointMake(CGRectGetMidX(pathRect), CGRectGetMidY(pathRect));
    CGFloat radius = MAX(pathRect.size.width/2, pathRect.size.height/2) * sqrt(2);
    
    CGContextSaveGState(context);
    CGContextAddPath(context, path);
    CGContextEOClip(context);
    CGContextDrawRadialGradient(context, gradient, center, 0, center, radius, 0);
    CGContextRestoreGState(context);
    CGGradientRelease(gradient);
    CGColorSpaceRelease(colorSpace);
}

-(void)setUI2{
    //创建CGContextRef
    UIGraphicsBeginImageContext(self.view.bounds.size);
    CGContextRef gc = UIGraphicsGetCurrentContext();
    //创建CGMutablePathRef
    CGMutablePathRef path = CGPathCreateMutable();
    //绘制Path
    CGRect rect = CGRectMake(0, 0, _view1.bounds.size.width, _view1.bounds.size.height);
    CGPathMoveToPoint(path, NULL, CGRectGetMinX(rect), CGRectGetMinY(rect));
    CGPathAddLineToPoint(path, NULL, CGRectGetMinX(rect), CGRectGetMaxY(rect));
    CGPathAddLineToPoint(path, NULL, CGRectGetMaxX(rect), CGRectGetMaxY(rect));
    CGPathAddLineToPoint(path, NULL, CGRectGetMaxX(rect), CGRectGetMinY(rect));
    CGPathCloseSubpath(path);
    //绘制渐变
    [self drawRadialGradient:gc path:path startColor:[UIColor colorWithRed:0xe5/255.0 green:0x25/255.0 blue:0xe4/255.0 alpha:1].CGColor endColor:[UIColor colorWithRed:0x35/255.0 green:0xe5/255.0 blue:0x64/255.0 alpha:1].CGColor];
    //注意释放CGMutablePathRef
    CGPathRelease(path);
    //从Context中获取图像，并显示在界面上
    UIImage *img = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    UIImageView *imgView = [[UIImageView alloc] initWithImage:img];
    [_view1 addSubview:imgView];
}

@end
