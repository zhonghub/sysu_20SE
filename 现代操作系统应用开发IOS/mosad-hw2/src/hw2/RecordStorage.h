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

@interface Record : NSObject
@property(nonatomic, copy)NSString *date;
@property(nonatomic, copy)NSString *place;
@property(nonatomic, copy)NSString *sights;
@property(nonatomic, copy)NSString *experience;
@property(nonatomic, retain) NSMutableArray<UIImage *> * imgs;
@end


@interface RecordStorage : NSObject
@property (nonatomic) NSMutableArray<Record *> * records;
- (void)storeWithData:(NSString *)Data
             andPlace:(NSString *)Place
            andSights:(NSString *)Sights
               andExp:(NSString *)Exp
              andImgs:(NSMutableArray<UIImage *> *)Imgs;
@end
NS_ASSUME_NONNULL_END

#endif /* RecordStorage_h */
