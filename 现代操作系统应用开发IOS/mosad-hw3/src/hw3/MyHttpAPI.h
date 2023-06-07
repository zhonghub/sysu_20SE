//
//  MyHttpAPI.h
//  hw3
//
//  Created by sushan on 2022/10/19.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef MyHttpAPI_h
#define MyHttpAPI_h
#import <UIKit/UIKit.h>

// 负责网络通信
@interface MyHttpAPI : NSObject<NSURLSessionDelegate>
@property(nonatomic) NSString *name;// 用户登陆信息
@property(nonatomic) NSString *password;
@property(nonatomic) NSString *code;
@property(nonatomic) NSString *uuid;// 验证码的uuid
@property(nonatomic) NSString *token;
@property(nonatomic) NSString *msg; // 登录按钮返回的验证信息
@property(nonatomic) NSNumber *responseCode;// 登录按钮返回的状态码：200OK
@property(nonatomic,strong) NSDictionary *dic;// 获取的个人信息保存在字典dic里
@property(nonatomic,strong) NSDictionary *dic2;// 获取的评论信息保存在字典dic2[@"data"]里
@property(nonatomic,strong) NSURLSessionConfiguration *defaultConfigObject;
@property(nonatomic,strong) NSURLSession *delegateFreeSession;
-(instancetype)init;
// 登录页面调用：将输入框的个人信息保存到MyAPI
-(void) setJsonWIthName:(NSString *)n andPassword:(NSString *)p andCode:(NSString *)c;
// GET,获取/刷新验证码图片
-(void)getVerify:(UIButton *)btn2;
// POST,登录获取token
-(void) login;
// GET,获取个人信息/评论图文
- (void)getWithUrl:(NSString*)urlStr toDic:(NSNumber*)dicNum;
@end

#endif /* MyHttpAPI_h */
