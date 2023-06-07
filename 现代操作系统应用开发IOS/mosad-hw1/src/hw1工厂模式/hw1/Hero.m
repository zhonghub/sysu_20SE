//
//  Hero.m
//  hw1
//
//  Created by sushan on 2022/9/6.
//  Copyright © 2022 SYSU. All rights reserved.
//

// #import <Foundation/Foundation.h>
#import "Hero.h"


@implementation Hero

- (void)initWithC: (NSString*) s1 andN: (NSString*) s2 andB: (NSInteger) s3 andE: (NSInteger) s4
{
    _country = s1;
    _name = s2;
    _blood_value = s3;
    _energy_value  = s4;
    _attack = 0;
    NSLog(@"%@ 's\t country is %@,\t blood_value is %ld,\t energy_value is %ld",_name, _country, _blood_value, _energy_value);
    
}

- (void)skills:(int)round{
    NSLog(@"This is father class Hero!");
}

- (void)changeStateWithAttack:(NSInteger) a andB:(NSInteger) b andE:(NSInteger) e{
    _attack = a;
    _blood_value += b;
    _energy_value += e;
}

- (void)getHurt:(NSInteger) attacks{
    NSLog(@"%@\t get hurt: blood_value-= %ld",_name, attacks);
    _blood_value -= attacks;
}

- (void)getNowState{
    NSLog(@"%@\t's blood_value is %ld,\t energy_value is %ld",_name, _blood_value, _energy_value);
}

@end

