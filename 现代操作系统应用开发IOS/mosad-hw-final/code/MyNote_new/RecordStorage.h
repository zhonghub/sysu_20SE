//
//  RecordStorage.h
//  hw2
//
//  Created by sushan on 2022/9/22.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef RecordStorage_h
#define RecordStorage_h

#import <stdlib.h>
#import <UIKit/UIKit.h>
NS_ASSUME_NONNULL_BEGIN
// 记录Record类

@interface RecordStorage : NSObject
@property(nonatomic,strong) NSString * imageCachePath;// 图片cache路径
@property(nonatomic,strong) NSString * listCachePath;// 文本cache路径
@property(nonatomic) NSMutableArray * records;
@property(nonatomic) NSArray * itemList;
+ (RecordStorage *)getInstance;
-(void) initCache;
-(void) readFromCache;
-(void) storeWithList:(NSMutableArray *)list0 withDic:(NSDictionary *)dic0;
-(void) clearList;
-(void) removeItem0:(NSDictionary*)r1;
@end
NS_ASSUME_NONNULL_END

#endif /* RecordStorage_h */
