package main;

public class HelloWorld {
	private HelloWorld() {
	}

	// 主函数main
	public static void main(String[] args) {
		out();
	}

	// 用于测试Junit的方法
	public static String out() {
		String str = "Hello World!";
		// 输出实际结果
		System.out.println(str);
		return str;
	}
}
