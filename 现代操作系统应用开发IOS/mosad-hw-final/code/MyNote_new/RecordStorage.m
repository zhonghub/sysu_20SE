//
//  RecordStorage.m
//  hw2
//
//  Created by sushan on 2022/9/22.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "RecordStorage.h"

@implementation RecordStorage
// 单例
+ (RecordStorage *)getInstance{
    static RecordStorage *instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        instance = [[self alloc] init];
    });
    return instance;
}

-init{
    // cache路径
    NSString *cacheDir =[NSSearchPathForDirectoriesInDomains(NSCachesDirectory, NSUserDomainMask,YES) lastObject];
    // 图片保存路径
    _imageCachePath = [cacheDir stringByAppendingPathComponent:@"imgCache"];
    // 评论保存路径
    _listCachePath = [cacheDir stringByAppendingPathComponent:@"listCache"];
    
    _itemList = [[NSArray alloc]initWithObjects:@"date",@"place",@"sights",@"exp",@"media0",@"media1",@"media2",@"media3",@"media4",nil];
    NSLog(@"RecordStorage init");
    [self readFromCache];
    return self;
}
// 在Cache中创建文件夹
-(void)initCache{
    BOOL isDir;
    if(![[NSFileManager defaultManager] fileExistsAtPath:self.listCachePath isDirectory:&isDir]){
        // 创建存放评论文本的目录
        [[NSFileManager defaultManager] createDirectoryAtPath:self.listCachePath withIntermediateDirectories:YES attributes:nil error:nil];
    }
    if(![[NSFileManager defaultManager] fileExistsAtPath:self.imageCachePath isDirectory:&isDir]){
        // 创建存放图片的目录
        [[NSFileManager defaultManager] createDirectoryAtPath:self.imageCachePath  withIntermediateDirectories:YES attributes:nil error:nil];
    }
}
// 从Cache中读取图文
-(void)readFromCache{
    [self initCache];
    self.records = [[NSMutableArray alloc] init];
    NSArray *file2 = [[[NSFileManager alloc] init] subpathsAtPath:_listCachePath];
    //NSLog(@"loadListFromeCache: %@",file2);
    for(int i = 0; i<file2.count; ++i){
        NSString *dictPath = [self.listCachePath stringByAppendingPathComponent:file2[i]];
        NSDictionary *dic = [[NSDictionary alloc]initWithContentsOfFile:dictPath];
        [_records addObject:dic];
    }
}
// 将笔记图文list0保存到Cache中，dic1用于判断是新增一条笔记，还是对原有笔记进行编辑
-(void)storeWithList:(NSMutableArray *)list0 withDic:(NSDictionary *)dic1{
    BOOL isDir;
    if(![[NSFileManager defaultManager] fileExistsAtPath:self.listCachePath isDirectory:&isDir]){
        // 创建存放评论文本的目录
        [[NSFileManager defaultManager] createDirectoryAtPath:self.listCachePath withIntermediateDirectories:YES attributes:nil error:nil];
    }
    NSDictionary * newRecord;
    NSDate * now = [NSDate date];
    NSString *nowStr = [[NSString stringWithFormat:@"%@",now] substringToIndex:19];
    NSString * nowName = [NSString stringWithFormat:@"%@%@",nowStr,@"_note"];
    NSString* dicName = [NSString stringWithFormat:@"%@%@",nowName,@".plist"];
    NSString* dictPath = [self.listCachePath stringByAppendingPathComponent:dicName];
    NSMutableDictionary *dic0 = [[NSMutableDictionary alloc] init];
    if(dic1!=nil){
        dictPath = dic1[@"dictPath"];
        nowName = dic1[@"nowName"];
        [self.records removeObject:dic1];
        NSLog(@"remove old dic");
    }
    //[[NSFileManager defaultManager] fileExistsAtPath:dictPath]
    if(true){
        [dic0 setValue:dictPath forKey:@"dictPath"];
        [dic0 setValue:nowName forKey:@"nowName"];
        for(int j = 0; j < list0.count;++j){
            if(j>=4){
                NSOperationQueue * queue=[[NSOperationQueue alloc]init];
                [queue addOperationWithBlock:^{
                    [self saveImg:list0[j] withName1:nowName withName2:self.itemList[j]];
                }];
                [dic0 setValue:self.itemList[j] forKey:self.itemList[j]];
            }else{
                [dic0 setValue:list0[j] forKey:self.itemList[j]];
            }
        }
        newRecord = [[NSDictionary alloc] initWithDictionary:dic0];
        NSOperationQueue * queue=[[NSOperationQueue alloc]init];
        [queue addOperationWithBlock:^{
            [newRecord writeToFile:dictPath atomically:YES];
        }];
        NSLog(@"store dicPath: %@",dictPath);
    }
    // 根据打卡时间插入，最新打卡在第一个位置
    [self.records insertObject:newRecord atIndex:0];
    NSLog(@"records.size = %ld",self.records.count);
}

// 清空数据源
- (void)clearList{
    _records = [[NSMutableArray alloc] init];
}

// 将图片保存到本地cache
- (void)saveImg:(UIImage*)img withName1:(NSString*)name1 withName2:(NSString*)name2{
    BOOL isDir;
    if(![[NSFileManager defaultManager] fileExistsAtPath:self.imageCachePath isDirectory:&isDir]){
        // 创建存放图片的目录
        [[NSFileManager defaultManager] createDirectoryAtPath:self.imageCachePath withIntermediateDirectories:YES attributes:nil error:nil];
    }
    NSString *imgName = [NSString stringWithFormat:@"%@_%@.jpg",name1,name2];
    // 图片路径
    NSString *imagePath = [_imageCachePath stringByAppendingPathComponent:imgName];
    [UIImageJPEGRepresentation(img, 1.0) writeToFile:imagePath atomically:YES];
    //NSLog(@"save a img:%@",imagePath);
}

// 将图片从本地cache删除
- (void)removeImgwithName1:(NSString*)name1 withName2:(NSString*)name2{
    NSString *imgName = [NSString stringWithFormat:@"%@_%@.jpg",name1,name2];
    NSString *imagePath = [_imageCachePath stringByAppendingPathComponent:imgName];
    [[NSFileManager defaultManager] removeItemAtPath:imagePath error:nil];
    //NSLog(@"remove a img %@",imagePath);
    NSLog(@"remove a img");
}
// 将笔记r1及其图片从Cache中删除
-(void)removeItem0:(NSDictionary*)r1{
    NSLog(@"remove %@",r1[@"dictPath"]);
    //if([[NSFileManager defaultManager] fileExistsAtPath:r1[@"dictPath"]]){
    if(r1!=nil){
        NSOperationQueue * queue=[[NSOperationQueue alloc]init];
        [queue addOperationWithBlock:^{
            NSLog(@"remove a note");
            //删除旧的
            NSString* dicName = [NSString stringWithFormat:@"%@%@",r1[@"nowName"],@".plist"];
            NSString *dictPath0 = [self.listCachePath stringByAppendingPathComponent:dicName];
            [[NSFileManager defaultManager] removeItemAtPath:dictPath0 error:nil];
            for(int j = 4; j < r1.count-2;++j){
                [self removeImgwithName1:r1[@"nowName"] withName2:self.itemList[j]];
            }
        }];
        [self.records removeObject:r1];
        NSLog(@"remove old dic");
    }
}
@end
