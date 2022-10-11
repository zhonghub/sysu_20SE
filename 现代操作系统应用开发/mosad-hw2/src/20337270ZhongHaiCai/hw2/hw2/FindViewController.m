//
//  findViewController.m
//  hw2
//
//  Created by sushan on 2022/9/20.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "FindViewController.h"

@implementation FindViewController
- init{
    self.navigationItem.title =@"打卡清单";
    _store = [[RecordStorage alloc] init];//初始化数据源
    [self setUI];//设置渐变色图层
    _tableview=[[UITableView alloc]initWithFrame:CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height*0.8)
                                           style:UITableViewStyleGrouped];
    _tableview.backgroundColor=[UIColor clearColor];
    _tableview.separatorInset = UIEdgeInsetsMake(0,30, 0, 20);
    _tableview.separatorStyle = UITableViewCellSeparatorStyleSingleLine;
    // 设置数据源和委托
    _tableview.delegate = self;
    _tableview.dataSource = self;
    // 搜索框
    _search=[[UISearchBar alloc] initWithFrame:(CGRectMake(0, 0, self.view.bounds.size.width - 10, 50))];
    _tableview.tableHeaderView=_search;
    _search.delegate = self;
    [_tableview addSubview:_search];
    
    // 把FindViewController作为根控制器
    self.nav = [[UINavigationController alloc]initWithRootViewController:self];
    [self.view addSubview:_tableview];
    
    NSLog(@"FindViewController");
    return self;
}

- (NSInteger)numberOfSectionsInTableView:(UITableView *)tableView {
    return [_store.records count];// section的个数
}
- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section {
    return 4; //每个cell的个数：date;place;sights;experience
}

// 每个section的头部的上下间距
-(CGFloat)tableView:(UITableView *)tableView heightForHeaderInSection:(NSInteger)section{
    if(section==0){
        return 40;
    }
    return 25;
}


-(UITableViewCell *)tableView:(UITableView*)tableView
        cellForRowAtIndexPath:(NSIndexPath *)indexPath{
    //[self.tableview reloadData];
    NSString *cellID = @"cellID";
    UITableViewCell *cell = [tableView dequeueReusableCellWithIdentifier:cellID];
    if(cell == nil){
        // 代码块内只做Cell样式的处理，不做数据设置
        cell = [[UITableViewCell alloc] initWithStyle:UITableViewCellStyleDefault
                                      reuseIdentifier:cellID];
        // 当给新的cell分配内存时输出其indexPath
        NSLog(@"new cell: section %ld, row %ld",indexPath.section,indexPath.row);
    }
    else{
        while ([cell.contentView.subviews lastObject] != nil){
            [(UITableViewCell *)[cell.contentView.subviews lastObject] removeFromSuperview];
        }
    }
    [cell setBackgroundColor:[UIColor clearColor]];
    Record *temp = [[Record alloc] init];
    if(_store.records.count>indexPath.section){
        temp = _store.records[indexPath.section];
        // [_store.records objectAtIndex:indexPath.section];
    }
    else{
        temp.date = @"";
        temp.place = @"";
        temp.sights = @"";
        temp.experience = @"";
    }
    if(indexPath.row==0)
        cell.textLabel.text=[NSString stringWithFormat:@"日期      %@",temp.date];
    if(indexPath.row==1)
        cell.textLabel.text=[NSString stringWithFormat:@"地点      %@",temp.place];
    if(indexPath.row==2)
        cell.textLabel.text=[NSString stringWithFormat:@"景点      %@",temp.sights];
    if(indexPath.row==3)
        cell.textLabel.text=[NSString stringWithFormat:@"旅游心得   %@",temp.experience];
    //NSLog(@"cell1");
    //cell.selectionStyle = UITableViewCellSelectionStyleGray;
    return cell;
}

- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath{
    return 30;
}

// 每个section的标题
-(NSString *)tableView:(UITableView *)tableView titleForHeaderInSection:(NSInteger)section{
    NSString * groupName = @"打卡";
    if(section == 0)
        groupName =  @"最新打卡：打卡0(点击打卡内容查看详情)";
    else
        groupName = [groupName stringByAppendingFormat:@"%ld", section];
    return groupName;
}

// section的动画效果
- (void)tableView:(UITableView *)tableView willDisplayHeaderView:(UIView *)view forSection:(NSInteger)section {
    UITableViewHeaderFooterView *header = (UITableViewHeaderFooterView *)view;
    header.textLabel.textColor = [UIColor redColor];
    header.textLabel.font = [UIFont boldSystemFontOfSize:15];
    CGRect headerFrame = header.frame;
    header.textLabel.frame = headerFrame;
    // header.textLabel.textAlignment = NSTextAlignmentCenter;// 居中
}

// 选择cell执行什么操作,进入详情页面
- (void)tableView:(UITableView *)tableView didSelectRowAtIndexPath:(NSIndexPath*)indexPath{
    DetailsViewController *dectrl = [[DetailsViewController alloc] initWithItem:_store.records[indexPath.section]];
    // 进入打卡详情页面
    [self.nav pushViewController:dectrl animated:YES];
    NSLog(@"select section %zd,row %zd",indexPath.section,indexPath.row);
}
// cell的动画效果
- (void)tableView:(UITableView *)tableView willDisplayCell:(UITableViewCell *)cell forRowAtIndexPath:(NSIndexPath *)indexPath{
    cell.layer.transform = CATransform3DMakeScale(0.3, 0.3, 1);
    // 滚动时的加载动画
    [UIView animateWithDuration:0.5 animations:^{cell.layer.transform = CATransform3DMakeScale(1, 1, 1);}];
    [cell.contentView.layer setBorderColor:UIColor.lightGrayColor.CGColor];
    [cell.contentView.layer setBorderWidth:1];
    cell.contentView.layer.borderWidth=4;
    cell.contentView.layer.cornerRadius=12;
    cell.contentView.layer.masksToBounds=YES;
}

// 搜索栏
-(void)searchBarCancelButtonClicked:(UISearchBar *)searchBar{
    [searchBar setShowsCancelButton:NO animated:YES];
    searchBar.text=@"";
    [searchBar endEditing:YES];
}

-(void)searchBarTextDidBeginEditing:(UISearchBar *)searchBar {
    [searchBar setShowsCancelButton:YES animated:YES];
}
// 搜索按钮被点击
- (void)searchBarSearchButtonClicked:(UISearchBar*)searchBar{
     NSString *input=[searchBar text];//获得输入
     bool succ=false;
     for(int i=0;i<self.store.records.count;i++){
         NSString *info = [NSString stringWithFormat:@"%@  %@  %@",_store.records[i].date, _store.records[i].place, _store.records[i].sights];
         if([info rangeOfString:input].location != NSNotFound){
             [self skipToIndex:i withInfo:info];//找到
             succ=true;
             break;
         }
     }
    if(!succ) [self noReply];//没找到
}
//没找到
- (void)noReply {
    UIAlertController* alert = [UIAlertController alertControllerWithTitle:@"提示" message:@"无查询相关内容" preferredStyle:UIAlertControllerStyleAlert];
    [alert addAction:[UIAlertAction actionWithTitle:@"确定" style:UIAlertActionStyleDefault handler:nil]];
    [self presentViewController:alert animated:true completion:nil];
}
//找到，通过下标index打开对应的详情页面
- (void)skipToIndex:(int)index withInfo:(NSString*)info {
    UIAlertController *alert = [UIAlertController alertControllerWithTitle:@"找到" message:info preferredStyle:UIAlertControllerStyleAlert];
    [alert addAction:[UIAlertAction actionWithTitle:@"查看"
    style:UIAlertActionStyleDefault handler:^(UIAlertAction* _Nonnull action) {
        // 若找到则新建对应的详情页面并跳转
        DetailsViewController* dectrl=[[DetailsViewController alloc]
                                    initWithItem:self.store.records[index]];
        [self.navigationController pushViewController:dectrl animated:YES];
        // 清空搜索框
        self.search.text=@"";
     }]];
    [alert addAction:[UIAlertAction actionWithTitle:@"取消" style:UIAlertActionStyleDefault handler:nil]];
    [self presentViewController:alert animated:true completion:nil];
}

-(void) setUI{
    // 设置背景渐变
    //  创建 CAGradientLayer 对象
    _gradient = [CAGradientLayer layer];
    //  设置 gradientLayer 的 Frame
    _gradient.frame = CGRectMake(0, 0,[UIScreen mainScreen].bounds.size.width, [UIScreen mainScreen].bounds.size.height);
    //  创建渐变色数组，需要转换为CGColor颜色
    _gradient.colors = @[
        (id)[UIColor colorWithRed:0xa7/255.0 green:0xb0/255.0 blue:0x75/255.0 alpha:1].CGColor,
        (id)[UIColor colorWithRed:0xe5/255.0 green:0xc5/255.0 blue:0xe4/255.0 alpha:1].CGColor];
    //  设置三种颜色变化点，取值范围 0.0~1.0
    _gradient.locations = @[@(0.1f) ,@(1.0f)];
    //  设置渐变颜色方向，左上点为(0,0), 右下点为(1,1)
    _gradient.startPoint = CGPointMake(0, 0);
    _gradient.endPoint = CGPointMake(1, 1);
    //  添加渐变色到创建的 UIView 上去
    [self.view.layer insertSublayer:_gradient atIndex:0];
}

@end
