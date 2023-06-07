//
//  AppDelegate.h
//  hw3
//
//  Created by sushan on 2022/10/24.
//  Copyright © 2022 SYSU. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <CoreData/CoreData.h>

@interface AppDelegate : UIResponder <UIApplicationDelegate>

@property (readonly, strong) NSPersistentContainer *persistentContainer;

- (void)saveContext;


@end

