package project1;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.WindowConstants;
import javax.swing.JOptionPane;

import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;

public class ClientMainFrame extends JFrame {
    private static final long serialVersionUID = 1L;
    // 服务器ip
    public String host = "localhost"; // "172.26.55.101"
    // 服务器端口号
    public int port = 8000;
    public boolean isRegister = false;
    private Socket socket;

    private final int LEFT_POS = 40;
    private final int INPUT_WIDTH = 360;
    private final int MIDDLE_POS = 260;
    private String userName = "未登录";
    private ClientMainFrame main;
    private JTextField txtSend;
    private JTextArea txtaReceive;

    ClientMainFrame() {
        this.setSize(600, 500); // 设置width和height
        this.setLocationRelativeTo(null); // 居屏幕中间
        this.setLayout(null); // 空布局，可以准确的定位组件在容器中的位置和大小
        this.setTitle("客户端: 登录用户:" + getUserName() + "  端口:" + port + "  host:" + host);
        main = this;

        txtSend = new JTextField("Hello World!", 30); // 初值，列数
        JLabel mainLab = new JLabel("客户端主窗口");
        JLabel nameLab = new JLabel("消息:");
        mainLab.setBounds(MIDDLE_POS, 10, 80, 25);
        nameLab.setBounds(LEFT_POS, 40, 40, 20); // 设置矩形大小(矩形左上角横坐标x,矩形左上角纵坐标y，矩形长度，矩形宽度)
        txtSend.setBounds(LEFT_POS + 60, 40, INPUT_WIDTH, 20); // left,top,width,height
        txtSend.setBorder(BorderFactory.createLineBorder(new Color(128, 128, 128)));// 设置边界颜色：RedGreenBlue(0~255)
        // txtSend.setBackground(Color.BLUE);// 设置背景色
        txtSend.setForeground(Color.RED); // 设置前景色
        this.add(mainLab);// 在当前窗口(JFrame)中增加控件
        this.add(nameLab);
        this.add(txtSend);

        // 在文本框上添加滚动条
        txtaReceive = new JTextArea();
        JScrollPane jsp = new JScrollPane(txtaReceive);
        jsp.setBounds(LEFT_POS + 60, 90, INPUT_WIDTH, 300);
        jsp.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);// 默认的设置是超过文本框才会显示滚动条，以下设置让滚动条一直显示
        jsp.setAutoscrolls(true);
        this.add(jsp);

        // 设置按钮
        this.setJMenuBar(addMenu(this));
        addSendBtn();

        this.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                exit(); // 点击窗口右上角X关闭时的事件
            }
        });

        this.setVisible(true);
        this.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);
    }

    /**
     * 从服务器读取历史消息
     */
    void readAllMsg() {
        // txtaReceive.setText("");
        String sendStr = "a" + "#" + "a" + "#" + "a";
        try {
            socket = new Socket(host, port); // 与服务器 建立连接。
            DataInputStream fromServer = new DataInputStream(socket.getInputStream());
            DataOutputStream toServer = new DataOutputStream(socket.getOutputStream());
            toServer.writeUTF(sendStr);// 发送数据
            String recv = fromServer.readUTF(); // 接收数据
            txtaReceive.setText(recv);
            fromServer.close();
            toServer.close();
            socket.close();
        } catch (Exception e1) {
        }
    }

    /**
     * 从服务器不断读取历史消息，每次读取时隔5000ms
     */
    void receiveFromServer() {
        new Thread() {
            @Override
            public void run() {
                while (isRegister) {
                    try {
                        readAllMsg();
                        Thread.sleep(5000);
                    } catch (Exception e1) {
                    }
                }
            }
        }.start();
    }

    /**
     * @param userName
     * 
     * @apiNote 修改当前用户名为userName
     */
    void setUserName(String userName) {
        this.userName = userName;
    }

    String getUserName() {
        return this.userName;
    }

    /**
     * @param userName
     * @param msg
     * @param time
     * 
     * @apiNote 接收编辑框增加一条记录
     */
    void addMsg(String userName, String msg, String time) {
        txtaReceive.append(time + "  \r" + userName + ":  \r" + msg + "\r\n"); // 加到末尾
    }

    void addMsg(String str) {
        String[] s = str.split("#");
        txtaReceive.append(s[3] + "  \r" + s[1] + ":  \r" + s[2] + "\r\n");
    }

    /**
     * @param s1 host
     * @param i  端口号
     * @apiNote 设置host和端口号
     */
    public void setHostPort(String s1, int i) {
        host = s1;
        port = i;
    }

    /**
     * @apiNote 设置“发布”按钮，并绑定事件
     */
    private void addSendBtn() {
        JButton btnTest = new JButton("发布");
        btnTest.setBounds(LEFT_POS + 60 + INPUT_WIDTH + 20, 40, 60, 20);
        this.add(btnTest);

        ActionListener al = new ActionListener() { // 加上按键事件
            @Override
            public void actionPerformed(ActionEvent e) {
                // new SubFrame(main);// 客户端子窗口
                if (!isRegister) {
                    JOptionPane.showMessageDialog(null, "请先登录！");
                    return;
                }
                String msg = txtSend.getText().trim();
                if (msg.isEmpty()) {
                    JOptionPane.showMessageDialog(null, "消息不能为空！");
                    return;
                }
                // 发送 -- 0+"#"+用户名+"#"+消息
                String sendStr = 0 + "#" + userName + "#" + msg;
                // 建立连接、发送数据、接收数据、关闭连接。
                try {
                    socket = new Socket(host, port); // 与服务器 建立连接。
                    DataOutputStream toServer = new DataOutputStream(socket.getOutputStream());
                    DataInputStream fromServer = new DataInputStream(socket.getInputStream());
                    toServer.writeUTF(sendStr);// 发送数据
                    String recv = fromServer.readUTF(); // 接收数据
                    System.out.println("send= " + sendStr);
                    System.out.println("recv= " + recv);
                    // addMsg(sendStr);
                    toServer.close();
                    socket.close(); // 关闭连接
                    // readAllMsg();
                } catch (Exception e1) {
                    e1.printStackTrace();
                }
            }
        };
        btnTest.addActionListener(al);
    }

    /**
     * @param jf
     * @return 返回一个菜单栏
     * @apiNote 给菜单栏设置按钮，并给按钮绑定事件：
     *          注册，登录，设置，退出登录，退出系统
     */
    JMenuBar addMenu(JFrame jf) {
        JMenuBar jmenu = new JMenuBar(); // 创建菜单
        jf.setJMenuBar(jmenu); // 不能设定位置，会自动放在最上部

        // 添加菜单
        JMenu menu1 = new JMenu(" 文件");
        JMenu menu2 = new JMenu(" 帮助");
        JMenuItem item1 = new JMenuItem(" 注册");
        JMenuItem item2 = new JMenuItem(" 登录");
        JMenuItem item5 = new JMenuItem(" 设置");
        JMenuItem item3 = new JMenuItem(" 退出登录");
        JMenuItem item4 = new JMenuItem(" 退出系统");

        // 添加菜单项至菜单上
        menu1.add(item1);
        menu1.add(item2);
        menu1.add(item5);
        menu1.add(item3);
        menu1.add(item4);

        jmenu.add(menu1);
        jmenu.add(menu2);

        ActionListener al = new ActionListener() { // 定义菜单点击事件
            @Override
            public void actionPerformed(ActionEvent e) {
                String str = e.getActionCommand();
                if (" 注册".equals(str)) {
                    if (main.isRegister) {
                        JOptionPane.showMessageDialog(null, "请先退出登录！");
                        return;
                    }
                    register();
                } else if (" 登录".equals(str)) {
                    if (main.isRegister) {
                        JOptionPane.showMessageDialog(null, "请先退出登录！");
                        return;
                    }
                    logIn();
                } else if (" 退出登录".equals(str)) {
                    JOptionPane.showMessageDialog(null, "退出登录");
                    logOut();
                } else if (" 退出系统".equals(str)) {
                    exit();
                } else if (" 设置".equals(str)) {
                    // JOptionPane.showMessageDialog(null, "设置");
                    set();
                }
            }
        };
        item1.addActionListener(al); // 菜单项加上点击事件
        item2.addActionListener(al);
        item3.addActionListener(al);
        item4.addActionListener(al);
        item5.addActionListener(al);

        return jmenu;
    }

    /**
     * @apiNote 退出客户端系统
     */
    void exit() {
        if (isRegister) {
            isRegister = false;
            String sendStr = 3 + "#" + userName + "#quit";
            // 建立连接、发送数据、接收数据、关闭连接。
            try {
                socket = new Socket(host, port); // 与服务器 建立连接。
                DataOutputStream toServer = new DataOutputStream(socket.getOutputStream());
                toServer.writeUTF(sendStr);// 发送数据
                toServer.close();
                socket.close(); // 关闭连接
            } catch (Exception e1) {
                // e1.printStackTrace();
            }
        }
        System.exit(0); // 退出系统。不会触发windowClosing事件
    }

    /**
     * @apiNote 登录, 生成一个子窗口
     */
    void logIn() {
        new ClientSubFrame(main, 2);
    }

    /**
     * @apiNote 注册, 生成一个子窗口
     */
    void register() {
        new ClientSubFrame(main, 1);
    }

    /**
     * @apiNote 设置host和por, 生成一个子窗口
     */
    void set() {
        new ClientSubFrame(main, 3);
    }

    /**
     * @apiNote 退出登录
     */
    void logOut() {
        if (isRegister) {
            String sendStr = 3 + "#" + userName + "#quit";
            // 建立连接、发送数据、接收数据、关闭连接。
            try {
                socket = new Socket(host, port); // 与服务器 建立连接。
                DataOutputStream toServer = new DataOutputStream(socket.getOutputStream());
                toServer.writeUTF(sendStr);// 发送数据
                toServer.close();
                socket.close(); // 关闭连接
                // txtSend.setText("");
            } catch (Exception e1) {
                // e1.printStackTrace();
            }
        }
        userName = "未登录";
        isRegister = false;
        txtSend.setText("Hello World!");
        txtaReceive.setText("");
        this.setTitle("客户端: 登录用户:" + getUserName() + "  端口:" + port + "  host:" + host);
    }

}