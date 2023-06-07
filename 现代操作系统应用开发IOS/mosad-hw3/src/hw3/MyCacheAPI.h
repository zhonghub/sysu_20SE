//
//  MyCacheAPI.h
//  hw3
//
//  Created by sushan on 2022/10/27.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef MyCacheAPI_h
#define MyCacheAPI_h
#import <UIKit/UIKit.h>
@interface MyCacheAPI:NSObject
@property(nonatomic,strong) NSArray *list2;// 获取的评论信息保存在list2里
@property(nonatomic,strong) NSString * imageCachePath;// 图片cache路径
@property(nonatomic,strong) NSString * listCachePath;// 文本cache路径
- (instancetype) init;
- (UIImage *) getImgByUrl:(NSString*)urlStr;
- (void) saveListWithDic:(NSDictionary *)dic;
- (void) loadListFromCache;
- (void) loadAllImgToCache;
- (void) clearList;
@end

#endif /* MyCacheAPI_h */
