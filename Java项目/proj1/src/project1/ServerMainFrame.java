package project1;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

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
import java.util.ArrayList;

// 服务器窗口
public class ServerMainFrame extends JFrame {
    private JFrame jf;
    public boolean isUsing = true;

    private static final long serialVersionUID = 1L;

    private final int LEFT_POS = 10;
    private final int INPUT_WIDTH = 370;
    private final int MIDDLE_POS = 270;

    private ServerMainFrame main;
    private JTextArea txtaReceive;
    private JTextArea txtaUser;
    // 服务器监听端口号
    private int port = 8000;// 8000

    public ServerMainFrame() {
        this.setSize(600, 500); // 设置width和height
        this.setLocationRelativeTo(null); // 居屏幕中间
        this.setLayout(null); // 空布局，可以准确的定位组件在容器中的位置和大小
        this.setTitle("服务器:未绑定端口");
        jf = this;
        main = this;

        JLabel mainLab = new JLabel("服务器");
        mainLab.setBounds(MIDDLE_POS, 10, 60, 25);
        this.add(mainLab);// 在当前窗口(JFrame)中增加控件

        // 消息框，在文本框上添加滚动条
        txtaReceive = new JTextArea();
        JScrollPane jsp = new JScrollPane(txtaReceive);
        jsp.setBounds(LEFT_POS + 10, 60, INPUT_WIDTH, 300);
        jsp.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);// 默认的设置是超过文本框才会显示滚动条，以下设置让滚动条一直显示
        jsp.setAutoscrolls(true);
        this.add(jsp);

        // 登录用户框
        txtaUser = new JTextArea();
        JScrollPane jsp2 = new JScrollPane(txtaUser);
        jsp2.setBounds(LEFT_POS + 70 + INPUT_WIDTH, 60, 110, 300);
        jsp2.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);// 默认的设置是超过文本框才会显示滚动条，以下设置让滚动条一直显示
        jsp2.setAutoscrolls(true);
        this.add(jsp2);

        // 添加菜单栏
        addMenu(jf);

        // 点击窗口右上角X关闭时的事件
        this.addWindowListener(new WindowAdapter() {
            public void windowClosing(WindowEvent e) {
                exit(); 
            }
        });

        this.setVisible(true);
        this.setDefaultCloseOperation(WindowConstants.EXIT_ON_CLOSE);

    }

    void exit() {
        jf.setVisible(false);
        jf.dispose();
        isUsing = false;
        System.exit(0); // 退出系统。不会触发windowClosing事件
    }

    JMenuBar addMenu(JFrame jf) {
        JMenuBar jmenu = new JMenuBar(); // 创建菜单
        jf.setJMenuBar(jmenu); // 不能设定位置，会自动放在最上部

        // 添加菜单
        JMenu menu1 = new JMenu(" 文件");
        JMenu menu2 = new JMenu(" 帮助");
        JMenuItem item1 = new JMenuItem(" 绑定端口");
        JMenuItem item2 = new JMenuItem(" 解除绑定");
        JMenuItem item3 = new JMenuItem(" 退出");

        // 添加菜单项至菜单上
        menu1.add(item1);
        menu1.add(item2);
        menu1.add(item3);

        jmenu.add(menu1);
        jmenu.add(menu2);

        ActionListener al = new ActionListener() { // 定义菜单点击事件
            @Override
            public void actionPerformed(ActionEvent e) {
                String str = e.getActionCommand();
                if (" 绑定端口".equals(str)) {
                    new ServerSubFrame(main);
                } else if (" 解除绑定".equals(str)) {
                    if (port == -1) {
                        JOptionPane.showMessageDialog(null, "请先绑定端口");
                    } else {
                        port = -1;
                        main.setTitle("服务器:未绑定端口");
                        JOptionPane.showMessageDialog(null, "解绑成功");
                    }
                } else if (" 退出".equals(str)) {
                    exit();
                }
            }
        };
        item1.addActionListener(al); // 菜单项加上点击事件
        item2.addActionListener(al);
        item3.addActionListener(al);

        return jmenu;
    }

    private class ServerSubFrame extends JFrame {
        private static final long serialVersionUID = 1L; // 本语句用于序列化，可以不要
        // 输入框
        private JTextField txtPort;
        private JFrame jf;

        public ServerSubFrame(ServerMainFrame main) {
            this.setSize(400, 300); // 设置width和height
            this.setLocationRelativeTo(null); // 居屏幕中间
            this.setLayout(null); // 空布局，可以准确的定位组件在容器中的位置和大小
            this.setTitle("绑定端口");
            jf = this;
            // 注意：JPasswordField用于密码，取值方法String.valueOf(pass.getPassword())
            if (port == -1) {
                txtPort = new JTextField("8000", 30); // 初值，列数
            } else {
                txtPort = new JTextField(main.port + "", 30); // 初值，列数
            }
            JLabel nameLab = new JLabel("端口:"); //
            nameLab.setBounds(100, 60, 40, 20); // left,top,width,height
            txtPort.setBounds(160, 60, 120, 20);
            this.add(nameLab);
            this.add(txtPort);

            JButton JB1 = new JButton("绑定");
            JB1.setBounds(160, 160, 100, 30);
            this.add(JB1);

            // 加上按键事件
            ActionListener al = new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    String portStr = txtPort.getText().trim();
                    if (portStr.isEmpty()) {
                        JOptionPane.showMessageDialog(null, "输入不能为空！");
                        return;
                    }
                    port = Integer.valueOf(portStr);
                    jf.setVisible(false);
                    main.setTitle("服务器:绑定端口" + portStr);
                    JOptionPane.showMessageDialog(null, "绑定成功");
                }
            };
            JB1.addActionListener(al);
            this.setVisible(true);
            this.setDefaultCloseOperation(WindowConstants.HIDE_ON_CLOSE);
        }
    }

    public int getPort() {
        return port;
    }

    public void appendStr(int i, String str) {
        if (i == 1) {
            String[] s = str.split("#");
            txtaReceive.append(s[3] + "  \r" + s[1] + ":  \r" + s[2] + " \r\n");
        } else {
            txtaUser.append(str + "\n");
        }
    }

    public void showUser(ArrayList<String> s) {
        txtaUser.setText("");
        for (String str : s) {
            appendStr(2, str);
        }
    }
}
