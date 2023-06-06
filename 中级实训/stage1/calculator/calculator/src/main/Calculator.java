package main;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.border.TitledBorder;

public class Calculator {
    private JFrame mainFrame;// 主界面
    private JButton btns[];// 5个运算按钮按钮
    private JLabel labels[];// 3个label分辨显示:运算符，等于号，结果
    private JTextField inputText[];// 左右两个操作数

    public Calculator() {
        mainFrame = new JFrame("简单计算器");
        // 界面布局设置
        mainFrame.setLayout(new GridLayout(2, 5, 10, 10));
        mainFrame.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
        mainFrame.setVisible(true);
        // 初始化界面元素：btns，labels，inputText
        setUI();
        // 给按钮绑定事件
        setBtn();
        // 将界面元素btns，labels，inputText添加到主界面
        mainFrame.add(inputText[0]);
        mainFrame.add(labels[0]);
        mainFrame.add(inputText[1]);
        mainFrame.add(labels[1]);
        mainFrame.add(labels[2]);
        for (JButton x : btns) {
            mainFrame.add(x);
        }
        // 界面大小自适应
        mainFrame.pack();
        // 界面规模和位置
        mainFrame.setSize(600, 400);
        mainFrame.setLocation(600, 300);
    }

    // 初始化界面元素：btns，labels，inputText的size、文字
    private void setUI() {
        btns = new JButton[5];
        labels = new JLabel[3];
        inputText = new JTextField[2];
        // 设置inputText
        for (int i = 0; i < 2; ++i) {
            inputText[i] = new JTextField("12", JTextField.CENTER);
            inputText[i].setHorizontalAlignment(JTextField.CENTER);
            inputText[i].setSize(100, 100);
        }
        inputText[1].setText("2");
        // 设置labels
        TitledBorder border = new TitledBorder(" ");
        for (int i = 0; i < 3; ++i) {
            labels[i] = new JLabel("", JLabel.CENTER);
            labels[i].setHorizontalAlignment(JLabel.CENTER);
            labels[i].setBorder(border);
            labels[i].setSize(100, 100);
        }
        labels[1].setText("=");
        // 设置btns
        final String[] btnStr = { "+", "-", "*", "/", "OK" };
        for (int i = 0; i < 5; ++i) {
            btns[i] = new JButton(btnStr[i]);
            btns[i].setSize(100, 100);
        }
    }

    // 给运算符按钮绑定事件
    private void setBtn() {
        // 加减乘除4个按钮的事件，改变label操作符的text文本
        for (int i = 0; i < 4; ++i) {
            switch (i) {
                case 0:
                    btns[i].addActionListener(new ActionListener() {
                        // 加号
                        @Override
                        public void actionPerformed(ActionEvent e) {
                            labels[0].setText("+");
                        }
                    });
                    break;
                case 1:
                    btns[1].addActionListener(new ActionListener() {
                        // 减号
                        @Override
                        public void actionPerformed(ActionEvent e) {
                            labels[0].setText("-");
                        }
                    });
                    break;
                case 2:
                    btns[2].addActionListener(new ActionListener() {
                        // 乘号
                        @Override
                        public void actionPerformed(ActionEvent e) {
                            labels[0].setText("*");
                        }
                    });
                    break;
                case 3:
                    btns[3].addActionListener(new ActionListener() {
                        // 除号
                        @Override
                        public void actionPerformed(ActionEvent e) {
                            labels[0].setText("/");
                        }
                    });
                    break;
                default:
                    break;
            }
        }
        // 等于号，进行运算
        btns[4].addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                double left = Double.parseDouble(inputText[0].getText());
                double right = Double.parseDouble(inputText[1].getText());
                // 进行相应的运算
                switch (labels[0].getText()) {
                    case "+":
                        labels[2].setText(calAdd(left, right));
                        break;
                    case "-":
                        labels[2].setText(calSub(left, right));
                        break;
                    case "*":
                        labels[2].setText(calMul(left, right));
                        break;
                    case "/":
                        labels[2].setText(calDev(left, right));
                        break;
                    default:
                        labels[2].setText("error");
                }
            }
        });
    }

    // 加法结果
    public String calAdd(double r, double l) {
        return r + l + "";
    }

    // 减法结果
    public String calSub(double r, double l) {
        return r - l + "";
    }

    // 乘法结果
    public String calMul(double r, double l) {
        return r * l + "";
    }

    // 除法结果
    public String calDev(double r, double l) {
        // 除0
        if (Double.toString(l).equals(Double.toString(0.0d))) {
            return "error";
        }
        return r / l + "";
    }

    public void run() {
        // System.out.println("running");
    }

}