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
-(instancetype)initWithFrame:(CGRect)frame andInfo:(NSDictionary *) dic1{
    _dic = dic1;
    self.view = [[UIView alloc] initWithFrame:frame];
    _view1 = [[UIScrollView  alloc] initWithFrame:frame];
    _view1.backgroundColor = [UIColor whiteColor];
    // 由于有些屏幕尺寸不够大，设计一个滚动视图来放下所有要展示的信息
    _view1.contentSize = CGSizeMake(frame.size.width, frame.size.height*1.4);
    _view1.bounces = YES;
    //设置滚动条指示器的类型，默认是白边界上的黑色滚动条
    _view1.indicatorStyle = UIScrollViewIndicatorStyleDefault;
    [self.view addSubview:_view1];
    [self setInfoView];
    return self;
}

// 增加一个圆形头像
-(void)addImg:(UIView*)view2 with:(NSURL*)url{
    CGFloat w = _view1.bounds.size.width;
    CGFloat h = _view1.bounds.size.height*0.8; // 用于自动布局
    UIImageView *v1 = [[UIImageView alloc] initWithFrame:CGRectMake(0,0,h*0.24,h*0.24)];
    // 通过UIImage的imageWithData获取url图片
    v1.image = [UIImage imageWithData:[NSData dataWithContentsOfURL:url]];
    v1.center=CGPointMake(w/2,h*0.28);
    v1.backgroundColor = [UIColor clearColor];
    v1.layer.masksToBounds = YES;
    v1.layer.cornerRadius = h*0.12;
    v1.layer.borderColor=[UIColor grayColor].CGColor;
    v1.layer.borderWidth=2;
    [view2 addSubview:v1];
}

// 绘制个人信息页面：
-(void) setInfoView{
    // 用于自动布局
    CGFloat w = _view1.bounds.size.width;
    CGFloat h = _view1.bounds.size.height*0.8;
    [self addLabel:_view1 withText:@"个人信息"
         withFrame:CGRectMake(0.3*w,h*0.05,0.4*w,40) withFont:35.0 isLeft:NO];
    // 头像的url,如：http://172.18.178.57:3000/prod-api + /profile/avatar/2022/10/18/blob_20221018174824A030.jpeg
    NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@", @"http://172.18.178.57:3000/prod-api",_dic[@"data"][@"avatar"]]];
    // 通过url添加圆形头像
    [self addImg:_view1 with:url];
    // arr1为其他信息中要展示的键key
    NSArray * arr1 = [[NSArray alloc]initWithObjects:@"nickName",@"phonenumber",@"email",@"sex",@"userId",@"createTime",@"deptName",@"deptId",@"loginIp",@"remark",@"roleName",nil];
    // arr2为arr1对应的中文
    NSArray * arr2 = [[NSArray alloc]initWithObjects:@"用户昵称",@"手机号码",@"邮箱",@"性别",@"用户ID",@"创建日期",@"所属部门",@"部门ID",@"登陆IP",@"remark",@"所属角色",nil];
    // 其他信息
    int i = 0;
    for (id key in arr1) {
        id str1 = arr2[i];
        NSString * str2;
        if([key isEqualToString:@"deptName"]){
            str2 = _dic[@"data"][@"dept"][@"deptName"];
        }
        else if([key isEqualToString:@"createTime"]){
            id value = [_dic[@"data"] objectForKey:key];
            str2 =  [value substringToIndex:16];
        }
        else if([key isEqualToString:@"roleName"]){
            str2 = _dic[@"data"][@"roles"][0][@"roleName"];
        }
        else if([key isEqualToString:@"sex"]){
            id value = _dic[@"data"][key];
            if([value isEqualToString:@"0"]){
                str2 = @"男";
            }else{
                str2 = @"女";
            }
        }
        else{
            id value = [_dic[@"data"] objectForKey:key];
            str2 =  value;
        }
        NSString *str = [NSString stringWithFormat:@"%@ :  %@",str1, str2];
        [self addLabel:_view1 withText:str withFrame:CGRectMake(0.05*w+10,h*0.40+40+i*42,0.8*w-10,30) withFont:20.0 isLeft:YES];
        i++;
    }
}

// 通过：内容、框架、字号、居中添加一个label
-(void)addLabel:(UIView*)view withText:(NSString*)str withFrame:(CGRect)r1 withFont:(CGFloat)f1 isLeft:(BOOL)left{
    UILabel *label1 = [[UILabel alloc] initWithFrame:r1];
    label1.text = str;
    label1.font = [UIFont systemFontOfSize: f1];
    if(left == YES){
        label1.textAlignment = NSTextAlignmentLeft;
    }
    [view addSubview:label1];
}

@end
