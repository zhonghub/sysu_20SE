//
//  RecordStorage.m
//  hw2
//
//  Created by sushan on 2022/9/22.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "RecordStorage.h"

@implementation Record
//[NSMutableArray array]
@end


@implementation RecordStorage
-init{
    self.records = [[NSMutableArray alloc] init];
    NSLog(@"RecordStorage init");
    return self;
}
- (void)storeWithData:(NSString *)Data
             andPlace:(NSString *)Place
            andSights:(NSString *)Sights
               andExp:(NSString *)Exp
              andImgs:(NSMutableArray<UIImage *> *)Imgs{
    Record *newRecord = [[Record alloc] init];
    newRecord.date = Data;
    newRecord.place = Place;
    newRecord.sights = Sights;
    newRecord.experience = Exp;
    newRecord.imgs = Imgs;
    // 根据打卡时间插入，最新打卡在第一个位置
    [self.records insertObject:newRecord atIndex:0];
}
@end
