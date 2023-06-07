//
//  GraphicListController.m
//  hw3
//
//  Created by sushan on 2022/10/13.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "GraphicListController.h"


@implementation GraphicListController
-(instancetype)initWithFrame:(CGRect)frame{
    self.view = [[UIView alloc]initWithFrame:frame];
    self.view.backgroundColor = [UIColor whiteColor];
    _table = [[UICollectionView alloc] initWithFrame:CGRectMake(0, 48, frame.size.width, frame.size.height*0.85) collectionViewLayout:[self getLatout]];
    _table.backgroundColor = [UIColor whiteColor];
    // 注册cell
    [_table registerClass:[UICollectionViewCell class] forCellWithReuseIdentifier:@"cellID"];
    // 遵守协议
    _table.delegate = self;
    _table.dataSource = self;
    [self.view addSubview:_table];
    // "加载" "清空" "删除缓存"
    _myCache = [[MyCacheAPI alloc] init];
    return self;

}

- (UICollectionViewFlowLayout*) getLatout{
    // UICollectionViewFlowLayout流水布局的内部成员属性有以下：
    UICollectionViewFlowLayout *layout = [[UICollectionViewFlowLayout alloc]init];
    layout.itemSize = CGSizeMake(100, 100);// 定义大小
    layout.minimumLineSpacing = 2;// 设置最小行间距
    layout.minimumInteritemSpacing = 2;// 设置垂直间距
    // 设置滚动方向（默认垂直滚动）
    // layout.scrollDirection = UICollectionViewScrollDirectionHorizontal;// 水平滚动
    return layout;
}

#pragma mark -- UICollectionViewDataSource
//定义展示的UICollectionViewCell的个数
-(NSInteger)collectionView:(UICollectionView *)collectionView numberOfItemsInSection:(NSInteger)section{
    //每个section中cell的个数,[list2[section].imgs count] + 3
    NSInteger num = 0;//图片张数
    for(int j = 1; j <=9; ++j){
        NSString * imgName = [NSString stringWithFormat:@"%@%@",@"media",[NSNumber numberWithInt:j]];
        if([_myCache.list2[section][imgName] isEqualToString:@""]){
            continue;
        }
        num++;
    }
    return num+3;
}
//定义展示的Section的个数
-(NSInteger)numberOfSectionsInCollectionView:(UICollectionView *)collectionView{
    return [_myCache.list2 count];// section的个数
}

//每个UICollectionView展示的内容
-(UICollectionViewCell *)collectionView:(UICollectionView *)collectionView cellForItemAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString * cellID = @"cellID";
    UICollectionViewCell * cell = [collectionView dequeueReusableCellWithReuseIdentifier:cellID forIndexPath:indexPath];
    cell.backgroundColor = [UIColor whiteColor];
    if(_myCache.list2.count <= indexPath.section){
        return cell;
    }
    CGFloat w = _table.bounds.size.width;
    NSDictionary * temp = _myCache.list2[indexPath.section];
    if(indexPath.row <= 1){
        UILabel *label = [[UILabel alloc] initWithFrame:CGRectMake(0, 0, w*0.89, 25)];
        label.layer.masksToBounds = YES;// 边框圆角
        label.layer.cornerRadius = 10; // 圆角弧度
        label.layer.borderWidth = 2; // 边框宽度
        label.layer.borderColor = [UIColor grayColor].CGColor;// 边框颜色
        if(indexPath.row == 0){
            [label setText:[NSString stringWithFormat:@"  评论ID: %@    发布者: %@",temp[@"commentId"], temp[@"createBy"]]];
        }else{
            [label setText:[NSString stringWithFormat:@"  发布时间: %@",temp[@"createTime"]]];
        }
        [cell setBackgroundView:label];
    }else if(indexPath.row == 2){
        UITextView *textView = [self getTextViewWithFrame:CGRectMake(0, 0, w*0.89, 100)];
        [textView setText:[NSString stringWithFormat:@"评论内容:   %@",temp[@"content"]]];
        [cell setBackgroundView:textView];
        
    }
    else if(indexPath.row >= 3){//这里为每个图片都分配了一个cell，也可以将所有图片放在一个cell里
        // temp.imgs[indexPath.row-3]
        NSOperationQueue * queue=[[NSOperationQueue alloc]init];
        [queue addOperationWithBlock:^{
            NSString * imgIndex = [NSString stringWithFormat:@"%@%ld",@"media",indexPath.row-2];
            NSString * urlStr = temp[imgIndex];
            UIImage *img = [self.myCache getImgByUrl:urlStr];
            [[NSOperationQueue mainQueue] addOperationWithBlock:^{
                UIImageView* imgView=[[UIImageView alloc] init];
                imgView.frame= CGRectMake(0, 0, w*0.26, w*0.26);
                imgView.image=img;// temp.imgs[indexPath.row-3]
                [cell setBackgroundView:imgView];
            }];
        }];
    }
    return cell;
}

-(UITextView*)getTextViewWithFrame:(CGRect)frame{
    UITextView* textView =  [[UITextView alloc] initWithFrame:frame];
    textView.backgroundColor = [UIColor clearColor];//设置它的背景颜色
    textView.layer.masksToBounds = YES;// 边框圆角
    textView.layer.cornerRadius = 10; // 圆角弧度
    textView.layer.borderWidth = 2; // 边框宽度
    textView.layer.borderColor = [UIColor grayColor].CGColor;// 边框颜色
    textView.returnKeyType = UIReturnKeyDefault;//返回键的类型
    textView.scrollEnabled = YES;//是否可以拖动
    textView.autoresizingMask = UIViewAutoresizingFlexibleHeight;//自适应
    textView.font = [UIFont fontWithName:@"Arial" size:18];//字体，大小
    [textView setEditable:NO];
    return textView;
}

#pragma mark --UICollectionViewDelegateFlowLayout
//定义每个UICollectionView 的大小
- (CGSize)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout*)collectionViewLayout sizeForItemAtIndexPath:(NSIndexPath *)indexPath{
    CGFloat w = _table.bounds.size.width;
    if(indexPath.row <= 1){
        return CGSizeMake(w*0.89, 25);
    }
    if(indexPath.row ==2){
        return CGSizeMake(w*0.89, 100);
    }
    return CGSizeMake(w*0.26, w*0.26);
}
//定义每个UICollectionView 的 margin(每个section的边缘)
-(UIEdgeInsets)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout *)collectionViewLayout insetForSectionAtIndex:(NSInteger)section{
    CGFloat w = _table.bounds.size.width;
    return UIEdgeInsetsMake(30, 0.05*w, 20, 0.05*w);// 上、左、下、右
}
//动态设置每行的间距大小
- (CGFloat)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout*)collectionViewLayout minimumLineSpacingForSectionAtIndex:(NSInteger)section{
    return 8;
}
//动态设置每列的间距大小
- (CGFloat)collectionView:(UICollectionView *)collectionView layout:(UICollectionViewLayout*)collectionViewLayout minimumInteritemSpacingForSectionAtIndex:(NSInteger)section{
    CGFloat w = _table.bounds.size.width;
    return 0.06*w; // 设置合适的列间距，使最后一行的图片对齐
}


#pragma mark --UICollectionViewDelegate
//UICollectionView被选中时调用的方法
-(void)collectionView:(UICollectionView *)collectionView didSelectItemAtIndexPath:(NSIndexPath *)indexPath{
    NSLog(@"select section %zd,row %zd",indexPath.section,indexPath.row);
    
}

//返回这个UICollectionView是否可以被选择
-(BOOL)collectionView:(UICollectionView *)collectionView shouldSelectItemAtIndexPath:(NSIndexPath *)indexPath{
    if(indexPath.row == 2) return YES;
    return NO;// 这里只是展示，如果要评论，则设为YES
}

// cell的动画效果
- (void)collectionView:(UICollectionView *)collectionView willDisplayCell:(UICollectionViewCell *)cell forRowAtIndexPath:(NSIndexPath *)indexPath{
    cell.backgroundView.layer.transform = CATransform3DMakeScale(0.3, 0.3, 0.5);
    // 滚动时的加载动画
    [UIView animateWithDuration:0.3 animations:^{cell.backgroundView.layer.transform = CATransform3DMakeScale(1, 1, 1);}];
}

@end
