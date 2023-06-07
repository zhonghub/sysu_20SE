//
//  ViewController.m
//  hw1
//
//  Created by sushan on 2022/9/6.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import "ViewController.h"
#import "Hero.h"
#import "HeroesFactory.h"


@interface ViewController ()
- (void)pk:(Hero*)h1
       and:(Hero*)h2
    rounds:(int)m;
@end

@implementation ViewController
// 英雄h1和h2进行m个回合的pk，在这里体现了多态性，实现接口重用
- (void)pk:(Hero*)h1
       and:(Hero*)h2
    rounds:(int)m
{
    for(int i = 0 ; i < m  ; ++i){
        NSLog(@"round %d", i+1);
        // 两个英雄分别使用技能
        [h1 skills:i];
        [h2 skills:i];
        // 两个英雄分别受伤
        [h1 getHurt: h2.attack];
        [h2 getHurt: h1.attack];
        // 这回合结束两英雄的状态
        [h1 getNowState];
        [h2 getNowState];
        // 这回合的结果, 本回合结束后血量多者获胜
        if(h1.blood_value > h2.blood_value)
            NSLog(@"%@ wins the round!\n", h1.name);
        else if(h1.blood_value < h2.blood_value)
            NSLog(@"%@ wins the round!\n",h2.name);
        else
            NSLog(@"The round is a draw!\n");
        NSLog(@"");
    }
    // 游戏结束，输出本次比赛的结果，所有回合结束后血量多者取得最终胜利（即最后一次回合的结果）
    if(h1.blood_value > h2.blood_value)
        NSLog(@"%@ finally won!\n", h1.name);
    else if(h1.blood_value < h2.blood_value)
        NSLog(@"%@ finally won!\n", h2.name);
    else
        NSLog(@"The two ended up in a draw!\n");
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    
    CGRect labelRect = CGRectMake(10, 20, 90, 20); // (origin.x, origin.y, size.width , size.height)
    UILabel *label = [[UILabel alloc] initWithFrame:labelRect];
    label.text = @"123456789";
    [self.view addSubview:label];
    
    CGFloat y0 = 40;// +=20
    labelRect.origin.y = y0;
    labelRect.size.width = 150;
    label = [[UILabel alloc] initWithFrame:labelRect];
    label.text = @"Hello! Game starts!";
    [self.view addSubview:label];
    
    NSLog(@"Hello! Game starts!");
    NSLog(@"");
    // Hero * hero = [[子类 alloc] init];
    // 共10个英雄的子类
    // Lvbu Liubei Zhangfei Zhaoyun Zhouyu Sunce Zhangliao Machao Huaxiong Guanyu
    // 初始化两个英雄子类的对象，都使用父类指针来指向，子类对象通过工厂模式生成
    Hero * h2 = [HeroesFactory getHeroWithName:@"Zhaoyun"];
    Hero * h1 = [HeroesFactory getHeroWithName:@"Huaxiong"];
    // 设置英雄所属国家
    NSString *c1 = @"Wei";
    NSString *c2 = @"Shu";
    // 根据类实际的类型名得到英雄的名字
    NSString *n1 = NSStringFromClass([h1 class]);
    NSString *n2 = NSStringFromClass([h2 class]);
    // 初始血量
    NSInteger b1 = 150;
    // 初始能量
    NSInteger e1 = 0;
    // 初始化：国家，名字，初识血量，初始能量
    [h1 initWithC:c1 andN:n1 andB:b1 andE:e1];
    [h2 initWithC:c2 andN:n2 andB:b1 andE:e1];
    NSLog(@"");
    // PK 8个回合, 多态性，对任意两个子类的对象，都使用父类指针来指向，以实现接口重用
    [self pk:h1 and:h2 rounds:10];
    
    NSLog(@"Bye! Game ends!\n");
}


@end
