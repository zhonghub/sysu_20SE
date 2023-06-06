# 中级实训总结报告

通过本次中级实训的三个阶段，我主要学习到了以下3个方面的知识：

1.学会使用java工具链（javac，java，ant，junit）进行项目的构建、编译、运行、单元测试，以及使用sonar对代码质量进行评测。

2.加深了我的面向对象程序设计的理解以及对java语言的掌握。

3.加深了我对几种搜索算法的理解（BFS，DFS，启发式搜索），以及如何在代码中实现和使用这些算法。



## 阶段一

阶段一主要是学习java工具链（javac，java，ant，junit）和代码评测工具soanr的使用，其中使用ant+junit实现自动化的单元测试的阶段一的重点。

### javac

用法：
$$
javac <options> <source files>
$$
其中, 可能的选项包括:

```

  -g                         生成所有调试信息
  -g:none                    不生成任何调试信息
  -g:{lines,vars,source}     只生成某些调试信息
  -nowarn                    不生成任何警告
  -verbose                   输出有关编译器正在执行的操作的消息
  -deprecation               输出使用已过时的 API 的源位置
  -classpath <路径>            指定查找用户类文件和注释处理程序的位置
  -cp <路径>                   指定查找用户类文件和注释处理程序的位置
  -sourcepath <路径>           指定查找输入源文件的位置
  -bootclasspath <路径>        覆盖引导类文件的位置
  -extdirs <目录>              覆盖所安装扩展的位置
  -endorseddirs <目录>         覆盖签名的标准路径的位置
  -proc:{none,only}          控制是否执行注释处理和/或编译。
  -processor <class1>[,<class2>,<class3>...] 要运行的注释处理程序的名称; 绕过默认的搜索进程
  -processorpath <路径>        指定查找注释处理程序的位置
  -d <目录>                    指定放置生成的类文件的位置
  -s <目录>                    指定放置生成的源文件的位置
  -implicit:{none,class}     指定是否为隐式引用文件生成类文件
  -encoding <编码>             指定源文件使用的字符编码
  -source <发行版>              提供与指定发行版的源兼容性
  -target <发行版>              生成特定 VM 版本的类文件
  -version                   版本信息
  -help                      输出标准选项的提要
  -A关键字[=值]                  传递给注释处理程序的选项
  -X                         输出非标准选项的提要
  -J<标记>                     直接将 <标记> 传递给运行时系统
  -Werror                    出现警告时终止编译
  @<文件名>                     从文件读取选项和文件名


```

在本次实训中，我使用得最多得便是 -classpath和 -d，用于指定classpath和生成的.class文件得目录。



### Ant

Ant是Unix的**Make**构建工具的更好**替代品**，因此使用和Make非常相似。 Ant是用Java编写的，需要JVM来构建Java项目。Ant使用XML来描述构建代码，默认情况下，它的XML文件名是`build.xml`

Ant通常含有4种元素：project项目标签，target目标标签，task任务标签，property属性标签。

Ant通过ant target来运行目标，类似于make中的make run，make clean。

在本次实训中，我经常编写target有clean，complie，run，test，分别用于：

| clean   | 清空生成的.class文件 |
| ------- | -------------------- |
| complie | 编译                 |
| run     | 运行                 |
| test    | Junit单元测试        |



### Junit

JUnit 是一个 Java 编程语言的单元测试框架。JUnit 在测试驱动的开发方面有很重要的发展，是起源于 JUnit 的一个统称为 xUnit 的单元测试框架之一。

#### 使用Junit的好处

1. 可以书写一系列的测试方法，对项目所有的接口或者方法进行单元测试。
2. 启动后，自动化测试，并判断执行结果, 不需要人为的干预。
3. 只需要查看最后结果，就知道整个项目的方法接口是否通畅。
4. 每个单元测试用例相对独立，由Junit 启动，自动调用。不需要添加额外的调用语句。
5. 添加，删除，屏蔽测试方法，不影响其他的测试方法。 开源框架都对JUnit 有相应的支持。

#### Junit 断言

Junit断言就是"判断"。Junit所有的断言都包含在 Assert 类中。

这个类提供了很多有用的断言方法来编写测试用例。只有**失败的断言**才会被记录。Assert 类中的一些有用的方法列式如下：

1. `void assertEquals(boolean expected, boolean actual)`:检查两个变量或者等式是否相等
2. `void assertTrue(boolean condition)`:检查条件为真
3. `void assertFalse(boolean condition)`:检查条件为假
4. `void assertNotNull(Object object)`:检查对象不为空
5. `void assertNull(Object object)`:检查对象为空
6. `void assertSame(boolean condition)`: assertSame() 方法检查两个相关对象是否指向同一个对象
7. `void assertNotSame(boolean condition)`: assertNotSame() 方法检查两个相关对象是否不指向同一个对象
8. `void assertArrayEquals(expectedArray, resultArray)`:assertArrayEquals() 方法检查两个数组是否相等

在本次实训中，我经常使用的Junit断言就是assertEquals，用于判断目标结果与期望结果是否相同。



## 阶段二

阶段二主要是通过继承info.gridworld里的一些类，并重写（Override）父类的一些方法以实现对父类某些功能的拓展。

在这个阶段中，令我感悟最深的是Critter的子类实现与其父类不同的act方法的途径：不是通过直接重写act方法，而是通过重写act调用的其它方法（如getActors，processActors，getMoveLocations，selectMoveLocation，makeMove）以实现改变了子类的act方法的功能。

```java
// @file: info/gridworld/actor/Critter.java
// @line: 38-47
	public void act()
    {
        if (getGrid() == null)
            return;
        ArrayList<Actor> actors = getActors();
        processActors(actors);
        ArrayList<Location> moveLocs = getMoveLocations();
        Location loc = selectMoveLocation(moveLocs);
        makeMove(loc);
    }
```

这也给了我一个启示：我们可以把接口方法作为公有方法，让其它对象调用，然后在这个接口方法里通过调用其它方法实现功能。这样我们就可以通过在子类里重写调用的其它方法以实现更加丰富的拓展功能，并且还能保证代码的逻辑一致。



## 阶段三

阶段三首先让我了解了bmp图像的存储方式，以及实现将其从二进制文件中读取的方法。



然后是几种搜索方法的实现和使用：

这几种搜素算法都是通过维护open表和close表来实现搜索的，其中open表中记录的是未访问的可达点，close表中记录的是已经访问过的可达点。

算法流程如下：

1.从open表中选出一个节点，并将其从open表中移除

2.将其后继可达节点加入open表

3.将该节点加入close表

算法的核心之一是如何从open表中挑选出下一个访问的节点，这涉及到open表使用何种数据结构：

DFS用栈，BFS用队列，A*算法使用优先队列。

然后close表使用集合（HashSet）存储，这样可以实现判断节点是否存在于close表的时间复杂度为O(1)。

但是我们判断一个新节点是否该加入open表中，要判断其是否处于open表或close表中（当且仅当该新节点为可达节点，且不处于open表或close表中，才能将其加入open表），而open表使用上述几种数据结构查询的时间复杂度都太高，所以这里我们可以将close表改进：close表仍然使用HashSet存储，当一个节点加入到open表的时候就同时加入到close表，不用在其从open表中移除的时候才加入到close表，这样我们就只用查询新节点是否处于close表中（因为这样close表是open表的超集），查询的时间复杂度就是O(1) 。