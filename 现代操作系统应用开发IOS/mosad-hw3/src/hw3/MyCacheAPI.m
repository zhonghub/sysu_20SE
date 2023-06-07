//
//  MyCacheAPI.m
//  hw3
//
//  Created by sushan on 2022/10/27.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "MyCacheAPI.h"

@implementation MyCacheAPI
-(instancetype)init{
    // cache路径
    NSString *cacheDir =[NSSearchPathForDirectoriesInDomains(NSCachesDirectory, NSUserDomainMask,YES) lastObject];
    // 图片保存路径
    _imageCachePath = [cacheDir stringByAppendingPathComponent:@"imgCache"];
    // 评论保存路径
    _listCachePath = [cacheDir stringByAppendingPathComponent:@"listCache"];
    return self;
}

#pragma mark --CacheList
// 如果本地cache不存在文本缓存，则将GET请求得到的评论文本dic[@"data"]保存到本地cache
- (void)saveListWithDic:(NSDictionary *)dic{
    BOOL isDir;
    if([[NSFileManager defaultManager] fileExistsAtPath:self.listCachePath isDirectory:&isDir]){
       return;
    }else{
        // 创建存放评论文本的目录
        [[NSFileManager defaultManager] createDirectoryAtPath:self.listCachePath withIntermediateDirectories:YES attributes:nil error:nil];
    }
    _list2 = dic[@"data"];
    NSArray * arr1 = [[NSArray alloc]initWithObjects:@"createBy",@"createTime",@"commentId",@"content",@"media0",@"media1",@"media2",@"media3",@"media4",@"media5",@"media6",@"media7",@"media8",@"media9",nil];
    for(int i = 0; i < _list2.count; ++i){
        NSOperationQueue * queue=[[NSOperationQueue alloc]init];
        NSBlockOperation *op1 = [NSBlockOperation blockOperationWithBlock:^{
            NSString* dicName = [NSString stringWithFormat:@"%@%@%@",@"commentId",self.list2[i][@"commentId"],@".plist"];
            NSString *dictPath = [self.listCachePath stringByAppendingPathComponent:dicName];
            if(![[NSFileManager defaultManager] fileExistsAtPath:dictPath]){
                NSMutableDictionary *dic0 = [[NSMutableDictionary alloc] init];
                for(int j = 0; j < arr1.count;++j){
                    [dic0 setValue:self.list2[i][arr1[j]] forKey:arr1[j]];
                }
                NSDictionary * dic_i = [[NSDictionary alloc] initWithDictionary:dic0];
                [dic_i writeToFile:dictPath atomically:YES];
                //NSLog(@"%@=%@",dicName,dic_i);
            }
        }];
        [queue addOperation:op1];
    }
}
// 从cache加载评论文本到list2
- (void) loadListFromCache{
    NSArray *file2 = [[[NSFileManager alloc] init] subpathsAtPath:_listCachePath];
    NSLog(@"loadListFromeCache: %@",file2);
    NSMutableArray *loadList = [[NSMutableArray alloc] init];
    for(int i = 0; i<file2.count; ++i){
        NSString *dictPath = [self.listCachePath stringByAppendingPathComponent:file2[i]];
        NSDictionary *dic = [[NSDictionary alloc]initWithContentsOfFile:dictPath];
        [loadList addObject:dic];
    }
    _list2 = [[NSArray alloc] initWithArray:loadList];
}
// 清空数据源
- (void)clearList{
    _list2 = nil;
}

#pragma mark --CacheImg
// 获取url中的图片名称(含格式)
-(NSString*) getNameFromUrl:(NSString*)urlStr{
    NSRange range = [urlStr rangeOfString:@"/" options:NSBackwardsSearch];
    NSString * imgName = [urlStr substringFromIndex:range.location+1];
    return imgName;
}

// 从网络加载图片并保存在本地
-(UIImage *) getImgAndSave:(NSString*)urlStr{
    NSLog(@"网络加载");
    //cache中存放图片的目录不存在则创建目录
    BOOL isDir;
    if(![[NSFileManager defaultManager] fileExistsAtPath:self.imageCachePath isDirectory:&isDir]){
        // 创建存放图片的目录
        [[NSFileManager defaultManager] createDirectoryAtPath:self.imageCachePath withIntermediateDirectories:YES attributes:nil error:nil];
    }
    NSString *imgName = [self getNameFromUrl:urlStr];
    // 图片路径
    NSString *imagePath = [_imageCachePath stringByAppendingPathComponent:imgName];
    NSURL *url = [NSURL URLWithString:[NSString stringWithFormat:@"%@%@", @"http://172.18.178.57:3000/prod-api",urlStr]];
    // 用url从网络加载
    UIImage * img = [UIImage imageWithData:[NSData dataWithContentsOfURL:url]];
    NSString* extension = [imgName substringFromIndex:imgName.length-3];
    // 保存在cache里
    if ([[extension lowercaseString] isEqualToString:@"png"]) {
        //NSLog(@"%@",extension);
        [UIImagePNGRepresentation(img) writeToFile:imagePath atomically:YES];
    }else if ([[extension lowercaseString] isEqualToString:@"jpg"] || [[extension lowercaseString] isEqualToString:@"peg"]){
        // 只取最后3位，所以jpeg->peg
        //NSLog(@"%@",extension) ;
        [UIImageJPEGRepresentation(img, 1.0) writeToFile:imagePath atomically:YES];
    } else {
        NSLog(@"文件后缀不认识");
    }
    return img;
}
// 获取图片：本地不存在，从网络加载，并保存到cache；否则从cache加载
-(UIImage *) getImgByUrl:(NSString*)urlStr{
    // 在这里实现从网络读取并保存到本地，还是从cache读取
    NSString *imgName = [self getNameFromUrl:urlStr];
    NSString *imagePath = [_imageCachePath stringByAppendingPathComponent:imgName];
    if(![[NSFileManager defaultManager] fileExistsAtPath:imagePath]){
        // 从网络加载并保存在cache
        UIImage * img = [self getImgAndSave:urlStr];
        return img;
    }else{
        NSLog(@"本地加载");
        // 从cache里加载
        UIImage *getImage = [UIImage imageWithContentsOfFile:imagePath];
        return getImage;
    }
}
// 上面函数的无返回版本：本地不存在加载到cache，否则返回
-(void) loadImgByUrl:(NSString*)urlStr{
    NSString *imgName = [self getNameFromUrl:urlStr];
    NSString *imagePath = [_imageCachePath stringByAppendingPathComponent:imgName];
    if(![[NSFileManager defaultManager] fileExistsAtPath:imagePath]){
        // 从网络加载并保存在cache
        [self getImgAndSave:urlStr];
    }else{
        NSLog(@"已加载到本地cache");
        return;
    }
}
// 将所有图片保存在本地cache
-(void) loadAllImgToCache{
    for(int i = 0; i < _list2.count; ++i){
        for(int j = 1; j <=9; ++j){
            NSString * imgName = [NSString stringWithFormat:@"%@%@",@"media",[NSNumber numberWithInt:j]];
            if([_list2[i][imgName] isEqualToString:@""]){
                continue;
            }
            // 使用NSOperationQueue异步加载
            NSOperationQueue * queue=[[NSOperationQueue alloc]init];
            [queue addOperationWithBlock:^{
                NSString * path =self.list2[i][imgName];
                [self loadImgByUrl:path]; // 加载到cache
            }];
        }
    }
}
@end
