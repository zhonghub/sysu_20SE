# Vi,Java,Ant和Junit的自学报告



## Vi/Vim

### Vim简介

Vim 被认为是克隆 Vi 编辑器，与 Vi 一样，它也是**以命令为中心**的编辑器。 学习 Vim 的好处之一是——它**随处可用**， 以任何 UNIX 变体为例，例如 Linux、Mac、HP-UX、AIX 等等，Vim 是默认存在的。 Vim 传统上没有 GUI，但现在有一个单独的安装程序叫做 gVim，它提供了 GUI。

### vi/vim 的使用

基本上 vi/vim 共分为三种模式，分别是**命令模式（Command mode）**，**输入模式（Insert mode）**和**底线命令模式（Last line mode）**。 这三种模式的作用分别是：

#### 命令模式：

用户刚刚启动 vi/vim，便进入了命令模式。

此状态下敲击键盘动作会被Vim**识别为命令**，而非输入字符。比如我们此时按下i，并不会输入一个字符，i被当作了一个命令。

以下是常用的几个命令：

- **i** 切换到输入模式，以输入字符。
- **x** 删除当前光标所在处的字符。
- **:** 切换到底线命令模式，以在最底一行输入命令。

若想要编辑文本：启动Vim，进入了命令模式，**按下i，切换到输入模式**。

命令模式只有一些**最基本的命令**，因此仍要依靠底线命令模式输入更多命令。

#### 输入模式

在命令模式下**按下i**就进入了输入模式，在输入模式中，可以使用以下按键：

- **字符按键以及Shift组合**，输入字符
- **ENTER**，回车键，换行
- **BACK SPACE**，退格键，删除光标前一个字符
- **DEL**，删除键，删除光标后一个字符
- **方向键**，在文本中移动光标
- **HOME**/**END**，移动光标到行首/行尾
- **Page Up**/**Page Down**，上/下翻页
- **Insert**，切换光标为输入/替换模式，光标将变成竖线/下划线
- **ESC**，退出输入模式，切换到命令模式

#### 底线命令模式

在命令模式下按下**:（英文冒号）**就进入了底线命令模式。

底线命令模式可以输入单个或多个字符的命令，可用的命令非常多。

在底线命令模式中，基本的命令有（已省略冒号）：

- q 退出程序
- w 保存文件

按ESC键可随时退出底线命令模式。

#### 小结

简单的说，我们可以将这三个模式切换用下图表示：（图片来源：[Linux vi/vim | 菜鸟教程 (runoob.com)](https://www.runoob.com/linux/linux-vim.html)）

<img src="https://www.runoob.com/wp-content/uploads/2014/07/vim-vi-workmodel.png" alt="img" style="zoom:77%;" />   

本次实训阶段一我只初步掌握一些基本的vim操作：

```
进入文件：vim filename（此时进入命令模式）
命令模式->输入模式：输入i
输入模式->命令模式：Esc
命令模式->底线命令模式：输入:
底线命令模式->命令模式：输入回车执行命令或Esc
底线命令模式保存：输入w
底线命令模式退出（退出了vim程序）：输入q
所以可以把三条命令合起来，直接从命令模式保存并退出：输入:wq
```



## Java

### Java简介

Java语法、特性与C/C++非常相似，最大的不同有以下几点：

1. Java 语言**不使用指针**，而是引用。并提供了自动分配内存和垃圾回收机制。

2. Java 丢弃了 C++ 中一些很少使用、很难理解的特性，如操作符重载、多继承（但支持接口之间的多继承）、自动的强制类型转换。
3. **Java 语言是面向对象的：** 虽然C++也面向对象，但是Java语言更是一个纯的面向对象程序设计语言。在Java中，一切都是对象（即类的实例），任何方法、变量都只能在类中（java没有函数，必须是放在一个类class里面的方法），通过对象的实例化来实现各种想要的功能。Java 语言全面支持**动态绑定**，通过关键字override实现覆盖（重写），而 C++语言只对虚函数使用动态绑定。
4. **Java 语言是解释型的：**不同于C/C++这种编译型语言，Java和python这种解释型语言一样，Java 程序在 Java 平台上被编译为**字节码格式**，然后可以在实现这个 Java 平台（**Java虚拟机，Jre**）的任何系统中运行。在运行时，**Java虚拟机**中的 **Java 解释器**对这些字节码进行解释执行，执行过程中需要的类在链接阶段被载入到运行环境中（运行时绑定）。

### Java基础语法

#### 1 常量和变量

**常量**：通常使用关键字final来定义一个常量，如 final int MAX_NUM = 100;

**变量**：

- 静态变量（类变量）：独立于方法之外的变量，用 static 修饰，即使类没有实例化成对象也能调用，所有实例对象共用同一个静态变量。

- 实例变量：独立于方法之外的变量，不过没有 static 修饰，需要将类实例化成对象才能调用。

- 局部变量：类的方法中的变量（注：Java不能在方法中声明静态变量（static），而C++可以）。

  静态变量和实例变量组成这个类的数据域。

  

#### 2 基本数据类型

Java语言提供了八种基本类型。六种数字类型（四个整数型，两个浮点型），一种字符类型，还有一种布尔型：

byte（1字节8位），short（2字节），int（4字节），long（8字节）float（4字节），double（8字节），

char（2字节），bool（1位）

**byte：**

- byte 数据类型是8位、有符号的，以二进制补码表示的整数；
- 最小值是 **-128（-2^7）**；最大值是 **127（2^7-1）**；
- 默认值是 **0**；
- byte 类型用在大型数组中节约空间，主要代替整数，因为 byte 变量占用的空间只有 int 类型的四分之一；
- 例子：byte a = 100，byte b = -50。

**short：**

- short 数据类型是 16 位、有符号的以二进制补码表示的整数
- 最小值是 **-32768（-2^15）**；最大值是 **32767（2^15 - 1）**；
- Short 数据类型也可以像 byte 那样节省空间。一个short变量是int型变量所占空间的二分之一；
- 默认值是 **0**；
- 例子：short s = 1000，short r = -20000。

**int：**

- int 数据类型是32位、有符号的以二进制补码表示的整数；
- 最小值是 **-2,147,483,648（-2^31）**；最大值是 **2,147,483,647（2^31 - 1）**；
- 一般地整型变量默认为 int 类型；
- 默认值是 **0** ；
- 例子：int a = 100000, int b = -200000。

**long：**

- long 数据类型是 64 位、有符号的以二进制补码表示的整数；
- 最小值是 **-9,223,372,036,854,775,808（-2^63）**；最大值是 **9,223,372,036,854,775,807（2^63 -1）**；
- 这种类型主要使用在需要比较大整数的系统上；
- 默认值是 **0L**；
- 例子： **long a = 100000L**，**long b = -200000L**。（"L"理论上不分大小写）

**float：**

- float 数据类型是单精度、32位、符合IEEE 754标准的浮点数；
- float 在储存大型浮点数组的时候可节省内存空间；默认值是 **0.0f**；
- 浮点数不能用来表示精确的值，如货币；
- 例子：float f1 = 234.5f。

**double：**

- double 数据类型是双精度、64 位、符合 IEEE 754 标准的浮点数；
- 浮点数的默认类型为 double 类型；
- double类型同样不能表示精确的值，如货币；
- 默认值是 **0.0d**；

**boolean：**

- boolean数据类型表示一位的信息；
- 只有两个取值：true 和 false；
- 这种类型只作为一种标志来记录 true/false 情况；
- 默认值是 **false**；
- 例子：boolean one = true。

**char：**

- char 类型是一个单一的 16 位 Unicode 字符；
- 最小值是 **\u0000**（十进制等效值为 0）；最大值是 **\uffff**（即为 65535）；
- char 数据类型可以储存任何字符；
- 例子：char letter = 'A';。

说明：

6种数字类型的基本数据类型的默认值都是0，boolean的默认值是false。

值得注意的是：Java中不能用数字来代替boolean类型作为条件判断，不能用0代替false，非0代替true，还得老老实实使用boolean值。

#### 3 语句

基本和C/C++中相同：

**条件语句：**if..else...语句和switch...case...语句

**循环语句：**for循环、while循环、do...while循环，以及判断循环执行的continue（跳过本次循环进入下次循环）和break（跳出循环）

但是Java中新增了**foreach语句**，方便我们对多种数据结构进行遍历（如数组、集合set等），例如：

```Java
int[] data = new int[10];
...对data进行初始化
for(int i = 0; i < data.length ;++i){
	System.out.println(data[i]);
}
for(int x:data){
	System.out.println(x);
}
```

在这两个循环中，foreach循环中的x的值就等于for循环的data[i]，但是，值得注意的是，变量x只是对data[i]的值的拷贝，对x的任何操作都不会影响到data[i]。



#### 4 数组

1. java数组是一个**对象**，而C++里数组是补充类型，要按照对象的方式初始化（new）：

所以我们不能直接 int data[8];

而是要先声明int data[];再初始化data = **new** int[8];

**或声明和初始化放一起，示例：**

int data[] = new int[8];

int rnds[] = new int[]{1,3,4,5,6};

int nums[] = {9, -10, 18, -978, 9, 287, 49, 7};

char[] chars = {'我', '是', '中', '大', '人'};

double map[\][\]= new double[3][10\];

2. java中只有一维数组，二维数组为一维数组的一维数组（每个元素都是一个对象，引用类型）：

因此每个数组大小可以不同，例如：

int table[][] = {{1},{2,3,4},{5,6,7,8}}; 

数组通过length属性访问长度，如：table.length， table[i].length



#### 5 字符串类String

字符串类型(String)为一个用于文字操作的类，其值为一串字符，采用Unicode编码存储，常用方法：

**判断字符串是否相等：**

== 看指针指向的对象是否为同一对象

.equals() 只看对象内容

.equalsIgnoreCase(“hello”); // 相等比较，忽略大小写

**判断字符串是否为空：**

.isEmpty()

.equals("")

**字符串的长度：**

.length()

**数值变量转化为字符串：**

String f0 = **String.valueOf**(100.3f); // 将浮点数转换为字符串

**""+**100.3f //更常用

**字符串转数值类型变量：**

double f1 = Double.parseDouble("100.3"); // 将字符串转换为Double数

**整数变字符串**： ""+int

**注意：**

**String**是不可变的对象，每次修改其内容都会生成了一个新的 String 对象，再从堆区分配空间。

当对字符串进行修改的时候，需要使用 StringBuffer（单线程） 和 StringBuilder（多线程） 类。和 String 类不同的是，StringBuffer 和 StringBuilder 类的对象能够被多次的修改，并且不产生新的未使用对象。



#### 6 OO三特性：封装、继承、多态性 相关：

**重载和重写**

（参数不同）重载overload（不能根据返回值不同类型来定义重载）—>编译时绑定

（参数完全相同）覆盖/重写@override—>运行时绑定，导致多态性

**子类中调用父类的方法**

调用父类（含以上）中的方法：supper.fun1()

**向上类型转换（转换为父类）**

 Father f = new Son();// 只能调用父类中有的方法

**子类重写检测**

在子类覆盖的方法前加上@Override，则会让编译器检查父类是否有这个方法：如果父类没有则会报错， 否则不会检查。

**抽象方法**

只有方法头，没有实现，由子类重写，方法声明前面加abstract关键字。

**抽象类**

含有抽象方法的类，类前面加abstract关键字。由于抽象类不能实例化对象，所以抽象类必须被继承，才能被使用。也是因为这个原因，通常在设计阶段决定要不要设计抽象类。

**接口类**

所有方法都是抽象方法，极端的一种抽象类，以下为其声明和实现的格式：

```Java
//声明
[可见度] interface 接口名称 [extends 其他的接口名] {
        // 声明变量
        // 抽象方法
}
//实现
[可见度] class 实现名称 implements 接口名称[其他接口名称, 其他接口名称..., ...] ...
// 使用匿名子类实现，下面定义了一个接口Door的匿名子类。 
Door door = new Door(){ 
	@Override public void open(){
	//回调函数 System.out.println("open anonymous door!"); 
	}
	@Override public void close(){
	//回调函数 System.out.println("close anonymous door!"); 
	}
};

```

- 接口是隐式抽象的，当声明一个接口的时候，不必使用**abstract**和**class**关键字。
- 接口中每一个方法也是隐式抽象的，声明时同样不需要**abstract**关键字。
- 接口中的方法都是公有的。



#### 7 final关键字（类似const）

final的类不能被继承。

final数据：常量，不能被再次赋值。

定义为final的方法不能被覆盖（@Override）。

如果定义为final的数据域是引用型（类）的，其对象的数据域的内容是可以被修改的。



#### 8 包（package）

C++的库：lib静态（编译时绑定），dll动态（运行时绑定）

java的包：一个子目录下的所有class文件形成一个包（package）。（包里的文件都是编译好的.class文件）

也可以把它们连同子目录结构放到一个jar文件中（即打包成一个jar包）。

jar包就是Java的库文件。

我们可以在类定义时，声明其所属包：package pkg1[．pkg2[．pkg3…]];

由此而来，产生了访问权限的问题：

**4种访问权限**：（private，public，protected，无修饰符（在同一个包里））

同一个包：除private都能访问

不同包：只能访问public

如果是子类：至少可以访问public和protected



## Ant

### Ant简介

Ant是Unix的**Make**构建工具的更好**替代品**，因此使用和Make非常相似。 Ant是用Java编写的，需要JVM来构建Java项目。Ant使用XML来描述构建代码，默认情况下，它的XML文件名是`build.xml`。

### Ant元素

Ant通常含有4种元素：project项目标签，target目标标签，task任务标签，property属性标签

### Ant编写语法

Ant使用XML来编写构建文件，每个构建文件包含一个项目project和至少一个默认目标。 `target`是任务task的容器，每个任务都是可以执行的代码。 可以将项目理解为将目标和任务包装到单个单元中的容器，所以：每个项目拥有1个project项目标签，这个project项目标签下可以有多个target目标标签和property属性标签，每个target目标标签可以有多个task任务标签。

#### project项目

我们可以使用`<project>`标记创建项目，它既包括目标也包括任务。

**常用属性：**

`name` 这是该项目的名称，非必需。  

`default` 如果没有明确提供目标，它用于设置默认执行的目标， 非必需。  

`basedir` 它需要基目录路径，非必需。

#### target目标

目标target是一个或多个任务task的集合。 任务是一段代码，即将被执行。 构建文件包含一个项目，在项目内部声明了所有目标。 要创建目标，可以使用`<target>`标记。

目标可以依赖于其他目标，并且依赖目标必须在当前目标之前执行。 例如：可能有两个目标:一个编译目标，另一个用于运行代码。 只有在执行编译目标后才能运行目标，因此运行目标取决于编译目标。

**常用属性**

name 要设置目标的名称（必需）

depends 它所依赖的目标列表（非必需）

if 一个计算结果为true的属性（非必需）

unless 一个计算结果为false的属性（非必需）

description 这个目标函数的简短描述（非必需）

extensionOf 将当前目标添加到扩展点的从属列表（非必需）

onMissingExtensionPoint 如果此目标扩展了缺少的扩展点，该如何处理（非必需）

#### task任务

任务是一段可以执行的代码。 任务可以具有多个属性，每个任务都具有共同的结构。 常见结构由任务名称，属性等组成。

任务分为两类:内置任务和用户定义的任务。

#### 常见的内置任务有：

##### 2.1. 存档任务

用于压缩和解压缩数据的任务称为归档任务。下面列出了一些常见的内置存档任务。

| 任务名称 | 描述                              |
| -------- | --------------------------------- |
| Ear      | Jar任务的扩展，对文件进行特殊处理 |
| Jar      | 一组文件                          |
| Tar      | 创建tar存档                       |
| Unjar    | 解压缩jar文件                     |
| Untar    | 解压tarfile                       |
| Unwar    | 解压缩warfile                     |
| Unzip    | 解压缩zip文件                     |
| War      | Jar任务的扩展                     |

##### 2.2. 审计任务

| 任务名称 | 描述                    |
| -------- | ----------------------- |
| JDepend  | 它用于调用JDepend解析器 |

##### 2.3. 编译任务

用于编译源文件的任务称为编译任务，下面列出了一些常见的内置编译任务。

| 任务名称 | 描述                       |
| -------- | -------------------------- |
| Depend   | 确定哪些类文件的资源已过期 |
| Javac    | 编译源文件                 |
| JspC     | 运行JSP编译器              |
| NetRexxC | 编译NetRexx源文件          |
| Rmic     | 运行rmic编译器             |

##### 2.4. 执行任务

用于执行运行应用程序的任务称为执行任务。下面列出了一些常见的内置执行任务。

| 任务名称 | 描述                             |
| -------- | -------------------------------- |
| Ant      | 在指定的构建文件上运行Ant        |
| AntCall  | 在同一个构建文件中运行另一个目标 |
| Apply    | 执行系统命令                     |
| Java     | 执行Java类                       |
| Parallel | 可包含其他ant任务的容器任务      |
| Sleep    | 按指定的时间暂停执行             |

##### 2.5. 文件任务

与句柄文件操作相关的任务称为文件任务。下面列出了一些常见的内置文件任务。

| 任务名称 | 描述                 |
| -------- | -------------------- |
| Chmod    | 更改文件的权限       |
| Chown    | 更改文件的所有权     |
| Concat   | 连接多个文件         |
| Copy     | 将文件复制到新目的地 |
| Delete   | 删除文件             |
| Mkdir    | 创建一个目录         |

由于本次实验使用内置任务即可完成，所以暂未学习自定义任务的实现。

#### property属性

属性是**键值对**，其中每个值都与键相关联。属性用于设置可在构建文件中的任何位置访问的值。 设置属性后，无法更改。

Ant提供了`<property>`标记，可用于设置属性。

Ant属性类型有两种:内置属性，用户定义的属性。

### Ant使用

在build.xml编写完成后，在build.xml所在文件夹目录下：

输入ant，执行默认目标；

输入ant targetname，执行对应**目标target**。

和make用法非常相似，如ant，ant run，ant clean。

#### 我的build.xml

见最后的Ant+Junit的组合使用。



## Junit

### Junit简介

JUnit 是一个 Java 编程语言的单元测试框架。JUnit 在测试驱动的开发方面有很重要的发展，是起源于 JUnit 的一个统称为 xUnit 的单元测试框架之一。

### 使用Junit的好处

1. 可以书写一系列的测试方法，对项目所有的接口或者方法进行单元测试。
2. 启动后，自动化测试，并判断执行结果, 不需要人为的干预。
3. 只需要查看最后结果，就知道整个项目的方法接口是否通畅。
4. 每个单元测试用例相对独立，由Junit 启动，自动调用。不需要添加额外的调用语句。
5. 添加，删除，屏蔽测试方法，不影响其他的测试方法。 开源框架都对JUnit 有相应的支持。

### Junit使用

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

#### JUnit 注解

用于放在测试类的方法前的关键字:

1. `@Test`:这个注释说明依附在 JUnit 的 public void 方法可以作为一个**测试案例。**
2. `@Before`:有些测试在运行前需要创造几个相似的对象。在 public void 方法加该注释是因为该方法需要在 test 方法前运行。
3. `@After`:如果你将外部资源在 Before 方法中分配，那么你需要在测试运行后释放它们。在 public void 方法加该注释是因为该方法需要在 test 方法后运行。
4. `@BeforeClass`:在 public void 方法加该注释是因为该方法需要在类中所有方法前运行。
5. `@AfterClass`:它将会使方法在所有测试结束后执行。这个可以用来进行清理活动。
6. `@Ignore`:这个注释是用来忽略有关不需要执行的测试的。

@Before和@After会在每个@Test前、后都执行一次，而@BeforeClass和@AfterClass只会执行一次。

#### JUnit 加注解执行过程

- `beforeClass()`: 方法首先执行，并且只执行一次。
- `afterClass()`:方法最后执行，并且只执行一次。
- `before()`:方法针对每一个测试用例执行，但是是在执行测试用例之前。
- `after()`:方法针对每一个测试用例执行，但是是在执行测试用例之后。
- 在 before() 方法和 after() 方法之间，执行每一个测试用例。

#### JUnit 执行测试

测试用例是使用 JUnitCore 类来执行的。JUnitCore 是运行测试的外观类。要从命令行运行测试，可以运行`java org.junit.runner.JUnitCore`。对于只有一次的测试运行，可以使用静态方法 `JunitCore.runClasses(Class[])`。

#### JUnit 套件测试

测试套件意味着捆绑几个单元测试用例并且一起执行它们，通过这样的方式，我们就可以一次运行多个测试。

在 JUnit 中，`@RunWith`和`@Suite`注释用来运行套件测试:

建一个TestSuite类

```Java
import org.junit.runner.RunWith;
import org.junit.runners.Suite;

@RunWith(Suite.class)
@Suite.SuiteClasses({
	TestXX1.class;
	TestXX2.class;
})
public class TestSuite{

}
```

然后通过JunitCore.runClasses( TestSuite.class)就可以一次运行多个测试。

#### 我的Calculator的Junit测试类

```Java
package test;

import static org.junit.Assert.*;
import org.junit.Test;
import org.junit.BeforeClass;
import org.junit.AfterClass;
import main.Calculator;

public class TestCalculator {
	private Calculator Calculator = new Calculator();
	private double l;
	private double r;

	public TestCalculator() {
		l = 12;
		r = 4;
	}

	@BeforeClass
	public static void setUpBeforeClass() {
		// System.out.println("begin test\n");
	}

	@AfterClass
	public static void tearDownAfterClass() {
		// System.out.println("\nend test\n");
	}

	// 测试加法函数
	@Test
	public void testAdd() {
		String result = l + r + "";
		assertEquals(result, Calculator.calAdd(l, r));
	}

	// 测试减法函数
	@Test
	public void testSub() {
		String result = l - r + "";
		assertEquals(result, Calculator.calSub(l, r));
	}

	// 测试乘法函数
	@Test
	public void testMul() {
		String result = l * r + "";
		assertEquals(result, Calculator.calMul(l, r));
	}

	// 测试除法函数，除以非0
	@Test
	public void testDev1() {
		String result = l / r + "";
		assertEquals(result, Calculator.calDev(l, r));
	}

	// 测试除法函数，除0
	@Test
	public void testDev2() {
		r = 0;
		String result = "error";
		assertEquals(result, Calculator.calDev(l, r));
	}

}

```



## Ant + Junit

通过Ant和Junit的组合使用，就能实现自动化的单元测试。

我的HelloWorld的build.xml，Calculator的build.xml和这类似，就不再赘述。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project name="HelloWorld" basedir="." default="test2">
	<!-- 源代码src路径 -->
	<property name="src.path" value="src/main" />
	<!-- 编译文件class路径 -->
	<property name="build.path" value="build" />
	<!-- 单元测试代码路径 -->
	<property name="test.path" value="src/test" />
	<property name="jarfile" value="${build.path}/*.jar" />

	<path id="classpath.base"/>
	<path id="compile.path">
		<pathelement location="lib/junit4.jar" />
		<pathelement location="lib/hamcrest-core-1.3.jar" />
		<pathelement location="${build.path}/classes"/>
		<!-- 下句在进行jar打包时可替换上句 
		<pathelement location="${build.path}/ht.jar" />
		-->
		<path refid="classpath.base" />
	</path>

	<target name="clean" description="清除所有编译生成的文件及生成的jar包">
		<echo> 清除build及其目录下的class文件! </echo>
		<delete dir="${build.path}"/>
		<delete dir="lib/ht.jar"/>
	</target>

	<target name="compile" depends="clean" description="编译main包">
		<echo> 编译main包! </echo>
		<mkdir dir="${build.path}/classes" />
		<javac includeantruntime="false" srcdir="${src.path}" destdir="${build.path}/classes" classpathref="compile.path" />
	</target>

	<target name="compile2" depends="compile" description="编译test包">
		<echo> 编译test包! </echo>
		<javac includeantruntime="false" srcdir="${test.path}" destdir="${build.path}/classes">
			<classpath refid="compile.path" />
		</javac>
	</target>

	<target name="run" depends="compile" description="运行main.HelloWorld">
		<echo> Run main.HelloWorld </echo>
		<java classname="main.HelloWorld">
			<classpath path="${build.path}/classes" />
		</java>
		<echo> Run结束! </echo>
	</target>
	
	<target name="test" depends="compile2" description="测试HelloWorld">
		<echo> JUnit单元测试test.TestHelloWorld! </echo>
		<junit printsummary="true" fork="yes">
			<classpath refid="compile.path" />
			<formatter type="brief" usefile="false" />
			<test name="test.TestHelloWorld" />
			<!--<classpath path="${build.path}"-->
		</junit>
		<echo> test.TestHelloWorld结束! </echo>
	</target>

	<!-- 打包 -->
	<target name="jar" depends="compile2" description="打包成jar包">
		<jar destfile="${build.path}/ht.jar" basedir="${build.path}/classes"/>
	</target>

</project>
```

