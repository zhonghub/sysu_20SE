## Xcode入门

###  开发环境

* Mac OS
* Objective-C
* Xcode

### 前言

本文主要讲述构建第一个Xcode项目，不使用storyboard和xlib进行布局（实践中很少使用）。

* storyboard：一旦Xcode打开，该文件就会发生改变，在团队开发时会引起很多冲突，维护成本太高。
* xlib：不利于多人协作。

### 多态

多态（Polymorphism），在面向对象语言中指的是同一个接口可以有多种不同的实现方式，OC中的多态则是不同对象对同一消息的不同响应方式，子类通过重写父类的方法来改变同一消息的实现，体现多态性。另外我们知道C++中的多态主要是通过virtual关键字(虚函数、抽象类等)来实现，具体来说指的是允许父类的指针指向子类对象，成为一个更泛化、容纳度更高的父类对象，这样父对象就可以根据实际是哪种子类对象来调用父类同一个接口的不同子类实现。

### 创建项目

1、打开Xcode，点击Create a new Xcode project，选择模版（每个模版都提供了一套程序，作用是简化开发，这里选最简单的 Single View Application模版。

![p1](img/p1.png)

2、填写模版选项

![p2](img/p2.png)

3、选择项目存放位置（是否勾选创建Git repository，默认即可，是一个版本控制器，适合多人协作开发）

4、删除Main.storyboard，并且清除info.plist配置文件中的入口

![p4](img/p4.png)

5、接下来找到`AppDelegate.m`文件，`UIApplication`为App的根对象，每个App对应一个`UIApplication`，实现了`UIApplicationDelegate`的对象为开发者提供控制app生命周期内的接口。这里我们找到app启动之后的入口函数，在这里我们初始化UIWindow（这里先不做介绍，后续有兴趣可深入了解，悬浮球可以用UIWindow实现），UIWindow为视图的容器，我们将其设置为屏幕大小。我们引入了ViewController，初始化了一个视图控制器，并且将其设置为window的根视图控制器。最后将window设置为key window并且可视化。

![p5](img/p5.png)

6、找到viewcontroller，该类继承自UIViewController（有固定的生命周期），这里我们在viewDidLoad函数中（生命周期函数）中输出“Hello World”。运行程序启动模拟器之后，可以在控制台中可以观察到输出。

```objc
//
//  ViewController.m
//  HelloWorld
//
//  Created by CookiesChen on 2019/8/26.
//  Copyright © 2019 CookiesChen. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()

@end

@implementation ViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    NSLog(@"Hello World");
}


@end

```

![p6](img/p6.png)

### 实验

现在有一个英雄基类Hero，其下有若干个三国英雄子类，父类有一个统一接口：getCountry，子类各自有自己的接口实现，返回各自对应的国家。这里给出.h的参考实现，具体的.m文件自行补充。

```objective-c
//
//  Hero.h
//  HeroPK
//  Copyright © 2019 TMachine. All rights reserved.
//

#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface Hero : NSObject {
    NSString country;   
    NSInteger blood_value;
    NSInteger energy_value;
}

- (void)PKOneUnit;
- (NSInteger)getBlood_value;
- (NSInteger)getenergy_value;
- (NSString *)getCountry;

@end

@interface Zhangfei : Hero {
    
}

@end

@interface Lvbu :Hero {
    
}

@end



NS_ASSUME_NONNULL_END

```