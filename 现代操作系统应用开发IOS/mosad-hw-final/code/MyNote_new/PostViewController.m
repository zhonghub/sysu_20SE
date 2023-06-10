//
//  postViewController.m
//  hw2
//
//  Created by sushan on 2022/9/22.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "PostViewController.h"


@implementation PostViewController

+ (PostViewController *)getInstance{
    static PostViewController *instance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        instance = [[self alloc] init];
        [instance setAddButton];
        [instance setBtnClearAndPost];
    });
    return instance;
}

#pragma mark --set PostViewController UI
-(instancetype)init{
    _r0 = nil;
    self.navigationItem.title = @"新建打卡";
    [self setUI];
    _view1 = [[UIView alloc]initWithFrame:CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height)];
    CGFloat w = _view1.bounds.size.width;
    CGFloat h = _view1.bounds.size.height; // 用于自动布局
    // 单行输入框
    _inputDate = [self getTextField:30 andName:@"日期:" andPlaceHolder:@" Eg: YYYY-MM-DD"];
    _inputPlace= [self getTextField:70 andName:@"地点:" andPlaceHolder:@" Eg: 北京"];
    _inputSights = [self getTextField:110 andName:@"景点:" andPlaceHolder:@" Eg: 故宫"];
    UILabel *labelExp = [[UILabel alloc] initWithFrame:CGRectMake(20, 150, 40, 30)];
    [labelExp setText:@"心得:"];
    // 多行输入框
    _inputExp = [[UITextView alloc] initWithFrame:
                 CGRectMake(30, 180,w - 50, h*0.2)];
    UILabel *label2 = [[UILabel alloc] initWithFrame:CGRectMake(20, 195+h*0.2, 40, 30)];
    [label2 setText:@"配图:"];
    
    [_view1 addSubview:_inputDate];
    [_view1 addSubview:_inputPlace];
    [_view1 addSubview:_inputSights];
    [_view1 addSubview:labelExp];
    [_view1 addSubview:_inputExp];
    [_view1 addSubview:label2];
    //text是输入的结果
    
    _inputExp.backgroundColor = [UIColor clearColor];//设置它的背景颜色
    _inputExp.layer.masksToBounds = YES;// 边框圆角
    _inputExp.layer.cornerRadius = 10; // 圆角弧度
    _inputExp.layer.borderWidth = 5; // 边框宽度
    _inputExp.layer.borderColor = [UIColor grayColor].CGColor;// 边框颜色
    _inputExp.returnKeyType = UIReturnKeyDefault;//返回键的类型
    _inputExp.scrollEnabled = YES;//是否可以拖动
    _inputExp.autoresizingMask = UIViewAutoresizingFlexibleHeight;//自适应
    _inputExp.font = [UIFont fontWithName:@"Arial" size:16];//字体，大小
    // 图片
    _imgs = [[NSMutableArray<UIImage *> alloc] init];
    
    // 根视图控制器
    self.nav = [[UINavigationController alloc]initWithRootViewController:self];
    [self.view addSubview:_view1];
    return self;
}


// 得到单行输入框
-(UITextField *)getTextField:(CGFloat)h1 andName:(NSString *)s1 andPlaceHolder:(NSString *)s2{
    UILabel *label = [[UILabel alloc] initWithFrame:CGRectMake(20, h1, 60, 30)];
    UITextField *text = [[UITextField alloc] initWithFrame:
                         CGRectMake(80, h1,[UIScreen mainScreen].bounds.size.width - 150, 30)];
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
    [_view1 addSubview:label];
    return text;
}

// 返回第i张图片的布局，采用自动布局
-(CGRect) getPos:(unsigned long)i{
    CGFloat w = _view1.bounds.size.width;
    CGFloat h = _view1.bounds.size.height; // 用于自动布局
    CGFloat h2 = (h -(245+h*0.2))*0.25;
    CGFloat s = h*0.15<0.25*w ? h*0.15 : 0.25*w ;
    s = s<h2 ? s:h2;
    // 40,240+h*0.2
    CGRect pos[5];
    pos[0]=CGRectMake(45, 245+h*0.2, s, s);
    pos[1]=CGRectMake(65+s, 245+h*0.2, s, s);
    pos[2]=CGRectMake(85+2*s, 245+h*0.2, s, s);
    pos[3]=CGRectMake(45, 265+h*0.2+s, s, s);
    pos[4]=CGRectMake(65+s, 265+h*0.2+s, s, s);
    return pos[i];
}
// 设置添加图片按钮
-(void) setAddButton{
    _imagePicker = [[UIImagePickerController alloc] init];
    _imagePicker.delegate = self;
    UIImage *image1 = [UIImage imageNamed:@"test4.png"];
    _addButton = [[UIButton alloc] initWithFrame:[self getPos:0]];
    _addButton.backgroundColor = [UIColor clearColor];
    _addButton.layer.masksToBounds = YES;// 圆形按钮
    _addButton.layer.cornerRadius = _addButton.bounds.size.height/2;
    _addButton.layer.borderColor=[UIColor grayColor].CGColor;
    _addButton.layer.borderWidth=1;
    [_addButton setImage:image1 forState:0];
    [_addButton addTarget:self action:@selector(chooseImg) forControlEvents:UIControlEventTouchUpInside];
    [_addButton adjustsImageWhenDisabled];
    [_view1 addSubview:_addButton];
}

// 当添加按钮点击时调用imagePicker
-(void)chooseImg{
    NSLog(@"addButton click");
    [self presentViewController:_imagePicker animated:YES completion:nil];
}

// 获取调用完imagePicker返回的图像并展示，同时将添加按钮右移
- (void)imagePickerController:(UIImagePickerController*)picker
didFinishPickingMediaWithInfo:(NSDictionary<NSString*,id>*)info {
    //获得添加的图片
    UIImage* image=info[UIImagePickerControllerOriginalImage];
    [self.imgs addObject:image];
     
    //在打卡页面上显示图片
    UIImageView* imgView=[[UIImageView alloc] init];
    imgView.frame= [self getPos:self.imgs.count-1];
    imgView.image=image;
    [self.view1 addSubview:imgView];
     
    //图片计数加一，添加图片按钮后移
    self.addButton.frame = [self getPos:self.imgs.count];
    if (self.imgs.count>=5)
        self.addButton.enabled=false;
    [picker dismissViewControllerAnimated:YES completion:nil];
}

// 设置背景渐变
-(void) setUI{
    // 设置背景渐变
    //  创建 CAGradientLayer 对象
    _gradient = [CAGradientLayer layer];
    //  设置 gradientLayer 的 Frame
    _gradient.frame = CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height);
    //  创建渐变色数组，需要转换为CGColor颜色
    _gradient.colors = @[(id)[UIColor colorWithRed:0xb5/255.0 green:0xa5/255.0 blue:0xa4/255.0 alpha:1].CGColor,
                         (id)[UIColor colorWithRed:0x87/255.0 green:0xc0/255.0 blue:0x35/255.0 alpha:1].CGColor];
    //  设置三种颜色变化点，取值范围 0.0~1.0
    _gradient.locations = @[@(0.1f) ,@(1.0f)];
    //  设置渐变颜色方向，左上点为(0,0), 右下点为(1,1)
    _gradient.startPoint = CGPointMake(0, 0);
    _gradient.endPoint = CGPointMake(1, 1);
    //  添加渐变色到创建的 UIView 上去
    [self.view.layer insertSublayer:_gradient atIndex:0];
}

// 展示图片，该函数用于详情页面
- (void)setImgPos{
    _addButton.frame = [self getPos:0];
    for(int i=0;i<self.imgs.count;i++){
        UIImage* img=self.imgs[i];
        UIImageView* imgView=[[UIImageView alloc] init];
        imgView.frame= [self getPos:i];
        imgView.image=img;
        [_view1 addSubview:imgView];
        self.addButton.frame = [self getPos:self.imgs.count];
    }
    if (self.imgs.count>=5)
        self.addButton.enabled=false;
}

// 用于详情页面，显示打卡
- (void)showWith:(NSDictionary *) r1{
    _r0 = r1;
    [[NSOperationQueue mainQueue] addOperationWithBlock:^{
        self.inputDate.text = r1[@"date"];
        self.inputPlace.text = r1[@"place"];
        self.inputSights.text = r1[@"sights"];
        self.inputExp.text = r1[@"exp"];
        self.imgs = [[NSMutableArray<UIImage *> alloc] init];
        NSString * name1 = r1[@"nowName"];
        for(int j = 0; j <= 4; ++j){
            NSString * name2 = [NSString stringWithFormat:@"%@%@",@"media",[NSNumber numberWithInt:j]];
            if([r1 objectForKey:name2]){
                NSLog(@"read begin: %@_%@.jpg",name1,name2);
                UIImage * img = [self getImgWithName1:r1[@"nowName"] withName2:name2];
                if(img){
                    [self.imgs addObject:img];
                }else{
                    NSLog(@"%@ %@ is nil",name1,name2);
                }
            }else{
                break;
            }
        }
        [self setImgPos];
    }];
}

// 工厂模式返回一个详情页面
-(PostViewController*)initWithItem:(NSDictionary *) r1{
    PostViewController * vc = [[PostViewController alloc] init];
    vc.navigationItem.title=@"打卡详情";
    [vc showWith:r1];
    [vc closeInput];
    self.addButton.enabled=false;
    return vc;
}

// 读取图片
-(UIImage *)getImgWithName1:(NSString*)name1 withName2:(NSString*)name2{
                NSString *imgName = [NSString stringWithFormat:@"%@_%@.jpg",name1,name2];
    // 图片路径
    NSString *imagePath = [[RecordStorage getInstance].imageCachePath stringByAppendingPathComponent:imgName];
    UIImage *img = [UIImage imageWithContentsOfFile:imagePath];
    return img;
}


-(void)closeInput{
    [_inputDate setEnabled:NO];
    [_inputPlace setEnabled:NO];
    [_inputSights setEnabled:NO];
    [_inputExp setEditable:NO];
}

#pragma mark --set Buttons1:Editor and delete and reload

// 设置编辑按钮
-(void)setEditorButton{
    CGFloat w = self.view1.bounds.size.width;
    CGFloat h = self.view1.bounds.size.height;
    [self addBtnText:@"编辑" Withx:9*w/10 Withy:h*0.06 WithSize:w*0.13 withAction:@selector(turnToEditorView)];
    [self addBtnText:@"删除" Withx:9*w/10 Withy:h*0.14 WithSize:w*0.13 withAction:@selector(removeItem0)];
    [self addBtnText:@"刷新" Withx:9*w/10 Withy:195+h*0.2 WithSize:w*0.10 withAction:@selector(reloadImg)];
}

// 圆形按钮
-(void)addBtnText:(NSString*)text Withx:(CGFloat)x Withy:(CGFloat)y WithSize:(CGFloat)size withAction:(SEL)action0{
    UIButton * btn = [[UIButton alloc] initWithFrame:CGRectMake(0, 0, size, size)];
    [btn addTarget:self action:action0 forControlEvents:UIControlEventTouchUpInside];
    btn.center=CGPointMake(x, y);
    btn.layer.borderColor=[UIColor blackColor].CGColor;
    btn.layer.borderWidth=2;
    btn.layer.cornerRadius = btn.bounds.size.width / 2.0; // 圆形按钮
    [btn setTitle:text forState: UIControlStateNormal];
    btn.titleLabel.font = [UIFont systemFontOfSize: size/4.0];
    btn.backgroundColor = [UIColor clearColor];
    [btn setTitleColor:[UIColor blackColor]forState:UIControlStateNormal];
    [_view1 addSubview:btn];
}

-(void)turnToEditorView{
    self.tabBarController.selectedIndex=1;//tabBarController
    _addButton.enabled=true;
    [[PostViewController getInstance] showWith:_r0];
    [self addAlertTitle:@"提示" andMsg:@"已跳转到编辑页面!" andComfirm:@"确定"];
}

-(void)removeItem0{
    self.tabBarController.selectedIndex=0;//tabBarController
    [[RecordStorage getInstance] removeItem0:_r0];
    _r0 = nil;
    [self clearInput];
    //[[RecordStorage getInstance] readFromCache];
    [[FindViewController getInstance].tableview reloadData];
    [[FindViewController getInstance].nav popToRootViewControllerAnimated:YES];
    //[self addAlertTitle:@"提示" andMsg:@"已删除该条打卡!" andComfirm:@"确定"];
    UIAlertController *alertVC = [UIAlertController alertControllerWithTitle:@"提示" message:@"已删除该条打卡!" preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *comfirmAc = [UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil];
    [alertVC addAction:comfirmAc];
    [[FindViewController getInstance] presentViewController:alertVC animated:YES completion:nil];
}

-(void)reloadImg{
    [self showWith:_r0];
}
     
// 增加弹窗
-(void)addAlertTitle:(NSString*)title andMsg:(NSString*)msg andComfirm:(NSString*)comfirm{
    UIAlertController *alertVC = [UIAlertController alertControllerWithTitle:title message:msg preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *comfirmAc = [UIAlertAction actionWithTitle:comfirm style:UIAlertActionStyleDefault handler:nil];
    [alertVC addAction:comfirmAc];
    [self presentViewController:alertVC animated:YES completion:nil];
}

// 隐藏打卡页面键盘
-(void)hidKeyboard{
    [_inputDate resignFirstResponder];
    [_inputPlace resignFirstResponder];
    [_inputSights resignFirstResponder];
    [_inputExp resignFirstResponder];
}
// 打卡页面清空输入框和图片
-(void)clearInput{
    NSLog(@"clearInput");
    self.r0 = nil;
    self.inputDate.text=@"";
    self.inputPlace.text=@"";
    self.inputSights.text=@"";
    self.inputExp.text = @"";
    // 删除图片在打卡页面的子视图
    for(UIView *mylabelview in [_view1 subviews]){
        if ([mylabelview isKindOfClass:[UIImageView class]]) {
            [mylabelview removeFromSuperview];
        }
    }
    // 清空选择的图片
    self.imgs = [[NSMutableArray<UIImage *> alloc] init];
    // 添加按钮回到起点
    self.addButton.frame = [self getPos:0];
    // 添加按钮设为可用
    self.addButton.enabled=true;
}

#pragma mark --set Buttons1:clear and post
- (void) setBtnClearAndPost{
    // 给vc2增加一个“发布”按钮
    self.navigationItem.rightBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"发布" style:UIBarButtonItemStyleDone target:self action:@selector(btnClick1)];
    
    // 给vc2增加一个“清空”按钮
    self.navigationItem.leftBarButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"清空"  style:UIBarButtonItemStyleDone target:self action:@selector(btnClick2)];
}
//发布按钮
- (void)btnClick1{
    // 隐藏键盘
    [self hidKeyboard];
    NSLog(@"button1 is click");
    // 如果时间、地点、景点存在为空的情况，不能发布，需要继续编辑打卡
    if( [_inputDate.text isEqual:@""] || [_inputPlace.text isEqual:@""] || [_inputSights.text isEqual:@""]){
        UIAlertController *alertVC0 = [UIAlertController alertControllerWithTitle:@"提示" message:@"时间、地点、景点不能为空！" preferredStyle:UIAlertControllerStyleAlert];
        UIAlertAction *comfirmAc0 = [UIAlertAction actionWithTitle:@"继续编辑"     style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {}];
        [alertVC0 addAction:comfirmAc0];
        [self presentViewController:alertVC0 animated:YES completion:nil];
        return;
    }
    UIAlertController *alertVC = [UIAlertController alertControllerWithTitle:@"提示" message:@"是否发布打卡？" preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *comfirmAc = [UIAlertAction actionWithTitle:@"是，查看最新打卡"     style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        // 代码块隐式地保留'self'; 明确地使用“self”来表示这是有意的行为
        // 将数据添加到数据源
        NSMutableArray *list = [[NSMutableArray alloc] init];
        [list addObject:self.inputDate.text];
        [list addObject:self.inputPlace.text];
        [list addObject:self.inputSights.text];
        [list addObject:self.inputExp.text];
        for(int i = 0; i < self.imgs.count; ++i){
            [list addObject:self.imgs[i]];
        }
        [[RecordStorage getInstance] storeWithList:list withDic:self.r0];
        //[self.store readFromCache];
        [[FindViewController getInstance].tableview reloadData];
        NSLog(@"store");
        // 发现页面先返回根视图tableView（如果当前页面不是tableView）
        [[FindViewController getInstance].nav popToRootViewControllerAnimated:YES];
        // 发现页返回顶部并更新数据源
        //[[FindViewController getInstance] returnTop];
        // 转到发现页面
        self.tabBarController.selectedIndex=0;//tabBarController
        PostViewController *dectrl = [[PostViewController alloc] initWithItem:[RecordStorage getInstance].records[0]];
        [dectrl setEditorButton];
        // 再进入打卡详情页面，查看最新打卡
        [[FindViewController getInstance].nav pushViewController:dectrl animated:YES];
        // 0.5s的弹窗
        UIAlertController *alert1 = [UIAlertController alertControllerWithTitle:@"提示" message:@"发布成功" preferredStyle:UIAlertControllerStyleAlert];
        // 弹窗以浮动形式加到vc1
        [[FindViewController getInstance] presentViewController:alert1 animated:YES completion:nil];
        [self performSelector:@selector(delayAlert1) withObject:nil afterDelay:0.5f];
        // 清除输入框和图片
        [self clearInput];
    }];
    UIAlertAction *comfirmAc2 = [UIAlertAction actionWithTitle:@"否，继续编辑" style:UIAlertActionStyleDefault handler:nil];
    [alertVC addAction:comfirmAc];
    [alertVC addAction:comfirmAc2];
    [self presentViewController:alertVC animated:YES completion:nil];
}
// 去除弹窗
-(void) delayAlert1{
    [[FindViewController getInstance] dismissViewControllerAnimated:YES completion:nil];
}

// 清空按钮
- (void)btnClick2{
    [self hidKeyboard];
    NSLog(@"button2 is click");
    UIAlertController *alertVC = [UIAlertController alertControllerWithTitle:@"提示" message:@"是否清空打卡内容？" preferredStyle:UIAlertControllerStyleAlert];
    UIAlertAction *comfirmAc = [UIAlertAction actionWithTitle:@"是" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {
        // 清除输入框
        [self clearInput];
    }];
    UIAlertAction *comfirmAc2 = [UIAlertAction actionWithTitle:@"否" style:UIAlertActionStyleDefault handler:^(UIAlertAction * _Nonnull action) {}];
    [alertVC addAction:comfirmAc];
    [alertVC addAction:comfirmAc2];
    [self presentViewController:alertVC animated:YES completion:nil];
}

@end
