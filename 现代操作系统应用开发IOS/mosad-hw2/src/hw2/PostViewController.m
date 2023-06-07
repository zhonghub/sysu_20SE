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
-(instancetype)init{
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
// 设置添加按钮
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
    self.addButton.enabled=false;
    for(int i=0;i<self.imgs.count;i++){
        UIImage* img=self.imgs[i];
        UIImageView* imgView=[[UIImageView alloc] init];
        imgView.frame= [self getPos:i];
        imgView.image=img;
        [_view1 addSubview:imgView];
    }
}

// 用于详情页面，只显示，不编辑
- (void)showWith:(Record *) r1{
    _inputDate.text = r1.date;
    [_inputDate setEnabled:NO];
    _inputPlace.text = r1.place;
    [_inputPlace setEnabled:NO];
    _inputSights.text = r1.sights;
    [_inputSights setEnabled:NO];
    _inputExp.text = r1.experience;
    [_inputExp setEditable:NO];
    _imgs = r1.imgs;
    [self setImgPos];
}

@end
