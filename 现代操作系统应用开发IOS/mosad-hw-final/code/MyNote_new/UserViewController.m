//
//  UserViewController.m
//  hw3
//
//  Created by sushan on 2022/10/19.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "UserViewController.h"

@implementation UserViewController
-(instancetype)init{
    self.navigationItem.title =@"存储管理";
    self.view = [[UIView alloc]initWithFrame:CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height)];
    _view1 = [[UIView alloc]initWithFrame:CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height)];
    _view1.backgroundColor = [UIColor whiteColor];
    [self setUI2];
    [self setUI];
    self.nav = [[UINavigationController alloc]initWithRootViewController:self];
    [self.view addSubview:_view1];
    return self;

}

-(void)setUI{
    //self.tabBarItem.title = @"用户管理";
    // 图文列表界面设置4个按钮
    CGFloat w = self.view.bounds.size.width;
    [self addBtnText:@"加载" Withx:0.3*w Withy:0.4*w WithSize:0.35*w withAction:@selector(action1)];
    [self addBtnText:@"清空" Withx:0.7*w Withy:0.4*w WithSize:0.35*w withAction:@selector(action2)];
    [self addBtnText:@"删除缓存" Withx:0.3*w Withy:0.8*w WithSize:0.35*w withAction:@selector(action3)];
    [self addBtnText:@"查看缓存" Withx:0.7*w Withy:0.8*w WithSize:0.35*w withAction:@selector(action4)];
}

// 圆形按钮
-(void)addBtnText:(NSString*)text Withx:(CGFloat)x Withy:(CGFloat)y WithSize:(CGFloat)size withAction:(SEL)action0{
    UIButton * btn = [[UIButton alloc] initWithFrame:CGRectMake(0, 0, size, size)];
    [btn addTarget:self action:action0 forControlEvents:UIControlEventTouchUpInside];
    btn.center=CGPointMake(x, y);
    btn.layer.borderColor=[UIColor blackColor].CGColor;
    btn.layer.borderWidth=2;
    btn.layer.cornerRadius = btn.bounds.size.width / 2.0; // 圆形按钮
    [btn setTitle:text forState: UIControlStateNormal];
    btn.titleLabel.font = [UIFont systemFontOfSize: size/1.5/[text length]];
    btn.backgroundColor = [UIColor clearColor];
    [btn setTitleColor:[UIColor blackColor]forState:UIControlStateNormal];
    [_view1 addSubview:btn];
}

// 按钮绑定事件
// 加载：本地不存在，从网络加载并保存到cache；否则从cache加载
-(void)action1{
    NSLog(@"重新加载");
    [self.store clearList];
    [self.store readFromCache];
    [_tableview reloadData];
    [self addAlertTitle:@"提示" andMsg:@"重新加载" andComfirm:@"确定"];
}
-(void)action2{
    NSLog(@"清空");
    [_store clearList];
    [_tableview reloadData];
    [self addAlertTitle:@"提示" andMsg:@"清空成功!" andComfirm:@"确定"];
}
-(void)action3{
    NSLog(@"删除缓存");// 删除缓存
    [_store clearList];
    [[NSFileManager defaultManager] removeItemAtPath:_store.imageCachePath error:nil];
    [[NSFileManager defaultManager] removeItemAtPath:_store.listCachePath error:nil];
    [_store initCache];
    [self.store readFromCache];
    [_tableview reloadData];
    [self addAlertTitle:@"提示" andMsg:@"已将本地缓存删除!" andComfirm:@"确定"];
}

-(void)action4{
    NSLog(@"查看缓存");// 查看缓存
    NSArray *file = [[[NSFileManager alloc] init] subpathsAtPath:_store.imageCachePath];
    // NSLog(@"img=%@",file);
    NSArray *file2 = [[[NSFileManager alloc] init] subpathsAtPath:_store.listCachePath];
    // NSLog(@"list=%@",file2);
    /*NSString * msg = [NSString stringWithFormat:@"图片缓存: %ld张\n %@ \nnote笔记: %ld条\n %@ \n",file.count, file, file2.count, file2];*/
    NSString * msg = [NSString stringWithFormat:@"图片缓存: %ld张\n note笔记: %ld条\n",file.count, file2.count];
    [self addAlertTitle:@"查看缓存" andMsg:msg andComfirm:@"确定"];
}

// 增加弹窗
-(void)addAlertTitle:(NSString*)title andMsg:(NSString*)msg andComfirm:(NSString*)comfirm{
    UIAlertController *alertVC = [UIAlertController alertControllerWithTitle:title message:msg preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *comfirmAc = [UIAlertAction actionWithTitle:comfirm style:UIAlertActionStyleDefault handler:nil];
    [alertVC addAction:comfirmAc];
    [self presentViewController:alertVC animated:YES completion:nil];
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
