# readme.md

## 文件目录

```
 ├── HelloWorld
 │   └── src // 源代码文件夹
 |		  └── main     // 主程序包
 │   	  └── test 	   // 测试类包
 │   └── build 		// 生成类/jar包文件夹（ant编译后才有）
 │   		└── classes  // 生成类文件夹
 │   		└── *.jar    // 生成jar包
 │   └── lib 		// 编译运行所需类库
 │   └── build.xml	// Ant 自动编译XML文件
 │   └── sonar-project.properties // Sonar 代码评估配置文件
 ├── Calculator
 │   └── src // 源代码文件夹
 |		  └── main     // 主程序包
 │   	  └── test 	   // 测试类包
 │   └── build 		// 生成类/jar包文件夹（ant编译后才有）
 │   		└── classes  // 生成类文件夹
 │   		└── *.jar    // 生成jar包
 │   └── lib 		// 编译运行所需类库
 │   └── build.xml	// Ant 自动编译XML文件
 │   └── sonar-project.properties // Sonar 代码评估配置文件
 ├── README.md
```

## HelloWorld

### **程序功能：**

HelloWorld.java  main函数调用out方法在终端输出“Hello World!”

TestHelloWorld.java  测试HelloWorld的out方法

### **Ant执行：**

进入HelloWorld目录下

编译主程序main包：ant  compile

编译主程序main包和测试类包test包：ant  compile2

运行主程序：ant run （设置了依赖条件，可直接运行）

运行单元测试：ant test （设置了依赖条件，可直接运行）

将生成的class文件打包成jar包：ant jar

清除生成的所有文件（在build目录下）：ant clean



## Calculator

### **程序功能：**

Calculator.java  简单的计算器小程序

MainClass.java 主函数类，实例化Calculator运行

TestCalculator.java  测试Calculator的运算方法

### **Ant执行：**

进入Calculator目录下

编译主程序main包：ant  compile

编译主程序main包和测试类包test包：ant  compile2

运行主程序：ant run （设置了依赖条件，可直接运行，但在ant下不能出现计算器小程序的图形界面）

单元测试：ant test （设置了依赖条件，可直接运行）

将生成的class文件打包成jar包：ant jar

清除生成的所有文件（在build目录下）：ant clean

**注意：**

使用ant导致程序直接运行结束，并不能显示出计算器小程序的图形界面，所以不能通过ant run直接运行，

而是在Calculator目录下：先执行：ant compile

再执行：java -classpath .:build/classes main.MainClass