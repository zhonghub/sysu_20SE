//
//  HeroesFactory.h
//  hw1
// 共10个英雄的子类
// Lvbu Liubei Zhangfei Zhaoyun Zhouyu Sunce Zhangliao Machao Huaxiong Guanyu

#ifndef HeroesFactory_h
#define HeroesFactory_h

#import "Hero.h"

// 英雄工厂，使用工厂模式产生英雄子类的实例
@interface HeroesFactory : NSObject{
}
// 根据对应的类名产生对应的英雄子类实例, +号表示静态方法（类方法），-号表示实例方法
+ (Hero*)getHeroWithName: (NSString*) className;

@end

// 以下为Hero的一些子类

@interface Lvbu : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Liubei : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Zhangfei : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Zhaoyun : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Zhouyu : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Sunce : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Zhangliao : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Machao : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Huaxiong : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end

@interface Guanyu : Hero {
// 子类，继承基类Hero，只重写使用技能的方法(void)skills:(int)round
}
@end



#endif /* HeroesFactory_h */
