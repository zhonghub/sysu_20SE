package main;

public class MainClass {
    public MainClass() {
        // System.out.println("Running Calculator:");
    }

    // 主函数,用于运行Calculator()
    public static void main(String[] args) {
        Calculator Calculator = new Calculator();
        Calculator.run();
    }
}