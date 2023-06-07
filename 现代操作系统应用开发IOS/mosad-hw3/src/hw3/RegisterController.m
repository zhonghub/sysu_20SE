//
//  RegisterController.m
//  hw3
//
//  Created by sushan on 2022/10/13.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "RegisterController.h"

@implementation RegisterController
- (void)viewDidLoad {
    [super viewDidLoad];
}

-(instancetype)init{
    // myAPI负责网络通信
    _myAPI = [[MyHttpAPI alloc] init];
    // 设置登录界面
    [self setRegister];
    // 登录后的页面为一个标签栏页面:个人信息，评论区.先初始化备用
    [self setGraphUI];
    _tab = [[UITabBarController alloc] init];
    return self;
}

#pragma mark --RegisterController
-(void)setRegister{
    self.view = [[UIView alloc] initWithFrame:CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height)];
    self.view.backgroundColor = [UIColor greenColor];
    CGFloat h = self.view.bounds.size.height*0.8;
    CGFloat w = self.view.bounds.size.width;
    _view1=[[UIView alloc]initWithFrame:self.view.bounds];
    _view1.backgroundColor = [UIColor whiteColor];
    // 3个输入框
    _inputName = [self getTextField:CGRectMake(100, 0.4*h, w-150, 50) andName:@"用户名：" andPlaceHolder:@"name" andSecure:NO];
    _inputPassword = [self getTextField:CGRectMake(100, 0.4*h+70, w-150, 50) andName:@"密   码：" andPlaceHolder:@"password" andSecure:YES];
    _inputVerify = [self getTextField:CGRectMake(100, 0.4*h+140, 0.3*w, 50) andName:@"验证码：" andPlaceHolder:@"验证码" andSecure:NO];
    // 两个按钮：圆形登录按钮，验证码图片按钮
    [self setBtn:_view1 Withx:w*0.5 Withy:0.4*h+220+0.15*w WithSize:w*0.3];
    [self setBtn:_view1 WithSize:CGRectMake(100+0.3*w,0.4*h+140,0.7*w-150,50)];
    [self.view addSubview:_view1];
    UILabel *label = [[UILabel alloc] initWithFrame:CGRectMake(w*0.1, h*0.1, w*0.8, h*0.3)];
    [label setText:@"登录页面"];//text是输入的结果
    [label setTextAlignment:NSTextAlignmentCenter];
    label.font = [UIFont systemFontOfSize: w*0.12];
    [_view1 addSubview:label];
}
// 得到单行输入框
-(UITextField *)getTextField:(CGRect)f andName:(NSString *)s1 andPlaceHolder:(NSString *)s2 andSecure:(BOOL)secure{
    UILabel *label = [[UILabel alloc] initWithFrame:CGRectMake(f.origin.x-80, f.origin.y, 80, f.size.height)];
    UITextField *text = [[UITextField alloc] initWithFrame:f];
    text.autocapitalizationType = UITextAutocapitalizationTypeNone;// 不自动大写
    [label setText:s1];//text是输入的结果
    [text setPlaceholder:s2];
    text.layer.borderWidth = 3;
    text.layer.borderColor = [UIColor grayColor].CGColor;
    text.layer.masksToBounds = YES;// 边框圆角
    text.layer.cornerRadius = 5;
    text.clearButtonMode = UITextFieldViewModeWhileEditing;// 清除按钮,编辑时出现
    //设置为YES时文本会自动缩小以适应文本窗口大小.默认是保持原来大小,而让长文本滚动
    text.adjustsFontSizeToFitWidth = YES;
    //设置左边视图的宽度,用于设置文字的左边距
    text.leftView = [[UIView alloc]initWithFrame:CGRectMake(0, 0, 8, 0)];
    //设置显示模式为永远显示(默认不显示 必须设置 否则没有效果)
    text.leftViewMode = UITextFieldViewModeAlways;
    if(secure){
        text.secureTextEntry = YES; // 密码
    }
    [_view1 addSubview:label];
    [_view1 addSubview:text];
    return text;
}

//点击空白处键盘隐藏
-(void)touchesBegan:(NSSet *)touches withEvent:(UIEvent *)event{
    [_inputName resignFirstResponder];
    [_inputPassword resignFirstResponder];
    [_inputVerify resignFirstResponder];
}
#pragma mark --VerifyCodeBtn
// 验证码图片按钮（点击刷新）
-(void)setBtn:(UIView *)view WithSize:(CGRect)size{
    UIButton* btn2 = [[UIButton alloc] initWithFrame:size];
    [btn2 addTarget:self action:@selector(getVerify) forControlEvents:UIControlEventTouchUpInside];
    btn2.layer.borderColor=[UIColor grayColor].CGColor;
    btn2.layer.borderWidth=1;
    btn2.backgroundColor = [UIColor clearColor];
    [btn2 setTitle: @"验证码" forState: UIControlStateNormal];
    [btn2 setTitleColor:[UIColor blackColor]forState:UIControlStateNormal];
    [view addSubview:btn2];
    _btn2 = btn2;
    [self getVerify];//初始：获取验证码
}

// 获取验证码
- (void)getVerify{
    _inputVerify.text = @"";
    [_myAPI getVerify:_btn2];
}

#pragma mark --RegisterBtn
// 圆形登录按钮
-(void)setBtn:(UIView *)view Withx:(CGFloat)x Withy:(CGFloat)y WithSize:(CGFloat)size{
    UIButton * btn = [[UIButton alloc] initWithFrame:CGRectMake(0, 0, size, size)];
    [btn addTarget:self action:@selector(logIn) forControlEvents:UIControlEventTouchUpInside];
    btn.center=CGPointMake(x, y);
    btn.layer.borderColor=[UIColor blackColor].CGColor;
    btn.layer.borderWidth=2;
    btn.layer.cornerRadius = btn.bounds.size.width / 2.0; // 圆形按钮
    [btn setTitle: @"登录" forState: UIControlStateNormal];
    btn.titleLabel.font = [UIFont systemFontOfSize: size/4.0];
    btn.backgroundColor = [UIColor clearColor];
    [btn setTitleColor:[UIColor blackColor]forState:UIControlStateNormal];
    [view addSubview:btn];
}
// 登录按钮绑定事件
-(void)logIn{
    NSLog(@"%@",[NSString stringWithFormat:@"%@ %@ %@ %@",@"click btn1:",_inputName.text,_inputPassword.text,_inputVerify.text]);
    if([_inputName.text isEqual:@""] || [_inputPassword.text isEqual:@""] || [_inputVerify.text isEqual:@""]){
        [self addAlertTitle:@"提示" andMsg:@"用户名、密码、验证码不能为空!" andComfirm:@"继续输入"];
        return;
    }
    [_myAPI setJsonWIthName:_inputName.text andPassword:_inputPassword.text andCode:_inputVerify.text];
    [_myAPI login];// 由于并发?的原因导致后面的语句在这句没结束就执行了，所以加个弹窗延迟
    UIAlertController *alertWait = [UIAlertController alertControllerWithTitle:@"提示" message:@"等待结果..." preferredStyle:UIAlertControllerStyleAlert];
    [self presentViewController:alertWait animated:YES completion:nil];
    [self performSelector:@selector(delayAlertWait) withObject:nil afterDelay:0.5f];
}

// 判断是否登录成功以及接下来的事件
-(void) delayAlertWait{
    // 消除弹窗
    [self dismissViewControllerAnimated:YES completion:nil];
    NSLog(@"登录成功??? responseCode=%@",_myAPI.responseCode);
    if([_myAPI.responseCode intValue] == 200){
        // 跳转登录后的界面
        UIAlertController *alert1 = [UIAlertController alertControllerWithTitle:@"提示" message:@"登录成功!" preferredStyle:UIAlertControllerStyleAlert];
        // 加载个人信息
        [_myAPI getWithUrl:@"http://172.18.178.57:3000/prod-api/system/user/profile" toDic:[NSNumber numberWithInt:1]];
        [self presentViewController:alert1 animated:YES completion:nil];
        // 在这跳转登录后的界面
        [self performSelector:@selector(trunToInfo) withObject:nil afterDelay:0.5f];
        return;
    }else{
        // 登录失败
        [self addAlertTitle:@"提示" andMsg:_myAPI.msg andComfirm:@"请重新输入"];
        [self getVerify];
    }
}

// 跳转到登录成功后的界面
-(void) trunToInfo{
    [self dismissViewControllerAnimated:YES completion:nil]; // 消除弹窗
    [self setUserVC];
    [_graph.myCache clearList];
    [_graph.table reloadData];
    _tab.viewControllers = @[_userVc,_graph];
    // 跳转到登录成功后的界面
    [_view1 addSubview:_tab.view];
    // 清空登录页面输入框
    _inputName.text = @"";
    _inputPassword.text = @"";
    _inputVerify.text = @"";
}

// 增加弹窗
-(void)addAlertTitle:(NSString*)title andMsg:(NSString*)msg andComfirm:(NSString*)comfirm{
    UIAlertController *alertVC = [UIAlertController alertControllerWithTitle:title message:msg preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *comfirmAc = [UIAlertAction actionWithTitle:comfirm style:UIAlertActionStyleDefault handler:nil];
    [alertVC addAction:comfirmAc];
    [self presentViewController:alertVC animated:YES completion:nil];
}

#pragma mark --SetUserVC
// 设置个人信息界面
-(void)setUserVC{
    _userVc = [[UserViewController alloc] initWithFrame:self.view1.bounds andInfo:self.myAPI.dic];
    _userVc.tabBarItem.title = @"个人信息";
    // tabBar按钮图标
    [_userVc.tabBarItem setImage:[[self getImg:@"test3.png" size:CGSizeMake(30, 30)] imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    [_userVc.tabBarItem setSelectedImage:[[self getImg:@"test3_selected.png" size:CGSizeMake(30, 30)] imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    [self setBackBtn:_userVc];
    // _tab为登录后界面
}
// 以newsize大小获取图像
- (UIImage *)getImg:(NSString*)name size:(CGSize)newsize{
    UIGraphicsBeginImageContext(newsize);
    UIImage *img = [UIImage imageNamed:name];
    [img drawInRect:CGRectMake(0, 0, newsize.width, newsize.height)];
    UIImage* scaledImage = UIGraphicsGetImageFromCurrentImageContext();
    UIGraphicsEndImageContext();
    return scaledImage;
}

// 返回登录界面按钮
-(void)setBackBtn:(UserViewController*)vc{
    UIButton* btn = [[UIButton alloc] initWithFrame:CGRectMake(0, 10, 130, 22)];
    [btn addTarget:self action:@selector(returnRegister) forControlEvents:UIControlEventTouchUpInside];
    [btn setTitle: @"< 退出登陆" forState: UIControlStateNormal];
    [btn setTitleColor:[UIColor blueColor]forState:UIControlStateNormal];
    [btn setTitleShadowColor:[UIColor grayColor] forState:UIControlStateNormal];
    btn.titleLabel.font = [UIFont systemFontOfSize: 20];
    btn.backgroundColor = [UIColor clearColor];
    [vc.view1 addSubview:btn];
}
// 返回登录界面，并刷新验证码
-(void)returnRegister{
    [_tab.view removeFromSuperview];
    [_myAPI getVerify:_btn2];
}

#pragma mark --SetGraphVC
-(void)setGraphUI{
    _graph = [[GraphicListController alloc]initWithFrame:_view1.bounds];
    _graph.tabBarItem.title = @"评论区";
    //[_graph.table reloadData];
    [_graph.tabBarItem setImage:[[self getImg:@"test1.png" size:CGSizeMake(30, 30)] imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    [_graph.tabBarItem setSelectedImage:[[self getImg:@"test1_selected.png" size:CGSizeMake(30, 30)] imageWithRenderingMode:UIImageRenderingModeAlwaysOriginal]];
    // 图文列表界面设置4个按钮
    [self setBtn:_graph.view withText:@"加载" withIndex:0 withAction:@selector(action1)];
    [self setBtn:_graph.view withText:@"清空" withIndex:1 withAction:@selector(action2)];
    [self setBtn:_graph.view withText:@"删除缓存" withIndex:2 withAction:@selector(action3)];
    [self setBtn:_graph.view withText:@"查看缓存" withIndex:3 withAction:@selector(action4)];
}
-(CGRect)getPos:(CGFloat)i{
    CGFloat w = _graph.view.bounds.size.width;
    CGFloat h = _graph.view.bounds.size.height;
    if(i==0) return CGRectMake(0, h*0.05, w/5, 15);
    if(i==1) return CGRectMake(w/5, h*0.05, w/5, 15);
    if(i==2) return CGRectMake(2*w/5, h*0.05, 3*w/10, 15);
    if(i==3) return CGRectMake(7*w/10, h*0.05, 3*w/10, 15);
    return CGRectMake(0, 0, 0, 0);
}
-(UIButton *)setBtn:(UIView *)view withText:(NSString*)text withIndex:(CGFloat)i withAction:(SEL)action0{
    // UIButton* btn = [[UIButton alloc] initWithFrame:CGRectMake((0.05+i*0.3)*w,5, 0.3*w, 24)];
    UIButton* btn = [[UIButton alloc] initWithFrame:[self getPos:i]];
    [btn addTarget:self action:action0 forControlEvents:UIControlEventTouchUpInside];
    [btn setTitle:text forState: UIControlStateNormal];
    [btn setTitleColor:[UIColor blueColor]forState:UIControlStateNormal];
    [btn setTitleShadowColor:[UIColor grayColor] forState:UIControlStateNormal];
    btn.titleLabel.font = [UIFont systemFontOfSize: 20];
    btn.backgroundColor = [UIColor clearColor];
    [view addSubview:btn];
    return btn;
}
// 加载时显示的旋转菊花图标
-(UIViewController*)getLoadingVc{
    UIViewController *vc = [[UIViewController alloc] init];
    vc.view = [[UIView alloc] initWithFrame:CGRectMake(0, 0, 100, 100)];
    UIActivityIndicatorView *waitView = [[UIActivityIndicatorView alloc]initWithActivityIndicatorStyle:UIActivityIndicatorViewStyleLarge];
    vc.view.center = CGPointMake(_view1.bounds.size.width/2, _view1.bounds.size.width/2);
    waitView.center = CGPointMake(_view1.bounds.size.width/2, _view1.bounds.size.width/2);
    waitView.backgroundColor = [UIColor whiteColor];//设置背景颜色
    [vc.view addSubview:waitView];
    [waitView startAnimating];
    return vc;
}
// 按钮绑定事件
// 加载：本地不存在，从网络加载并保存到cache；否则从cache加载
-(void)action1{
    NSLog(@"加载");
    // 加载图标
    UIViewController* vc = [self getLoadingVc];
    [self.graph presentViewController:vc animated:YES completion:nil];
    // 多线程
    NSOperationQueue * queue=[[NSOperationQueue alloc]init];
    //queue.maxConcurrentOperationCount  = 1;
    NSBlockOperation *op1 = [NSBlockOperation blockOperationWithBlock:^{
        NSLog(@"thread1  获取图文列表的文本");
        BOOL isDir;
        if(![[NSFileManager defaultManager] fileExistsAtPath:self.graph.myCache.listCachePath isDirectory:&isDir]){
            // 从网络获取图文列表的文本到self.myAPI.dic2[@"data"]
            [self.myAPI getWithUrl:@"http://172.18.178.57:3000/prod-api/yuan/comment/list" toDic:[NSNumber numberWithInt:2]];
        }else{
            // 从本地cache加载图文列表的文本到list2
            [self.graph.myCache loadListFromCache];
        }
        NSLog(@"thread1  end");
    }];
    NSBlockOperation *op2 = [NSBlockOperation blockOperationWithBlock:^{
        NSLog(@"thread2  将获取的图文列表的文本、图片保存到cache");
        // 如果本地cache不存在图文列表的文本，将lsit2保存到cache;否则返回
        [self.graph.myCache saveListWithDic:self.myAPI.dic2];
        // 将所有图片加载到cache（如果某一图片已在cache则该图片的加载会跳过）
        [self.graph.myCache loadAllImgToCache];
        NSLog(@"thread2  end");
    }];
    [op2 addDependency:op1]; // 让op2 依赖于 op1，则先执行op1，在执行op2
    [queue addOperation:op1]; // 添加操作到队列中
    [queue addOperation:op2];
    // 主线程更新collectionView
    NSBlockOperation *op3 = [NSBlockOperation blockOperationWithBlock:^{
        NSLog(@"thread3  图文列表更新");
        [self.graph.table reloadData];
        //[waitView stopAnimating];
        [self.graph dismissViewControllerAnimated:YES completion:nil]; // 消除弹窗
        NSLog(@"thread3  end");
    }];
    [op3 addDependency:op2];
    [[NSOperationQueue mainQueue] addOperation:op3];
}
-(void)action2{
    NSLog(@"清空");
    [_graph.myCache clearList];
    [_graph.table reloadData];
    [self addAlertTitle:@"提示" andMsg:@"清空成功!" andComfirm:@"确定"];
}
-(void)action3{
    NSLog(@"删除缓存");// 删除缓存
    [_graph.myCache clearList];
    [_graph.table reloadData];
    [[NSFileManager defaultManager] removeItemAtPath:_graph.myCache.imageCachePath error:nil];
    [[NSFileManager defaultManager] removeItemAtPath:_graph.myCache.listCachePath error:nil];
    [self addAlertTitle:@"提示" andMsg:@"已将本地缓存删除!" andComfirm:@"确定"];
}

-(void)action4{
    NSLog(@"查看缓存");// 查看缓存
    NSArray *file = [[[NSFileManager alloc] init] subpathsAtPath:_graph.myCache.imageCachePath];
    // NSLog(@"img=%@",file);
    NSArray *file2 = [[[NSFileManager alloc] init] subpathsAtPath:_graph.myCache.listCachePath];
    // NSLog(@"list=%@",file2);
    NSString * msg = [NSString stringWithFormat:@"图片缓存: %ld张 \n评论缓存: %ld条",file.count,file2.count];
    [self addAlertTitle:@"查看缓存" andMsg:msg andComfirm:@"确定"];
}

@end
