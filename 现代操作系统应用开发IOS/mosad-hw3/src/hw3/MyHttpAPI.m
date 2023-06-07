//
//  MyHttpAPI.m
//  hw3
//
//  Created by sushan on 2022/10/19.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "MyHttpAPI.h"

@implementation MyHttpAPI
-(instancetype)init{
    _defaultConfigObject = [NSURLSessionConfiguration defaultSessionConfiguration];
    _delegateFreeSession = [NSURLSession sessionWithConfiguration:_defaultConfigObject delegate: self delegateQueue: [NSOperationQueue mainQueue]];
    return self;
}
-(void) setJsonWIthName:(NSString *)n andPassword:(NSString *)p andCode:(NSString *)c{
    _name = n;
    _password = p;
    _code = c;
}

#pragma mark --GET
// http://172.18.178.57:3000/prod-api/captchaImage
// 获取验证码
- (void)getVerify:(UIButton *)btn2{
    NSLog(@"click btn2:获取/刷新验证码");
    NSURL *url = [NSURL URLWithString:[NSString stringWithFormat: @"http://172.18.178.57:3000/prod-api/captchaImage"]];
    NSURLRequest *request = [NSURLRequest requestWithURL:url];
    //生成任务
    NSURLSessionDataTask * dataTask = [_delegateFreeSession dataTaskWithRequest:request completionHandler:^(NSData *data, NSURLResponse *response, NSError *error){
        if(error == nil){
            NSString * jsonString = [[NSString alloc] initWithData: data encoding: NSUTF8StringEncoding];
            NSData *jsonData = [jsonString dataUsingEncoding:NSUTF8StringEncoding];
            error = nil;
            // 转字典
            NSDictionary *dic = [NSJSONSerialization JSONObjectWithData:jsonData options:NSJSONReadingAllowFragments error:&error];
            // 保存uuid 和 验证码图片
            self.uuid = dic[@"uuid"];
            NSLog(@"uuid = %@\n",self.uuid);
            UIImage * img = [self stringToUIImage:dic[@"img"]];
            [btn2 setImage:img forState:0];
            [btn2 adjustsImageWhenDisabled];
            
        }
    }];
    //创建的task是停止状态，需要我们去启动
    [dataTask resume];
}
// NSString与UIImage的相互转化
- (NSString *)imageToNSString:(UIImage *)image{
    NSData *imageData = UIImagePNGRepresentation(image);
    return [imageData base64EncodedStringWithOptions:NSDataBase64Encoding64CharacterLineLength];
}

- (UIImage *)stringToUIImage:(NSString *)string{
    NSData *data = [[NSData alloc]initWithBase64EncodedString:string
                                                      options:NSDataBase64DecodingIgnoreUnknownCharacters];
    return [UIImage imageWithData:data];
}
#pragma mark --POST
// http://172.18.178.57:3000/prod-api/login
-(void)login{
    NSURL * url = [NSURL URLWithString:@"http://172.18.178.57:3000/prod-api/login"];
    NSMutableURLRequest * urlRequest = [NSMutableURLRequest requestWithURL:url];
    [urlRequest setHTTPMethod:@"POST"];
    NSDictionary *headers = @{
       @"Content-Type" : @"application/json"
    };
    [urlRequest setAllHTTPHeaderFields:headers]; //重点是这一句！！
    NSDictionary *dic = @{@"username":_name, @"password":_password, @"code":_code, @"uuid":_uuid};
    NSError *error = nil;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:dic options:1 error:&error];
    NSString *jsonString = [[NSString alloc] initWithData:jsonData encoding:NSUTF8StringEncoding];
    urlRequest.HTTPBody = [[NSData alloc] initWithData:[jsonString dataUsingEncoding:NSUTF8StringEncoding]];
    NSURLSessionDataTask * dataTask =[_delegateFreeSession dataTaskWithRequest:urlRequest completionHandler:^(NSData *data, NSURLResponse *response, NSError *error) {
        //NSLog(@"Response:%@\n error:%@\n", response, error);
        if(error == nil) {
            //NSString * text = [[NSString alloc] initWithData: data encoding: NSUTF8StringEncoding];
            NSDictionary *dict = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
            self.token = dict[@"token"];
            self.msg = dict[@"msg"];
            self.responseCode = dict[@"code"];
            NSLog(@"token= %@",self.token);
            NSLog(@"code = %@\n",dict[@"code"]);
        }
    }];
    [dataTask resume];
}

#pragma mark --GET2
// 获取个人信息,@"http://172.18.178.57:3000/prod-api/system/user/profile@" , 1
// 获取评论图文 @"http://172.18.178.57:3000/prod-api/yuan/comment/list" , 2
- (void)getWithUrl:(NSString*)urlStr toDic:(NSNumber*)dicNum{
    NSURL *url = [NSURL URLWithString:urlStr];
    // 在获取评论图文时需要使用信号量进行同步
    dispatch_semaphore_t sema = dispatch_semaphore_create(0);
    if(dicNum.intValue == 1){
        dispatch_semaphore_signal(sema);
    }
    NSMutableURLRequest *request = [NSMutableURLRequest requestWithURL:url cachePolicy:NSURLRequestReturnCacheDataElseLoad timeoutInterval:5.0];
    NSDictionary *headers = @{
        @"Authorization" : _token
    };
    [request setAllHTTPHeaderFields:headers];
    //生成任务
    NSURLSessionDataTask * dataTask = [self.delegateFreeSession dataTaskWithRequest:request completionHandler:^(NSData *data, NSURLResponse *response, NSError *error){
    if(error == nil){
        error = nil;
        // 转字典
        NSDictionary *dic = [NSJSONSerialization JSONObjectWithData:data options:NSJSONReadingAllowFragments error:&error];
        if(dicNum.intValue == 1){
            self.dic = dic;
        }else{
            self.dic2 = dic;
            NSLog(@"dic2 is loaded by url,count= %ld",[self.dic2[@"data"] count]);
        }
    }
    dispatch_semaphore_signal(sema);
    }];
    //创建的task是停止状态，需要我们去启动
    [dataTask resume];
    dispatch_semaphore_wait(sema, DISPATCH_TIME_FOREVER);
}

@end
