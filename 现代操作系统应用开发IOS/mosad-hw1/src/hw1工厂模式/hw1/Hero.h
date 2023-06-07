//
//  Hero.h
//  hw1
//
//  Created by sushan on 2022/9/6.
//  Copyright © 2022 SYSU. All rights reserved.
//

#ifndef Hero_h
#define Hero_h

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

// 英雄的父类
@interface Hero : NSObject{
}
// 国家，名字，血量，能量，攻击力
@property(nonatomic) NSString *country;
@property(nonatomic) NSString *name;
@property(nonatomic) NSInteger blood_value;
@property(nonatomic) NSInteger energy_value;
@property(nonatomic) NSInteger attack;
// 初始化：国家，名字，血量，能量
- (void)initWithC: (NSString*) s1 andN: (NSString*) s2 andB: (NSInteger) s3 andE: (NSInteger) s4;
// 输出该回合结束的英雄的状态：血量，能量
- (void)getNowState;
// 英雄在回合round使用技能，由子类进行重写
- (void)skills:(int)round;
// 英雄使用技能后，状态（攻击力，血量，能量）发生改变
- (void)changeStateWithAttack:(NSInteger) a andB:(NSInteger) b andE:(NSInteger) e;
// 英雄受伤：血量blood_value -= 敌方英雄本回合的攻击力attack
- (void)getHurt:(NSInteger) attacks;

@end



NS_ASSUME_NONNULL_END


#endif /* Hero_h */
