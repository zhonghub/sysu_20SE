//
//  HeroesFactory.m
//  hw1
//
// 共10个英雄的子类
// Lvbu Liubei Zhangfei Zhaoyun Zhouyu Sunce Zhangliao Machao Huaxiong Guanyu

#import <Foundation/Foundation.h>
#import "HeroesFactory.h"

@implementation HeroesFactory
+ (Hero *) getHeroWithName: (NSString *) className{
    NSLog(@"create a Hero %@\n",className);
    Class myClass = NSClassFromString(className);
    id myObject = [[myClass alloc] init];
    // NSLog(@"%@", NSStringFromClass(myClass));
    if ([myClass isSubclassOfClass:[Hero class]]) {
    // ChildClass是ParentClass的子类
        return myObject;
    } else {
    // ChildClass不是ParentClass的子类
        return [[Hero alloc] init];
    }
}
@end


@implementation Lvbu
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 30){
        attack0 = 45;
        blood0 = 15;
        energe0 = -30;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 10;
                blood0 = 10;
                energe0 = 10;
                skill0 = 1;
                break;
            case 1:
                attack0 = 25;
                blood0 = 5;
                energe0 = 0;
                skill0 = 2;
                break;
            case 2:
                attack0 = 3;
                blood0 = 10;
                energe0 = 17;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end


@implementation Liubei
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 35){
        attack0 = 45;
        blood0 = 20;
        energe0 = -35;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 20;
                blood0 = 0;
                energe0 = 10;
                skill0 = 1;
                break;
            case 1:
                attack0 = 5;
                blood0 = 15;
                energe0 = 10;
                skill0 = 2;
                break;
            case 2:
                attack0 = 6;
                blood0 = 7;
                energe0 = 17;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end


@implementation Zhangfei
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 20){
        attack0 = 10;
        blood0 = 40;
        energe0 = -20;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 10;
                blood0 = 15;
                energe0 = 5;
                skill0 = 1;
                break;
            case 1:
                attack0 = 15;
                blood0 = 5;
                energe0 = 10;
                skill0 = 2;
                break;
            case 2:
                attack0 = 8;
                blood0 = 7;
                energe0 = 15;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end


@implementation Zhaoyun
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 40){
        attack0 = 15;
        blood0 = 55;
        energe0 = -40;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 15;
                blood0 = 5;
                energe0 = 10;
                skill0 = 1;
                break;
            case 1:
                attack0 = 25;
                blood0 = 0;
                energe0 = 5;
                skill0 = 2;
                break;
            case 2:
                attack0 = 13;
                blood0 = 7;
                energe0 = 10;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end


@implementation Zhouyu
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 50){
        attack0 = 40;
        blood0 = 40;
        energe0 = -50;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 10;
                blood0 = 0;
                energe0 = 20;
                skill0 = 1;
                break;
            case 1:
                attack0 = 20;
                blood0 = 0;
                energe0 = 10;
                skill0 = 2;
                break;
            case 2:
                attack0 = 13;
                blood0 = 8;
                energe0 = 9;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end


@implementation Sunce
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 35){
        attack0 = 30;
        blood0 = 30;
        energe0 = -35;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 6;
                blood0 = 14;
                energe0 = 10;
                skill0 = 1;
                break;
            case 1:
                attack0 = 5;
                blood0 = 20;
                energe0 = 5;
                skill0 = 2;
                break;
            case 2:
                attack0 = 4;
                blood0 = 9;
                energe0 = 17;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end


@implementation Zhangliao
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 25){
        attack0 = 45;
        blood0 = 10;
        energe0 = -25;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 6;
                blood0 = 8;
                energe0 = 16;
                skill0 = 1;
                break;
            case 1:
                attack0 = 13;
                blood0 = 9;
                energe0 = 8;
                skill0 = 2;
                break;
            case 2:
                attack0 = 3;
                blood0 = 18;
                energe0 = 9;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end

@implementation Machao
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 40){
        attack0 = 30;
        blood0 = 40;
        energe0 = -40;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 10;
                blood0 = 15;
                energe0 = 5;
                skill0 = 1;
                break;
            case 1:
                attack0 = 5;
                blood0 = 10;
                energe0 = 15;
                skill0 = 2;
                break;
            case 2:
                attack0 = 8;
                blood0 = 3;
                energe0 = 19;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end

@implementation Huaxiong
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 25){
        attack0 = 20;
        blood0 = 35;
        energe0 = -25;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 4;
                blood0 = 16;
                energe0 = 10;
                skill0 = 1;
                break;
            case 1:
                attack0 = 11;
                blood0 = 12;
                energe0 = 7;
                skill0 = 2;
                break;
            case 2:
                attack0 = 3;
                blood0 = 11;
                energe0 = 16;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end

@implementation Guanyu
- (void)skills:(int)round{
    NSInteger attack0 = 0;
    NSInteger blood0 = 0;
    NSInteger energe0 = 0;
    int skill0 = 0;
    if(self.energy_value >= 30){
        attack0 = 36;
        blood0 = 24;
        energe0 = -30;
        skill0 = 4;
    }
    else{
        switch (round % 3) {
            case 0:
                attack0 = 10;
                blood0 = 8;
                energe0 = 12;
                skill0 = 1;
                break;
            case 1:
                attack0 = 9;
                blood0 = 8;
                energe0 = 13;
                skill0 = 2;
                break;
            case 2:
                attack0 = 14;
                blood0 = 9;
                energe0 = 7;
                skill0 = 3;
                break;
            default:
                break;
        }
    }
    // 英雄使用技能后状态发生改变
    [self changeStateWithAttack:attack0 andB:blood0 andE:energe0];
    NSLog(@"%@\t used skill %d:\t attack = %ld,\t blood_value+= %ld,\t energy_value+= %ld",
          self.name, skill0, attack0, blood0, energe0);
}
@end
