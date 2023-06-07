//
//  GraphicListController.h
//  hw3
//
//  Created by sushan on 2022/10/13.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef GraphicListController_h
#define GraphicListController_h
#import <UIKit/UIKit.h>
#import "MyCacheAPI.h"

@interface GraphicListController : UIViewController<UICollectionViewDataSource,UICollectionViewDelegate,UICollectionViewDelegateFlowLayout>
@property(nonatomic,strong) MyCacheAPI *myCache;// 数据源，获取的评论信息保存在myCache.list2里
@property(nonatomic,strong) UICollectionView * table;//  图文列表
- (instancetype) initWithFrame:(CGRect)frame;
@end

#endif /* GraphicListController_h */
